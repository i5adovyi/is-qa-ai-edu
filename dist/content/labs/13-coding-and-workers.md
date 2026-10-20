# Lab 13 — Deliver a coding change and coordinate real workers

Allow 2–4 hours across both parts. **Part A** requires lessons 10–12, Python 3.9+ and Git, so it can begin in week 5. **Part B** additionally requires lessons 19–21 and belongs after week 8's delegation work. You do not need the delegation lessons to start Part A. The scripted worker path has no additional dependency or account requirement. The optional AI-worker path requires an installed, authenticated Codex CLI and model access. Outputs are fictional and local.

## Part A: a reproducible coding-agent mission

Create a disposable repository from the supplied defect:

```sh
python3 -m lab.practicum.coding init --out work/coding-mission
python3 -m lab.practicum.coding check --out work/coding-mission
```

Initialization exits zero and saves the deliberately failing baseline. The second command exits **1** until you repair the defect. Open `baseline.json`, `router.py`, `test_router.py`, and `AGENTS.md` in that new repository. There are five tests and one seeded boundary failure. This does not alter the course reference.

Write a three-case acceptance brief before using an assistant. Open a fresh coding-assistant session rooted in `work/coding-mission`, give it the brief, and request a reproduction, narrow patch, and actual test evidence. If no assistant is available, perform the same work yourself and label the route manual.

Use the existing test command to check the patch:

```sh
python3 -m lab.practicum.coding check --out work/coding-mission
git -C work/coding-mission diff --check
git -C work/coding-mission diff
```

Inspect the tests as well as the implementation. A passing check achieved by deleting the failing assertion is not an acceptable repair. Save the first failure and the final `check.json`. Commit only after reviewing:

```sh
git -C work/coding-mission add router.py
git -C work/coding-mission commit -m "Fix reproduced step-budget boundary"
```

Write `handoff.md` with the current commit, observed test result, affected behavior, and next action. Start another fresh session with that file and the repository. Ask it to verify the claim against the current files. The check report is an observation, not permission to skip verification.

Rehearse undoing the change on a separate branch:

```sh
git -C work/coding-mission switch -c rollback-rehearsal
git -C work/coding-mission revert --no-edit HEAD
python3 -m lab.practicum.coding check --out work/coding-mission
git -C work/coding-mission switch practice
python3 -m lab.practicum.coding check --out work/coding-mission
```

The reverted branch should reproduce the original failure. Returning to `practice` should restore the passing repair. Keep your working tree clean before switching branches. These commands operate only on this disposable repository.

For an instruction experiment, create fresh mission directories. Initialization includes `AGENTS.md`, so **move that generated file outside the first disposable repository before opening its assistant session**; that condition uses only your task brief. Keep `AGENTS.md` in the second condition. In the third, keep the same instructions and additionally invoke the installed review skill from Lab 10 on an appropriate evidence packet. Use the same defect and acceptance criteria. Record which file the host actually loaded and what changed.

For a fourth condition, keep the second condition's instructions and change one supported per-session tool permission, such as making command execution unavailable. Predict which verification step becomes impossible, then distinguish a proposed check from an executed check in the result. Keep the model and input files fixed. A skill's prose is not a tool configuration, and these conditions do not isolate a cause if you change all three together. Do not change global settings for this exercise.

**Gate:** original failure, scoped patch, unchanged relevant assertions, passing result, reviewed commit, fresh-session verification, and successful revert/restore rehearsal. Preserve the distinction between manual and AI-assisted execution.

## Part B: two independently running workers

Predict whether parallelism will help this small task, then run:

```sh
python3 -m lab.practicum.workers --out work/workers-scripted --cases 8
```

This launches real separate Python subprocesses. It is labeled **scripted**, not AI. For each of eight synthetic cases, one worker performs the baseline; the team runs evidence and completeness workers concurrently. Each receives a separate directory and an explicit input hash. Only the parent writes the integrated report.

Separate directories make ownership inspectable; they are not a security boundary against a malicious Python process. The optional host also uses its read-only mode and disables tools. This classroom wrapper is not an operating-system isolation system.

Inspect `case-1/single/`, `case-1/evidence/`, `case-1/completeness/`, and the top-level `report.json`. The report separates wall time, summed worker time, parent integration time, quality, and eight coordination fault checks. The worker assignment removes policy text from the completeness checker because its requirements do not depend on the export limit.

`parent_integration_seconds` measures the automated merge function, not all supervision. Record your own assignment design, review, and repair minutes separately; include those minutes and every worker's reported usage when deciding whether the team was worthwhile. Do not compare the fastest worker alone with the complete single-worker run.

Then optionally repeat one case using actual models:

```sh
python3 -m lab.practicum.workers --out work/workers-live --mode codex --cases 1
```

If `codex` is not on PATH, add `--codex` followed by its actual executable path. For a reproducible model comparison, supply `--model` with an identifier available to your account. Without it, `model_identity_source` records that the host's default identity was not exposed. The wrapper uses fresh ephemeral sessions, bounded subprocess timeouts, structured output, read-only host mode, and disabled shell/web/plugin tools. It captures reported usage when available and does not infer dollar cost.

Three model requests are made for one case: baseline, evidence, and completeness. `--cases 8` makes 24 requests. A timeout stops the experiment, preserves partial artifacts and records `interruption.json`; it does not claim a passing result. Use a new output directory for another trial.

**Gate:** eight scripted case comparisons pass, including stale input, duplicate completion, missing worker, cancelled work, partial output, fabricated citation, and conflicting duplicate rejection. For a live gate, preserve actual host events and model-produced results. One live case proves an integration path, not a performance advantage.

## Change one condition

Copy the packet-producing function into an isolated experiment or author your own packets. Change the policy limit, then inspect which assignment hash changes. Predict why the completeness result can be reused when its complete input set is unchanged. Deliver an old policy result after a new assignment and show that integration rejects it.

Author four additional cases with source conflicts and an explicit applicability rule. Run both architectures on identical inputs and record how you adjudicated conflicts. Keep the original eight cases as a reproducible reference.

## Submission

Submit the coding mission evidence, eight paired worker results, one live result if attempted, a failed coordination trace, and a decision about whether the team justified its extra effort. Explain what the runtime enforced versus what the model merely proposed. A no-delegation decision supported by measurements is valid.

[Practice map](../../docs/PRACTICE-MAP.md) · [Worker implementation](../../lab/practicum/workers.py)
