"""MCP SDK client with stream-boundary evidence; no hand-written protocol emulator."""
from contextlib import asynccontextmanager, contextmanager
from datetime import timedelta
import importlib.metadata
import json
import logging
from pathlib import Path
import sys

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.exceptions import McpError

SDK_VERSION = "1.30.0"
ROOT = Path(__file__).resolve().parents[2]


def dump(value):
    return value.model_dump(mode="json", by_alias=True, exclude_none=True)


class RecordingStream:
    """Transparent SDK message-stream adapter; records actual assigned RPC IDs."""

    def __init__(self, stream, events, connection, direction):
        self.stream = stream
        self.events = events
        self.connection = connection
        self.direction = direction

    def record(self, value):
        event = {"sequence": len(self.events) + 1, "connection": self.connection, "direction": self.direction}
        if isinstance(value, Exception):
            # Validation detail includes platform-specific docs; retain stable classification.
            event["transport_error"] = type(value).__name__
        else:
            event["message"] = dump(value.message)
        self.events.append(event)

    async def send(self, value):
        self.record(value)
        await self.stream.send(value)

    async def receive(self):
        value = await self.stream.receive()
        self.record(value)
        return value

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.receive()
        except anyio.EndOfStream:
            raise StopAsyncIteration

    async def aclose(self):
        await self.stream.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.aclose()


@asynccontextmanager
async def connection(events, stderr_path, fault="normal", server_file=None):
    args = [str(server_file)] if server_file else ["-m", "lab.mcp_lab.server"]
    parameters = StdioServerParameters(
        command=sys.executable,
        args=args + ["--fault", fault],
        cwd=str(ROOT),
        # Do not forward API keys or user-defined environment variables.
        env={"PYTHONPATH": str(ROOT), "PYTHONUNBUFFERED": "1"},
    )
    with Path(stderr_path).open("w", encoding="utf-8") as errlog:
        async with stdio_client(parameters, errlog=errlog) as (read, write):
            incoming = RecordingStream(read, events, fault, "server_to_client")
            outgoing = RecordingStream(write, events, fault, "client_to_server")
            async with ClientSession(incoming, outgoing, read_timeout_seconds=timedelta(seconds=3)) as session:
                yield session


def tool_error(result, marker=None):
    text = " ".join(block.text for block in result.content if block.type == "text")
    return result.isError and (marker is None or marker in text)


def check(checks, name, passed, evidence):
    checks.append({"name": name, "passed": bool(passed), "evidence": evidence})


@contextmanager
def client_diagnostics(path):
    """Keep the deliberate stdout corruption diagnostic in a reviewable file."""
    logger = logging.getLogger("mcp.client.stdio")
    handler = logging.FileHandler(path, encoding="utf-8")
    before = logger.propagate
    logger.addHandler(handler)
    logger.propagate = False
    try:
        yield
    finally:
        logger.propagate = before
        logger.removeHandler(handler)
        handler.close()


