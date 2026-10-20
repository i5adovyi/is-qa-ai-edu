# Real MCP subprocess lab

This optional lab runs the **official MCP Python SDK on both sides of a real stdio connection**. The client launches a separate Python server process, initializes the session, discovers tools, and calls a synthetic read-only knowledge service. No LLM, API key, account, network listener, or external ticket system is involved. Installing dependencies needs internet; executing the lab does not.

Start with [Lab 09: real MCP](../../content/labs/09-real-mcp.md) for the exercises. This page is the operational manual.

## Setup

Use **Python 3.12** in a separate environment. The academy's existing standard-library route still runs on Python 3.9. The pinned SDK itself supports Python 3.10+, but the complete dependency snapshot here was verified on Python 3.12.14 and macOS ARM64, not on every Python/platform combination.

First check `python3.12 --version`. If that command is missing, install Python 3.12 from the [official Python downloads](https://www.python.org/downloads/) or use the full path to an existing Python 3.12 interpreter in the first command below. A newer system `python3` is not a substitute for the tested interpreter without a separate compatibility check. Creating the virtual environment does not install Python itself.

From the repository root:

```sh
python3.12 -m venv work/mcp-venv
work/mcp-venv/bin/python -m pip install -r lab/mcp_lab/requirements.lock.txt
work/mcp-venv/bin/python -m pip check
work/mcp-venv/bin/python -m lab.mcp_lab --out work/mcp-run-01
work/mcp-venv/bin/python -m unittest discover -s tests -p 'test_mcp_lab.py' -v
```

On Windows, use `py -3.12 -m venv work/mcp-venv` and replace `work/mcp-venv/bin/python` with `work/mcp-venv/Scripts/python.exe`. Use a fresh output directory on each run. The gate refuses to overwrite evidence. The default gate reports **13/13** checks; the integration suite runs **10** tests. Core tests skip these ten when the optional pinned SDK is absent; a skip is not evidence of passing the MCP lab.

The lock pins the SDK and transitive packages to exact versions. It is a version lock, not a wheel-hash supply-chain guarantee. Review updates deliberately, reinstall in a fresh environment, and repeat the integration gate. Do not silently remove the SDK pin to follow an unrelated example.

## What runs

```text
__main__.py
  client.py → official ClientSession → official stdio_client
    │ separate child process, newline-delimited JSON-RPC
    └ server.py → official low-level Server → lookup_article
                                      └ corpus.json (three synthetic records)
```

`server.py` registers tools only when `make_server()` is called; importing it starts no process or transport. The server validates the tool name independently of the input schema. Unknown names, additional properties, non-string IDs, and unknown records cannot produce a successful lookup. Successful results contain `record` and `trust: "untrusted_evidence"` and are checked against the advertised output schema.

The `readOnlyHint` annotation describes intent. The actual code prevents writes by exposing no mutation handler. A different server could lie about its annotations; the annotation itself is not an access-control mechanism.

`client.py` records messages at the SDK's typed stream boundary. It does not handcraft an `initialize` response or invent request IDs. The request IDs in the evidence are assigned by the official client. The SDK serializes messages over the child's stdin/stdout. This is a runnable interoperability exercise between this SDK's client and server, not a certification of every MCP implementation or client application.

## Evidence files

| Artifact | Use |
|---|---|
| `report.json` | Stable assertions, negotiated protocol version, capabilities, schemas, accepted and rejected call results |
| `messages.jsonl` | Actual SDK messages in order, connection label, direction, request IDs, notifications, and transport-error classifications |
| `normal.stderr.txt` | Human diagnostic written by the server outside protocol stdout |
| `timeout.stderr.txt` | Diagnostics for the deliberately delayed server |
| `disconnect.stderr.txt` | Diagnostics for the child that exits during a call |
| `stdout-noise.stderr.txt` | Server diagnostics during the contamination exercise |
| `client.stderr.txt` | Client parser diagnostic for the intentionally invalid stdout line |

If learner code violates an output contract, the gate writes a failed report and preserves the available message journal. An aborted report explicitly says that later checks did not run; partial progress is not a passing integration.

The report and message journal omit timestamps and wall-clock durations so fixed input produces stable evidence. Diagnostic stack traces can contain machine-specific paths. This lab records complete **synthetic** message content; that choice is unsuitable for real customer data without a redaction policy.

## Failure coverage

| Case | Expected evidence |
|---|---|
| Valid lookup | Structured result for `KB-EXPORT-2` |
| Wrong argument type / extra property | `isError: true`, input validation failure |
| Unknown tool / record | `isError: true`, `unknown_tool` / `unknown_record` |
| Injected article | Malicious sentence remains returned evidence; no new tool becomes available |
| Slow call | Client's 0.35-second call deadline expires; pinned SDK reports code `408` |
| Child exits during call | Connection error, pinned SDK reports `-32000`; no success invented |
| Diagnostic on stdout | SDK reports a parsing error; diagnostic is captured in `client.stderr.txt` |

The deadline applies to a call, not the full process startup. Initialization has a three-second request timeout. Tests impose an overall subprocess deadline, including cleanup. No automatic retry runs. The slow server sleeps for five seconds, so the deadline check exercises an actual timer rather than the reference harness's virtual milliseconds.

The stdout experiment deliberately corrupts the transport. This SDK can report the invalid line and continue, but other hosts may disconnect. Write logs to stderr and do not depend on error recovery. A message with a matching request ID is still not proof of a side effect's persistence; this service has no writes. Design reconciliation separately when extending it to mutations.

## Learner extension

Copy the server and corpus, then implement `list_topics`:

```sh
mkdir work/mcp-student &&
  cp lab/mcp_lab/server.py lab/mcp_lab/corpus.json work/mcp-student/
work/mcp-venv/bin/python -m lab.mcp_lab \
  --server-file work/mcp-student/server.py --exercise --out work/mcp-before
```

The copy command deliberately refuses an existing `work/mcp-student` directory; do not replace `mkdir` with `mkdir -p`, because copying again would overwrite your implementation. If it exists, reuse your work without copying or choose a new directory name and use it in the following commands. The copy command uses a POSIX shell. In PowerShell, use this guarded copy instead, then run the Python gate with the Windows interpreter path:

```powershell
if (Test-Path work/mcp-student) {
  throw "Choose a new learner directory; existing work is preserved."
} else {
  New-Item -ItemType Directory -Path work/mcp-student | Out-Null
  Copy-Item lab/mcp_lab/server.py, lab/mcp_lab/corpus.json `
    -Destination work/mcp-student/
}
```

Expected before implementation: **13/16**, exit code `1`. Add the tool with an empty-object input schema that rejects extra properties. Return exactly `{"topics": ["account", "adversarial", "export"]}` by deriving sorted unique topics from the corpus. Advertise a structured output schema and read-only annotations. Keep lookup validation intact. Rerun with `--out work/mcp-after`; target **16/16**. See [solution guidance](solutions.md) after your attempt.

The exercise client accepts a server source path because the learner must run code they edited. Python code runs with the learner's OS permissions; the MCP tool allowlist does not sandbox that process.

## Troubleshooting

| Symptom | Check |
|---|---|
| Optional dependency message | Invoke the venv's Python, not the system Python |
| SDK version mismatch | Recreate the environment from the lock; current-major examples use different APIs |
| `corpus.json` missing in learner copy | Copy both the server and corpus as shown above |
| Timeout during initialization | Inspect the connection's stderr; first import on a slow machine may exceed three seconds |
| Output directory is not empty | Choose another output path to preserve the previous experiment |
| JSON parsing failure | Remove human output from stdout; inspect `client.stderr.txt` |
| Core suite reports skips | Run the optional tests with the MCP venv to establish the MCP result |

## Versions and primary sources

Checked 20 October 2026. This lab pins **`mcp==1.30.0`**, the supported v1 maintenance line. The current major is v2; a migration is an additional engineering exercise, not an implicit dependency upgrade. The v1 APIs are chosen to make the connection and message-stream boundaries explicit. The report records the protocol version actually negotiated.

- [Official Python SDK v1.30.0 source and maintenance policy](https://github.com/modelcontextprotocol/python-sdk/tree/v1.30.0)
- [Exact SDK release metadata](https://pypi.org/project/mcp/1.30.0/)
- [Official v1 client documentation](https://py.sdk.modelcontextprotocol.io/v1/client/)
- [MCP stdio transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP tool input, output, and error contracts](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [Official migration guide for v2](https://py.sdk.modelcontextprotocol.io/migration/)
