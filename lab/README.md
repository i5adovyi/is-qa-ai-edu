# Signal Desk engineering lab

A complete, offline practice system for learning how an agent's surrounding software changes its behavior. Signal Desk handles **synthetic support tickets**, retrieves a small approved handbook, drafts responses locally, and escalates unsupported requests.

The policy is explicit Python rules. **There is no LLM, API key, subscription requirement, network access, or paid service.** This makes failure experiments repeatable and lets you understand the harness before adding a model. Tools never send email, contact customers, invoke a shell, or connect to a real ticket system.

## Start in five minutes

Requirements: Python 3.9 or later; terminal opened at the repository root. The suite was verified with Python 3.9.6. No installation step or third-party dependencies.

```sh
python3 --version
python3 -m lab.cli demo
python3 -m lab.cli evaluate --split train
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The demo prints a local draft and its run-artifact directory. The training gate should report **18/18 cases and 11/11 scenarios**. Unit tests should pass. One test deliberately injects a failing policy to verify the regression gate.

Open [the practice labs](../content/labs/README.md) next. Their starter checks intentionally fail until you implement the corresponding function in `lab/student.py`. They do not break the reference harness.

After Labs 01–08, [Lab 11](../content/labs/11-complete-student-harness.md) composes all eight functions into the running harness. The complete wiring and a runnable disclosed instructor example ship together; `lab/student.py` remains your intentional exercise workspace. Use `python3 -m lab.composed evaluate --components completed` to inspect the example, then `--components student` to assess your own eight implementations. The student profile never substitutes missing functions, and a passing example report does not count as learner completion. Keep or adapt your existing student work; do not overwrite it with the example just to make the gate green.

For a real-model experiment without an API key, use the [manual model bridge](model-bridge.md): export a prompt, obtain a JSON answer from any chat model, and replay it through this harness. A labeled mock response makes the same workflow runnable offline.

## Exact commands

Commands below use distinct output directories. A run refuses to overwrite an existing nonempty directory; use a new name when repeating.

```sh
# Normal reference run; output directory omitted means a fresh .lab-runs subdirectory.
python3 -m lab.cli demo --scenario normal --case train-01

# A concrete trace experiment.
python3 -m lab.cli demo --scenario timeout-once --out .lab-runs/timeout-experiment
python3 -m lab.cli trace .lab-runs/timeout-experiment/trace.jsonl
python3 -m lab.cli trace .lab-runs/timeout-experiment/trace.jsonl --json

# Tool contracts, without execution.
python3 -m lab.cli schemas

# Train while iterating. Use holdout for a final check.
python3 -m lab.cli evaluate --split train
python3 -m lab.cli evaluate --split holdout
python3 -m lab.cli evaluate --split all

# Student extension checks; initially nonzero by design.
python3 -m lab.cli practice --lab 01
python3 -m lab.cli practice --lab 08
python3 -m lab.cli evaluate --policy student --split train
python3 -m lab.cli evaluate --policy student --split holdout
```

`evaluate --no-scenarios` runs only ticket cases. The standard gate includes fault scenarios. A successful run exits `0`; a failed run or acceptance gate exits `1`; a command/configuration error exits `2`; the intentional crash scenario exits `3`.

## Failure experiments

| Scenario | Expected outcome | Lesson |
|---|---|---|
| `normal` | Completed, one draft/write | Observe the normal sequence |
| `injection` | Escalated, zero writes | Untrusted instructions are input data |
| `timeout-once` | One retry, then completion | Recover from transient failure |
| `timeout-always` | Failed with `tool_timeout` | Retry limit prevents looping |
| `invalid-tool` | Failed with `tool_denied` | Policy output cannot expand tool authority |
| `budget` | Failed with `budget_exhausted` | Attempts count toward limits |
| `duplicate` | Two save calls, one write | Idempotent effect, repeated acknowledgment |
| `crash-after-write` | Deliberate stop; resume completes | Recover an uncertain acknowledgment |
| `denied-tag` | Draft saved; tag rejected | Failure does not roll back prior effects |
| `approved-tag` | Draft and tag saved | Specific grant permits specific mutation |
| `context-overflow` | Read result rejected by budget | Bound what reaches the policy |

Example:

```sh
python3 -m lab.cli demo --scenario invalid-tool
```

Its nonzero exit is the intended result of this experiment. The scenario acceptance suite expects and scores that failure correctly.

Recovery experiment:

```sh
python3 -m lab.cli demo --scenario crash-after-write --out .lab-runs/recovery-experiment
# The preceding command deliberately exits 3. Run the next command separately.
python3 -m lab.cli resume .lab-runs/recovery-experiment/checkpoint.json
python3 -m lab.cli trace .lab-runs/recovery-experiment/trace.jsonl
```

Expected final result: one draft, one durable write, a `run_resumed` event, and a `tool_result` with `replayed=true`. The committed draft and its deduplication record live in the same atomic store replacement. The checkpoint preserves the pending operation and consumed budget.

## Architecture you can read in an hour

```text
cli.py
  ├── engine.py: bounded state machine and checkpoints
  │     ├── policy.py: deterministic classification and decision
  │     ├── tools.py: external authorization and tool dispatch
  │     ├── contracts.py: schemas, errors, limits and accounting
  │     └── storage.py: local effects, idempotency and traces
  ├── evaluation.py: case assertions and failure-scenario acceptance
  ├── practice.py → student.py: focused helper acceptance checks
  └── composed.py → student.py or completed.py: all eight integrated components
