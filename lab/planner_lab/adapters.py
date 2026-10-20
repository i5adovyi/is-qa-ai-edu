"""Optional transports. No credential values, raw provider errors, or reasoning are logged."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile

from lab.contracts import HarnessError
from .runtime import DECISION_SCHEMA, LOOKUP_SCHEMA, PROPOSAL_SCHEMA, completion, strict_json


async def child_output(command, data, cwd=None):
    process = await asyncio.create_subprocess_exec(
        *command, cwd=cwd, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await process.communicate(data.encode("utf-8"))
        if process.returncode:
            # CLI/HTTP text may include account data. Return classification only.
            raise HarnessError("transport_error", "Child transport failed; details intentionally omitted.")
        if len(stdout) > 2_000_000:
            raise HarnessError("malformed_output", "Transport output exceeds limit.")
        return stdout.decode("utf-8")
    finally:
        if process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=2)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()


class ResponsesPlanner:
    """Actual HTTPS adapter with an injected async transport for offline contract tests."""
    evidence_label = "live_responses_api"

    def __init__(self, model, max_output_tokens=1024, transport=None):
        if not model or not 16 <= max_output_tokens <= 8192:
            raise ValueError("Specify a model and max_output_tokens between 16 and 8192.")
        self.model, self.max_output_tokens = model, max_output_tokens
        self.transport = transport or self.http_transport
        self.history, self.pending_call_id = [], None

    async def http_transport(self, payload, timeout):
        from .runtime import ROOT
        raw = await child_output(
            [sys.executable, "-m", "lab.planner_lab.http_worker"],
            json.dumps({"payload": payload, "timeout": min(timeout, 60)}), cwd=str(ROOT))
        envelope = strict_json(raw)
        if "error" in envelope:
            raise HarnessError(envelope["error"], "Provider transport did not complete.")
        return envelope["response"]

    async def propose(self, request, timeout):
        # Mutate conversation state only after a successful response.
        history = deepcopy(self.history)
        if not history:
            history = [{"role": "user", "content": json.dumps(
                {"ticket": request["ticket"], "catalog": request["catalog"]})}]
        elif self.pending_call_id:
            history.append({"type": "function_call_output", "call_id": self.pending_call_id,
                            "output": json.dumps(request["observations"][-1])})
        payload = {
            "model": self.model, "store": False, "instructions": request["instructions"],
            "input": history, "parallel_tool_calls": False, "tool_choice": "required",
            "max_output_tokens": self.max_output_tokens,
            "tools": [
                {"type": "function", "name": "lookup_article", "description": "Read synthetic article by ID.",
                 "parameters": LOOKUP_SCHEMA, "strict": True},
                {"type": "function", "name": "complete", "description": "Propose a final local draft or escalation.",
                 "parameters": DECISION_SCHEMA, "strict": True},
            ],
        }
        response = await self.transport(payload, timeout)
        if type(response) is not dict:
            raise HarnessError("malformed_output", "Provider response is not an object.")
        output = response.get("output", [])
        if type(output) is not list or any(type(item) is not dict for item in output):
            raise HarnessError("malformed_output", "Provider output is invalid.")
        if any(block.get("type") == "refusal" for item in output
               for block in item.get("content", []) if isinstance(block, dict)):
            raise HarnessError("refusal", "Provider refused the request.")
        if response.get("status") != "completed":
            raise HarnessError("incomplete_response", "Provider response did not complete.")
        calls = [item for item in output if item.get("type") == "function_call"]
        if len(calls) != 1:
            raise HarnessError("malformed_output", "Exactly one function call is required.")
        call = calls[0]
        if not isinstance(call.get("call_id"), str) or not call["call_id"]:
            raise HarnessError("malformed_output", "Function call has no correlation ID.")
        arguments = strict_json(call.get("arguments", ""))
        if call.get("name") == "complete":
            proposal = completion(arguments)
        else:
            proposal = {"kind": "tool", "name": call.get("name"), "arguments": arguments, "decision": None}
        self.history = history + output
        self.pending_call_id = call["call_id"] if proposal["kind"] == "tool" else None
        return {"proposal": proposal, "metadata": {
            "provider": "openai_responses", "requested_model": self.model,
            "model": response.get("model"), "response_id": response.get("id"),
            "usage": response.get("usage"), "max_output_tokens": self.max_output_tokens,
            "parallel_tool_calls": False, "store": False,
        }}


class CodexPlanner:
    """Use supported CLI auth without extracting credentials; no CLI tools are needed."""
    evidence_label = "live_codex_cli_proposal"

    def __init__(self, model, executable="codex"):
        if not model:
            raise ValueError("Specify the model explicitly.")
        self.model = model
        self.executable = shutil.which(executable)
        if not self.executable:
            raise ValueError("Codex CLI is unavailable; use the scripted route.")

    async def propose(self, request, timeout):
        with tempfile.TemporaryDirectory(prefix="signal-desk-planner-") as directory:
            schema = Path(directory) / "schema.json"
            response_path = Path(directory) / "response.json"
            schema.write_text(json.dumps(PROPOSAL_SCHEMA), encoding="utf-8")
            command = [self.executable, "exec", "--ignore-user-config", "--ephemeral",
                       "--skip-git-repo-check", "--sandbox", "read-only", "--json",
                       "--model", self.model, "--output-schema", str(schema),
                       "--output-last-message", str(response_path), "-C", directory]
            for feature in ("shell_tool", "unified_exec", "multi_agent", "apps", "plugins", "skill_search"):
                command.extend(["--disable", feature])
            command.extend(["-c", 'web_search="disabled"', "-"])
            prompt = ("Respond only with the next proposal matching the supplied output schema. "
                      "Do not use host tools, read files, or delegate. An outer harness executes the "
                      "proposal and supplies observations in a subsequent request.\n" + json.dumps(request))
            raw = await child_output(command, prompt)
            events = [strict_json(line) for line in raw.splitlines() if line.strip()]
            items = [event.get("item", {}) for event in events if event.get("type") == "item.completed"]
            if any(item.get("type") in {"command_execution", "mcp_tool_call", "web_search", "file_change"} for item in items):
                raise HarnessError("unexpected_host_tool", "Proposal adapter unexpectedly used a host tool.")
            if any(event.get("type") in {"turn.failed", "error"} for event in events):
                raise HarnessError("provider_error", "CLI reported a failed turn.")
            if not response_path.exists():
                raise HarnessError("malformed_output", "CLI produced no final response.")
            proposal = strict_json(response_path.read_text(encoding="utf-8"))
            usage = next((event.get("usage") for event in reversed(events)
                          if event.get("type") == "turn.completed"), None)
            return {"proposal": proposal, "metadata": {
                "provider": "codex_cli", "requested_model": self.model,
                "model": self.model, "model_identity_source": "explicit_cli_request",
                "usage": usage, "host_tools_used": False,
                "note": "Fresh CLI session per proposal; outer harness supplies observation history.",
            }}


class MCPLookup:
    evidence_label = "real_mcp_sdk_stdio"

    def __init__(self, out):
        self.out, self.events, self.number = Path(out), [], 0

    async def lookup(self, record_id):
        # Optional imports stay off the Python 3.9 / stdlib route.
        from lab.mcp_lab.client import connection, dump
        self.number += 1
        try:
            async with connection(self.events, self.out / ("mcp-%d.stderr.txt" % self.number)) as session:
                initialized = await session.initialize()
                tools = await session.list_tools()
                tool = next((item for item in tools.tools if item.name == "lookup_article"), None)
                if tool is None or not tool.outputSchema:
                    raise HarnessError("mcp_discovery", "Required tool/schema not discovered.")
                result = await session.call_tool("lookup_article", {"record_id": record_id})
                if result.isError:
                    raise HarnessError("mcp_tool_error", "MCP tool rejected the lookup.")
                value = result.structuredContent
                return value
        finally:
            (self.out / "mcp-messages.jsonl").write_text(
                "".join(json.dumps(event) + "\n" for event in self.events), encoding="utf-8")