async def _run_checks(out, server_file, exercise, events, checks):
    async with connection(events, out / "normal.stderr.txt", server_file=server_file) as session:
        initialization = await session.initialize()
        check(checks, "initialize_capabilities", initialization.capabilities.tools is not None,
              {"protocolVersion": initialization.protocolVersion, "server": dump(initialization.serverInfo)})
        tools = await session.list_tools()
        lookup = next((t for t in tools.tools if t.name == "lookup_article"), None)
        check(checks, "discovery_schemas", lookup is not None and bool(lookup.outputSchema),
              {"tools": [dump(t) for t in tools.tools]})
        found = await session.call_tool("lookup_article", {"record_id": "KB-EXPORT-2"})
        record = (found.structuredContent or {}).get("record")
        check(checks, "valid_lookup", not found.isError and isinstance(record, dict)
              and record.get("id") == "KB-EXPORT-2",
              dump(found))
        malformed = await session.call_tool("lookup_article", {"record_id": 7})
        check(checks, "malformed_arguments", tool_error(malformed, "Input validation error"), dump(malformed))
        extra = await session.call_tool("lookup_article", {"record_id": "KB-RESET", "grant": "write"})
        check(checks, "extra_argument_denied", tool_error(extra, "Input validation error"), dump(extra))
        unknown = await session.call_tool("delete_account", {"record_id": "KB-RESET"})
        check(checks, "unknown_tool", tool_error(unknown, "unknown_tool"), dump(unknown))
        missing = await session.call_tool("lookup_article", {"record_id": "KB-MISSING"})
        check(checks, "unknown_record", tool_error(missing, "unknown_record"), dump(missing))
        adversarial = await session.call_tool("lookup_article", {"record_id": "KB-INJECTION"})
        still_listed = await session.list_tools()
        check(checks, "untrusted_evidence_no_authority",
              not adversarial.isError
              and (adversarial.structuredContent or {}).get("trust") == "untrusted_evidence"
              and all(t.name != "delete_account" for t in still_listed.tools),
              {"result": dump(adversarial), "permitted_tool": "lookup_article",
               "note": "Host performs no model-driven instruction execution; this is a boundary check, not an injection-defense benchmark."})
        if exercise:
            extension = next((t for t in tools.tools if t.name == "list_topics"), None)
            check(checks, "learner_discovery_schema",
                  extension is not None and bool(extension.outputSchema)
                  and extension.inputSchema.get("additionalProperties") is False,
                  {"tool": dump(extension) if extension else None})
            result = await session.call_tool("list_topics", {})
            expected = ["account", "adversarial", "export"]
            check(checks, "learner_list_topics", not result.isError
                  and result.structuredContent == {"topics": expected}, dump(result))
            result = await session.call_tool("list_topics", {"extra": "denied"})
            check(checks, "learner_extra_argument_denied", tool_error(result, "Input validation error"), dump(result))

    # Requests are assigned IDs by the SDK; notifications have no ID.
    normal = [e for e in events if e["connection"] == "normal" and "message" in e]
    requests = [e["message"]["id"] for e in normal
                if e["direction"] == "client_to_server" and "id" in e["message"]]
    responses = [e["message"]["id"] for e in normal
                 if e["direction"] == "server_to_client" and "id" in e["message"]]
    initialized = any(e["message"].get("method") == "notifications/initialized" for e in normal)
    check(checks, "request_id_correlation",
          initialized and len(set(requests)) == len(requests) and sorted(requests) == sorted(responses),
          {"request_ids": requests, "response_ids": responses, "initialized_notification": initialized})
    stderr = (out / "normal.stderr.txt").read_text(encoding="utf-8")
    check(checks, "stderr_separated", "server ready" in stderr and not any("transport_error" in e for e in events),
          {"diagnostic_in_stderr": "server ready" in stderr, "normal_transport_errors": 0})

    for fault in ("timeout", "disconnect"):
        observed = None
        async with connection(events, out / (fault + ".stderr.txt"), fault, server_file) as session:
            await session.initialize()
            await session.list_tools()
            try:
                await session.call_tool("lookup_article", {"record_id": "KB-RESET"},
                                        read_timeout_seconds=timedelta(seconds=0.35))
                observed = "unexpected_success"
            except McpError as error:
                observed = error.error.code
        # Observed error codes of the pinned SDK, not portable protocol constants.
        expected = 408 if fault == "timeout" else -32000
        call_id = next(e["message"]["id"] for e in reversed(events)
                       if e["connection"] == fault and e.get("message", {}).get("method") == "tools/call")
        check(checks, "bounded_" + fault, observed == expected,
              {"observed_error_code": observed, "expected_error_code": expected,
               "request_timeout_seconds": 0.35, "request_id": call_id,
               "outcome": "no_success_response", "retry_count": 0})

    with client_diagnostics(out / "client.stderr.txt"):
        async with connection(events, out / "stdout-noise.stderr.txt", "stdout-noise", server_file) as session:
            await session.initialize()
            await session.list_tools()
    noise = [e for e in events if e["connection"] == "stdout-noise" and "transport_error" in e]
    check(checks, "stdout_noise_detected", len(noise) >= 1,
          {"transport_errors": [e["transport_error"] for e in noise],
           "note": "The SDK reports the invalid line and can continue; never depend on recovery from stdout contamination."})


def error_leaves(error):
    children = getattr(error, "exceptions", None)
    if children is not None:
        return [leaf for child in children for leaf in error_leaves(child)]
    return [{"type": type(error).__name__, "message": str(error)[:1000]}]


async def run_suite(out, server_file=None, exercise=False):
    """Create evidence even when a learner server violates a protocol contract."""
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("Output directory must be empty; select a fresh --out path")
    out.mkdir(parents=True, exist_ok=True)
    installed = importlib.metadata.version("mcp")
    if installed != SDK_VERSION:
        raise ValueError("This lab requires mcp==" + SDK_VERSION + "; installed " + installed)
    events, checks = [], []
    aborted = False
    try:
        await _run_checks(out, server_file, exercise, events, checks)
    except Exception as error:
        aborted = True
        check(checks, "integration_aborted", False,
              {"errors": error_leaves(error), "note": "Later checks did not run. Inspect messages and server stderr."})
    report = {
        "schema_version": 1,
        "transport": "stdio",
        "sdk": {"package": "mcp", "version": installed},
        "data": "synthetic read-only articles",
        "aborted": aborted,
        "planned_checks": 16 if exercise else 13,
        "passed": sum(item["passed"] for item in checks),
        "total": len(checks),
        "checks": checks,
    }
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "messages.jsonl").write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
    return report
