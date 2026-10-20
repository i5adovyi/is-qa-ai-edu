# Lab 12 — A model proposes, the harness executes

**Prerequisites:** lessons 07–09 and 13–16; complete Lab 11's component gate first. Read the [planner README](../../lab/planner_lab/README.md) for file names and commands. The core route uses Python 3.9+ with no packages or network access. Actual MCP uses Lab 09's Python 3.12 environment. Live routes need your own supported host login or API access.

**Time budget:** read and predict 20–30 minutes; scripted practice 45–75 minutes; MCP integration 20–40 minutes; optional live comparison 45–90 minutes. These are planning ranges, not measured learner timings.

**Learning objective:** demonstrate a proposal, validated execution, observation, and subsequent decision. Explain which component owns permission and which evidence establishes actual model use.

The Lab 11 harness runs a fixed sequence. This lab adds a separate planner runtime. It reuses the existing `validate_decision` rules and actual Lab 09 MCP server; it does not silently replace the composed harness or bypass its student gate. The runtime still controls allowed tools, arguments, evidence, deadlines, retries, and the final local draft.

## Start with a prediction

Do not open the runtime's scripted reference or the checked-in execution evidence yet.

The task is a synthetic customer asking what to try when an export times out in version 2.4. The catalog lists an export article, an account article, and an untrusted supplier note. Catalog titles supply routing hints, not answer evidence.

Write a four-line prediction:

```text
What the planner should propose first:
What the runtime must check before acting:
What the next planner request should contain:
What must be true before a local draft can be accepted:
```

You need no API key for this step. A tutor should review this attempt before showing a trace.

## Gate A — Scripted planner and actual execution

Run from the repository root, using a fresh output path:

```sh
python3 -m lab.planner_lab --out work/planner-a
```

This is **scripted planner + local fixture lookup**. It should produce `report.json`, `trace.jsonl`, and one local `draft.json`. There is no send tool. Read the trace and mark:

1. The proposal; this is untrusted input to the runtime.
2. Argument validation and dispatch.
3. The observation, with its source ID and trust label.
4. The second proposal and validated completion.

Compare the trace with your prediction. Explain why a tool result is not automatically a correct final answer.

Implement `StudentPlanner.propose` in [student.py](../../lab/planner_lab/student.py). Return one proposal at a time; use the supplied `request["output_schema"]`. Your planner must not call a tool directly.

```sh
python3 -m lab.planner_lab --backend student --out work/planner-student-before
```

Before implementation, expected exit code is **1**, with `student_incomplete` in the report. Preserve it. Then implement the lookup choice and a subsequent decision based on the actual observation. Re-run with a new output directory. Keep the reference runtime and validators unchanged.

**Pass criteria:** two distinct proposals; the second request contains the first tool's result; citations refer to retrieved, relevant evidence; no undeclared operation runs. A correct final string without this trace does not pass the integration gate.

## Make the boundary fail

Predict the stopping layer before each run:

```sh
python3 -m lab.planner_lab --scenario repeated --out work/planner-repeated
python3 -m lab.planner_lab --scenario premature --out work/planner-premature
python3 -m lab.planner_lab --scenario malformed --out work/planner-malformed
python3 -m lab.planner_lab --scenario refusal --out work/planner-refusal
python3 -m lab.planner_lab --scenario rate-limit --out work/planner-rate-limit
python3 -m unittest tests.test_planner_lab -v
```

Do not chain expected failures with `&&`: it would stop the sequence after the first failure. Consult [fault-fixtures.json](../../lab/planner_lab/fault-fixtures.json) **after** writing predictions. Failing scenarios exit 1 and preserve a trace; the retry scenario should finish after a bounded retry.

The tests also exercise timeout, cancellation during work, a strict wall-clock deadline, process cleanup, exhausted budgets, unknown tools, extra arguments, wrong source identities, stale product versions, and attempted authority expansion through retrieved text.

Add one new fault of your own. Preserve its input, predicted outcome, actual report, and a regression test. Do not “repair” the test by relaxing permission or citation checks.

For cancellation, supply `--cancel-file work/planner.cancel` and create that file from a second terminal while a live request is active. A pre-existing file causes immediate cancellation. Use a new path or remove your own marker before another run. The runtime cancels its adapter and local child process; cancellation cannot prove the remote provider stopped processing or billing.

## Gate B — The same loop over actual MCP

Complete [Lab 09](09-real-mcp.md) first. With its environment activated:

```sh
python -m lab.planner_lab --lookup mcp --out work/planner-mcp
python -m unittest tests.test_planner_lab -v
```

Compare `mcp-messages.jsonl` with `trace.jsonl`. Find discovery, the `tools/call` request and response, and the observation received by the planner. Server diagnostics go to `mcp-1.stderr.txt`, outside protocol stdout.

This gate proves **scripted planner + real MCP SDK/stdio**. It still contains no AI planner. A schema annotation cannot authorize a write; the runtime allowlist only dispatches `lookup_article`.

## Gate C — Optional actual model

Choose one route. Keep each run to two decisions and two attempts for the first experiment. If a model needs more steps, preserve the failure and justify a revised limit before a new run.

