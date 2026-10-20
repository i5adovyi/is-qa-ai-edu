# Lab 11 — Compose and prove your complete harness

**Outcome:** run all eight student functions inside one checkpointed application, then prove each function changes real behavior. Suggested time: 2–4 hours after Labs 01–08. Requirements: Python 3.9+; no packages, model access, credentials, or network.

This lab closes the gap between eight passing helper functions and an integrated system. `python3 -m lab.composed` reads **all eight functions** from `lab/student.py` when `--components student` is selected. It never fills an unfinished function with the reference implementation. The separate `completed` profile is an instructor example copied from the disclosed solutions. It helps you inspect wiring; its green result is not your completion certificate.

The ordinary `python3 -m lab.cli evaluate` still evaluates the reference harness. `lab.cli evaluate --policy student` substitutes only Lab 08's decision. Neither command proves that Labs 01–07 are connected. This lab has its own composition command and evidence.

## 1. Locate the eight real seams

Read `lab/composed.py`, then follow one normal run through `lab/engine.py`.

| Student function | Where its return value is used | Independent host boundary |
|---|---|---|
| `redact_sensitive` | Ticket subject/body before classification and decision | Rejects remaining teaching-format email/demo keys; local raw fixture store stays unchanged |
| `pack_context` | Chooses retrieved article IDs actually passed to the decision | IDs must come from retrieval, be unique, fit the selected answer-character budget, and retain any known competing answers |
| `tool_allowed` | Permits or rejects the initial ticket read | Dispatcher still enforces schema, allowlist, and ticket scope |
| `retry_delay_ms` | Delay charged before the one permitted timeout retry | Integer within cap; virtual time budget may reject the retry |
| `operation_key` | Key used by actual draft and tag mutations, including replay | Store rejects conflicting payloads and persists effect/deduplication atomically |
| `citations_valid` | Approves or rejects a proposed draft before saving | Decision validator and dispatcher still require relevant retrieved citations |
| `summarize_trace` | Produces terminal diagnostic summary saved in composition evidence | Counts compared with recorded events; bad summary fails the run even after a prior write |
| `build_decision` | Chooses draft or escalation from the redacted ticket and selected evidence | Strict decision schema, tool permissions, approvals, and mutation limits remain in force |

Lab 03's contract is intentionally **read-only**: its function gates `read_ticket`. It is not a general dispatcher and does not authorize retrieval, drafts, or tags. Those tools retain their existing mandatory host checks. An implementation that always returns `True` cannot grant broader authority, and it fails the Lab 03 helper gate.

Two context budgets have distinct purposes. The engine's cumulative `max_context_chars` charges serialized tool outputs **before** the learner selector sees them. `--context-chars` caps the sum of selected article answer lengths. It does not erase already consumed tool output, count tokens, or limit arbitrary Python execution.

## 2. Inspect the disclosed working example

Use a fresh output directory each time:

```sh
python3 -m lab.composed run --components completed --case train-01 --out .lab-runs/composed-example
python3 -m lab.composed evaluate --components completed --split all \
  --out .lab-runs/composed-example-gate
```

Expected gate: **28/28 cases, 11/11 scenarios, 3/3 integration probes, all eight hook coverage values true**, and exit `0`. The three probes add teaching-format sensitive text to a ticket, force a zero-character evidence selection, and retrieve conflicting answers under a tight packing budget. They verify redaction reaches the policy boundary, context selection can change a draft into escalation, and packing cannot hide a known conflict to manufacture a draft. These probes supplement the eight helper acceptance gates and all existing behavioral/failure scenarios.

Inspect these files in one run directory:

| Artifact | What to inspect |
|---|---|
| `components.jsonl` | Each component call/return or failure, input/output hashes, selected evidence IDs |
| `composition.json` | Profile/source fingerprint, call counts, diagnostic summary, result status, provenance |
| `checkpoint.json` | Same component binding, pending phase, consumed budgets, selected observations |
| `trace.jsonl` | Tool attempts, rejections, retry delay, mutation/replay, terminal outcome |
| `store.json` | Actual local draft/tag effects and idempotency records |
| `result.json` | Terminal result, including writes that happened before a later failure |

The gate's parent `report.json` combines helper checks, case/scenario results, probe outcomes, and aggregate hook coverage. `completed` must appear in the example's provenance. A passing reference report has no equivalent composition evidence and cannot satisfy this lab's deliverable.

Trace metadata and component evidence contain hashes rather than full ticket text. Hashes are comparison evidence, not encryption. The local synthetic source store still contains the original fixture; redaction protects what reaches the policy, not every file on disk.

## 3. Run your implementations

