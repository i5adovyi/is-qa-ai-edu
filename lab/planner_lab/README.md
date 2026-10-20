# Planner integration lab

Start with [Lab 12](../../content/labs/12-model-tool-loop.md). Its prediction checkpoint keeps the reference implementation and execution trace out of your first attempt.

The core requires Python 3.9+ and the standard library. `--lookup mcp` additionally requires the pinned [Lab 09 environment](../mcp_lab/README.md). Live backends are explicit: default commands never contact a provider.

| File | Responsibility |
| --- | --- |
| `student.py` | Your deterministic planner exercise; initially incomplete |
| `runtime.py` | Proposal validation, allowlisted execution, observations, completion, budgets, cancellation |
| `adapters.py` | Responses transport, supported Codex CLI transport, actual MCP lookup |
| `http_worker.py` | Isolated blocking HTTPS operation that can be terminated on deadline |
| `host.py` | Optional independent assistant-host connection using invocation-local settings |
| `fault-fixtures.json` | Expected failure outcomes; consult after predicting |

Run from the repository root:

```sh
python3 -m lab.planner_lab --out work/planner-first
python3 -m lab.planner_lab --backend student --out work/planner-student
python3 -m unittest tests.test_planner_lab -v
```

The starter student command deliberately exits 1 with `student_incomplete`. Core tests pass with one optional MCP test skipped when the SDK is unavailable. In the MCP environment, all planner tests should run.

Exit codes: **0** accepted structural draft; **1** failed, cancelled, escalated, or incomplete student run with report; **2** CLI configuration/setup failure. Reports do not claim semantic correctness. Use a fresh output directory each time.

The runtime is deliberately small: one synthetic task, one read-only tool, no arbitrary shell, no sending, no account mutation. A model cannot expand the tool list by returning extra fields. It reuses `lab.policy.validate_decision` but is a separate extension to the composed student harness. It does not claim to supply checkpoints or a production service.

Credentials are never included in prompts or evidence. Failure logs retain typed errors; raw provider errors and CLI diagnostics are not persisted. Only synthetic proposals, observations, selected metadata, and final drafts are recorded. Raw model reasoning is excluded.

For optional live configuration, budget limits, current official references, and a comparison of SDK/host/API evidence, follow Lab 12. See [EVIDENCE.md](EVIDENCE.md) only after your attempt.