### Existing Codex login

Use the supported CLI login you already have; check `codex login status`. Set `SIGNAL_DESK_MODEL` to an accessible model identifier you explicitly choose. Do not paste credentials into any file in this repository.

```sh
python -m lab.planner_lab --backend codex --model "$SIGNAL_DESK_MODEL" \
  --lookup mcp --deadline 90 --max-attempts 2 --max-decisions 2 \
  --max-retries 0 --out work/planner-live
```

The adapter creates an ephemeral, read-only CLI session for each proposal, disables its unrelated tools, and supplies observation history itself. Only the outer runtime executes the proposal. It uses invocation-local settings, preserves supported authentication, and does not modify global configuration. The official [non-interactive CLI documentation](https://learn.chatgpt.com/docs/non-interactive-mode) describes structured final output and JSONL events.

Record the requested model and `model_identity_source`: CLI evidence names the explicitly requested model; it does not establish an immutable server-side model revision. Available usage comes from CLI events and includes host overhead. This route does not expose a per-request output-token cap; its controls are attempts, decisions, and wall time.

### Responses API adapter

Supply `OPENAI_API_KEY` through your existing environment or secret manager. The adapter reads it only inside its HTTP worker. Choose an accessible model explicitly. API usage may be billed separately from a chat subscription.

```sh
python -m lab.planner_lab --backend responses --model "$SIGNAL_DESK_MODEL" \
  --lookup mcp --deadline 90 --max-attempts 2 --max-decisions 2 \
  --max-retries 0 --max-output-tokens 1024 --out work/planner-api
```

The working adapter offers two strict function schemas, forwards a validated observation using its call ID, and records returned model identity and usage. Provider responses remain proposals. [Official function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling) is the API reference for this seam. If your selected model rejects a setting, keep the failure and consult its current official documentation before changing it.

The API route bounds output tokens per request, request attempts, context characters, and wall time. It does **not** guarantee a dollar ceiling: input tokens, cached rates, retries, and provider billing differ. `cost_usd` remains unavailable until you calculate it using actual usage and an explicitly dated price source. A failed request may still incur usage.

The API wire format has offline fake-transport regression coverage. A successful CLI run does not validate API credentials, account access, or live Responses behavior. Label those separately.

## Optional host connection: who owns the loop?

This exercise connects the same server directly to an assistant host. It is independent of the outer planner runtime. Use your MCP environment's Python path; do not substitute its resolved base-interpreter path.

```sh
python3 -m lab.planner_lab.host --model "$SIGNAL_DESK_MODEL" \
  --python work/mcp-venv/bin/python --out work/host-mcp --deadline 90
```

Adjust `--python` to your actual environment; on Windows this commonly ends with `Scripts/python.exe`. The helper passes server command, arguments, working directory, tool allowlist, and required-startup settings to a single CLI invocation. Only this synthetic read-only lookup is approved for that invocation. It does not install global MCP configuration. These configuration fields are documented in the [official MCP host guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Inspect `host-report.json`: confirm an actual completed MCP tool call, its arguments and returned record, followed by the host's final response. Compare who dispatched the call in this run versus Gate C. A host saying “I used MCP” without a tool event is insufficient evidence.

## Model behavior: three small experiments

First predict, then run, then explain:

1. **Schema versus truth.** Change a proposed draft to include a plausible but unsupported guarantee while preserving the schema and a valid citation. Which checks pass? Independently label each claim supported, contradicted, or not established. The regression suite deliberately demonstrates a semantically wrong answer that passes structural validation. Extend the content gate only after defining the claim you intend to catch.
2. **Characters versus tokens.** Compare the request's `context_chars` with available provider input-token usage. Include English text, an emoji, and an identifier in three scratch strings. Count characters and UTF-8 bytes locally. If you use a matching tokenizer, record its name/version; otherwise mark token counts unavailable. Do not derive a universal token ratio from three strings. CLI input usage includes its own instructions, so it cannot be equated with this request's character count.
3. **Repeated runs.** Repeat the same live task three times with identical request configuration and new output directories. Record selected article, final action, grounded claims, latency, and usage. Identical results do not prove determinism; different phrasing does not necessarily mean different correctness. If model access is unavailable, complete the prediction and mark actual sampling evidence pending.

## Submission and evidence labels

Submit your prediction, student planner, success trace, one new fault/test, and a claim-level review. Add separate rows for:

| Evidence | What it establishes |
| --- | --- |
| Scripted + fixture | Runtime integration with controlled proposals |
| Scripted + real MCP | Actual SDK/stdio discovery and execution |
| Live planner + real MCP | Model proposal → validated execution → observation → subsequent model decision |
| Actual assistant host + MCP | Host discovery and a model-selected tool call in that host |
| Live Responses API | That specific API, model request, account, and transport worked |

Do not fill an unavailable row with a simulated result. Automated completion is a structural gate; practical mastery additionally requires explaining the failure layers and reviewing claims.

After your attempt, inspect [recorded integration evidence](../../lab/planner_lab/EVIDENCE.md). It is an instructor example, not evidence that your own environment or implementation passes.