Complete Labs 01–08 in `lab/student.py`; keep your own code. Run the helper checks while iterating, then the integrated training gate:

```sh
python3 -m lab.cli practice --lab 01
python3 -m lab.cli practice --lab 08
python3 -m lab.composed evaluate --components student --split train \
  --out .lab-runs/composed-student-train-v1
```

Run each numbered helper check, not only 01 and 08 shown above. An untouched student module must fail: expected exit `1`, no reference fallback, and unfinished helpers identified in `report.json`. A correctly implemented training composition passes **18 cases, 11 scenarios, three probes, and eight helper gates**. If a helper raises an exception, component evidence records its name and exception type without copying the input text into the event.

Diagnose the earliest failing seam before changing the policy. A zero-length context selection can cause a valid escalation; a malformed selection is a component error; hiding one of multiple competing retrieved answers fails with `component_context_ambiguity` before the decision; an overly strict citation helper can block a perfectly valid draft. These have different causes even when no draft is saved.

## 4. Prove your wiring with controlled failures

Before each experiment, predict the outcome. Change one student function, run into a new directory, save evidence, and restore the correct implementation.

1. Return the input unchanged from the redactor. The sensitive-text probe fails before a decision/write; ordinary tickets without those formats may still pass.
2. Return an empty selection from `pack_context`. Supported tickets escalate instead of drafting, so useful-work acceptance fails. Returning an invented ID is rejected earlier.
3. Return `False` from `tool_allowed`. The ticket read is denied before a dispatcher attempt. Explain why other tool permissions do not move into this function.
4. Return `401` from the retry helper. `timeout-once` fails the delay contract. Restore it, then inspect the `100` virtual milliseconds charged by the normal first retry.
5. Return the same key for every action. `approved-tag` saves its draft, then fails `idempotency_conflict` on the tag. A failed terminal state does not mean zero effects.
6. Return `False` from `citations_valid`. A valid draft is blocked. Return `True` and invent a citation in the policy: the independent host validator must still block it.
7. Return zero counts from `summarize_trace`. A normal draft may already exist, but diagnostic acceptance fails with `component_summary`.
8. Make every policy decision a valid escalation. Schema checks pass; useful-work evaluation fails. Safety includes completing authorized work correctly.

Automated regressions reproduce these boundaries:

```sh
python3 -m unittest discover -s tests -p 'test_composed_harness.py' -v
```

Do not leave deliberate regressions in your final student version. Include one failure trace and its explanation in your release evidence.

## 5. Crash, resume, and change identity

```sh
python3 -m lab.composed run --components completed --scenario crash-after-write \
  --out .lab-runs/composed-recovery
# The preceding command intentionally exits 3. Run the next separately.
python3 -m lab.composed resume .lab-runs/composed-recovery/checkpoint.json --components completed
```

Expected final effect: **one draft, one write**, a replay hit, and increased consumed usage. Repeat with your completed `student` profile after the example works.

Resume binds the profile, component source/function fingerprints, and selected-context limit. Trying `--components student` on the example checkpoint, changing a helper's source after a crash, or resuming with a different `--context-chars` is rejected with `component_mismatch` before dispatch. Preserve the original code to finish an old experiment or start a new run for changed code. Do not reset budgets to make a pending run pass.

Function fingerprints include Python bytecode metadata and can vary with the Python version or source location. Resume is intended in the same runtime and checkout. Imported dependency changes are not completely attested by this binding. The binding detects accidental mismatch, not malicious local editing. Checksums are not signatures, Python code executes with your user privileges, and neither hashing nor the dispatcher creates an operating-system sandbox. Virtual retry delay is accounting, not a real timed network retry.

## 6. Freeze, evaluate, and submit

Freeze your source before the final gate:

```sh
python3 -m lab.composed evaluate --components student --split holdout \
  --out .lab-runs/composed-student-holdout-v1
python3 -m lab.composed evaluate --components student --split all \
  --out .lab-runs/composed-student-release-v1
```

Final release criterion: **28 cases + 11 scenarios + 3 probes + 8 helper gates, all passed, all eight hooks exercised, student profile recorded**. The holdout is visible; using its failures to tune code converts it into development data. These are small synthetic acceptance cases, not measured model quality or proof of production security.

Submit your student source, `report.json`, a normal run's composition evidence, one deliberate regression with predicted versus observed behavior, a crash/replay packet, and a short diagram showing which checks are learner code versus mandatory host code. A reviewer must be able to reproduce the result and distinguish your implementation from the disclosed instructor example. If you used the example as scaffolding, say so explicitly and explain what you changed and independently tested.

[Lab index](README.md) · [Harness manual](../../lab/README.md) · [Manual model bridge](../../lab/model-bridge.md)
