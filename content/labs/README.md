# Eleven engineering labs

Build engineering judgment by observing a working system, predicting a failure, making a narrow change, and testing the prediction. The [Signal Desk manual](../../lab/README.md) explains setup and every CLI command.

The reference implementation works immediately. Your separate workspace is `lab/student.py`; eight deliberately unfinished functions let you practice without dismantling the baseline. The `practice` command checks that workspace. The unit-test suite checks the reference harness and public solution implementations.

| Lab | Engineering question | Student function | Suggested time |
|---|---|---|---|
| [01 — Data boundaries](01-data-boundaries.md) | What information should survive into a prompt or log? | `redact_sensitive` | 45–75 min |
| [02 — Context budgets](02-context-budgets.md) | Which evidence deserves scarce space? | `pack_context` | 60–90 min |
| [03 — Tool authority](03-tool-authority.md) | Who decides what an agent may do? | `tool_allowed` | 60–90 min |
| [04 — Retries and budgets](04-retries-and-budgets.md) | When should an agent stop trying? | `retry_delay_ms` | 60–90 min |
| [05 — Idempotency and recovery](05-idempotency-and-recovery.md) | Did the effect happen before the crash? | `operation_key` | 75–120 min |
| [06 — Grounding and evaluation](06-grounding-and-evaluation.md) | Does a citation make an answer true? | `citations_valid` | 60–90 min |
| [07 — Traces and diagnosis](07-traces-and-diagnosis.md) | Can another engineer explain a failed run? | `summarize_trace` | 60–90 min |
| [08 — Ship an evaluated policy](08-ship-an-evaluated-policy.md) | Can you improve usefulness without weakening the boundary? | `build_decision` | 90–150 min |
| [09 — Real MCP](09-real-mcp.md) | Can a separate client and server negotiate and exchange valid tool results? | SDK client/server integration | 120–180 min |
| [10 — Installed skill](10-installed-skill.md) | Can a fresh host discover and correctly use your installed procedure? | Skill package and host evidence | 75–120 min |
| [11 — Complete student harness](11-complete-student-harness.md) | Do all eight components actually control an evaluated run? | Composed runner and component evidence | 120–240 min |

Times are planning estimates, not promises. Expect roughly 9–13 focused hours for the first eight implementations and written reviews, plus 5–9 hours for the integration labs. Setup, debugging and stretch work can add time. See the [integration route](../../docs/INTEGRATION-LABS.md) for prerequisites and sequence.

## The work loop

1. Read the lab and write your prediction **before** running the experiment.
2. Run the reference behavior and inspect its artifacts.
3. Implement only the named function in `lab/student.py`.
4. Run `python3 -m lab.cli practice --lab NN`.
5. Add at least two cases that distinguish your implementation from a plausible wrong one.
6. Write a short evidence note with the hypothesis, changed behavior, command, output, and remaining weakness.
7. Consult [progressive hints](hints/README.md) only after a concrete attempt; [solutions](solutions/README.md) are separate spoilers.

This function-by-function loop applies to labs 01–08. Labs 09–11 supply their own setup, execution and evidence commands. Every lab has a completion gate and a deeper review question. Passing a gate proves its stated contract, not mastery of the entire engineering topic.

## Portfolio evidence

Keep your own notes under `work/`, which is excluded from distribution. For each lab, save:

- A prediction and a short decision record.
- The exact command and a concise result excerpt.
- Two additional adversarial cases and their outcomes.
- One remaining limitation and a next experiment.

For lab 11, include the student code, train and holdout reports, component invocation evidence, an annotated failure trace, and a two-minute explanation of the trust boundary. A reviewer can reproduce the composed harness offline. Actual host behavior in lab 10 requires the chosen assistant host; do not substitute a local validator result for that evidence.