```

`model_bridge.py` exports synthetic requests and replays saved responses through `Runner`; it makes no provider calls. Labs 01–08 start with focused function exercises. `composed.py` connects all eight to read authorization, redaction, selected context, retries, mutation keys, citation validation, decision, and trace summary. Lab 08's ordinary `--policy student` mode and the model bridge substitute only the decision seam; use the explicit composition gate for full integration evidence.

Read `contracts.py`, `tools.py`, `engine.py`, then `evaluation.py`. Follow one `save_draft` operation from the decision contract through the dispatcher to the durable store.

Every run produces:

| File | Contains | Handling |
|---|---|---|
| `trace.jsonl` | Event sequence, commit/replay markers, argument names, hashes, usage, error codes | No full ticket or draft text |
| `checkpoint.json` | Pending phase, observations, decision, budget usage | Contains synthetic ticket and draft text |
| `store.json` | Ticket, drafts, tags, idempotency records | Local mutation source of truth |
| `result.json` | Terminal status, decision, usage, write counts | Created on completion/failure |

Evaluation adds `report.json` above the per-case run directories. Composed runs additionally write `components.jsonl` and `composition.json`, with per-hook hashes/calls and explicit `student` or `completed` provenance. Composed checkpoints bind the component source/profile and selected-context limit on resume. See [Lab 11](../content/labs/11-complete-student-harness.md) for the complete gate, deliberate failures, and artifact interpretation.

The trace uses real UTC timestamps; virtual latency is a deterministic accounting dimension. Run IDs and timestamps vary; expected outcomes do not.

## What the gate actually measures

There are **28 synthetic cases: 18 training and 10 holdout**, with distinct ticket IDs. Each case checks terminal status, decision action, category, exact expected citation set, draft count, required reply phrases, forbidden reply phrases, and mutation bounds. All eight checks must pass for a case to pass. Eleven additional scenarios verify failure handling and recovery.

The gate exits nonzero if any case or scenario fails. An agent that escalates every ticket cannot pass: useful successful drafts are required as well as safe escalation.

This is deliberately a small, closed-world acceptance suite. It does not measure complete semantic correctness, generalization to real customer language, real-model intelligence, actual token billing, provider latency, or comprehensive resistance to prompt injection. The holdout is visible on disk and protected by your learning discipline, not a technical barrier.

## Limits worth understanding

- The mock policy recognizes a finite list of suspicious patterns. Its regexes are examples, not an injection-defense guarantee.
- The tool boundary rejects unknown tools, wrong argument shapes, cross-ticket access, unapproved tags, and unretrieved citations independently of policy decisions.
- Citation presence proves an identifier came from retrieval. It does not prove every sentence follows from its source.
- `max_context_chars` measures serialized characters across tool observations, not tokens or the active context-window size. It is cumulative exposure accounting.
- Virtual milliseconds model costs deterministically. They do not interrupt a blocked network request or enforce a real deadline.
- Atomic JSON replacement supports these single-process crash/replay experiments. This store is not concurrent, distributed, authenticated, or designed for power-loss durability guarantees.
- Checkpoint checksums detect accidental corruption. They do not authenticate files against a malicious local editor.
- Stores and traces are bound to a run ID, and store ticket scope is checked before dispatch. Accidentally swapping another run's files is rejected.
- The deliberate crash occurs after a durable effect and before advancing the orchestrator's phase. It is a controlled simulation, not a process-kill chaos test.
- Local Python code, including student extensions, runs with your normal Python permissions. The tool allowlist is not an operating-system sandbox.
- A failing tag operation can follow a successful draft write. Always inspect effects and status separately.
- A mutation can commit before its response exceeds the context budget. A `mutation_committed` event records this boundary even if the later response is rejected.

For a hands-on model experiment, follow [model-bridge.md](model-bridge.md). For a live transport extension plan, read [provider-adapter-design.md](provider-adapter-design.md). For dataset stewardship, read [data/README.md](data/README.md).
