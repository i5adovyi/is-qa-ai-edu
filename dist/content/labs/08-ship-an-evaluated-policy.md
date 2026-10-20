# Lab 08 — Ship a policy with evidence

**Outcome:** replace the bounded decision function, pass usefulness and safety gates, and produce a reviewable release note. Suggested time: 90–150 minutes.

## The problem

You now have data handling, context selection, permissions, budgets, recovery, citations, and traces. This exercise connects a student policy to the harness while preserving those boundaries. Its `--policy student` command substitutes only the decision function. Continue with [Lab 11](11-complete-student-harness.md) to wire all eight student functions into the complete harness and prove every seam is active.

This is still a deterministic offline policy. After completing it, use the working [manual model bridge](../../lab/model-bridge.md) to export a request, ask any chat model for a JSON decision, and replay its answer through the same harness. No API key is needed; a labeled mock response also works offline. A live provider integration is a further extension described in the [adapter design brief](../../lab/provider-adapter-design.md).

## Build

Implement `build_decision(ticket, articles)` in `lab/student.py`.

You may use `classify` from `lab.policy`. Focus on how a decision uses evidence:

- Escalate `safety` and `unknown` categories.
- Select only articles whose topic matches the classified category.
- Escalate when relevant evidence is absent or ambiguous.
- For exactly one relevant approved article, return its answer as the draft and cite its ID.
- Return the exact decision contract: `action`, `category`, `reply`, `citations`, `reason`.
- Escalations use an empty reply and citation list.

Keep the operational reason concise. Do not ask an agent for hidden chain-of-thought; the application needs a brief explanation of the chosen action and evidence.

## Iterate on training

```sh
python3 -m lab.cli practice --lab 08
python3 -m lab.cli evaluate --policy student --split train --out .lab-runs/lab08-train-v1
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The public practice checks must pass. The student training gate should pass 18 ticket cases and 11 scenarios. Use a new output directory for every evaluation to preserve previous reports.

If a case fails, inspect its `result.json` and trace. Categorize the failure before editing: schema, classification, missing evidence, incorrect citation, unsupported claim, tool permission, budget, or recovery. Change one cause at a time.

## Freeze and evaluate

Before the holdout run, record:

- Your implementation version or commit.
- The exact change and expected benefit.
- Training score and known weaknesses.
- Which files and settings are frozen.
- Your pass/fail criterion.

Then run:

```sh
python3 -m lab.cli evaluate --policy student --split holdout --out .lab-runs/lab08-holdout-v1
```

The standard gate requires **10/10 holdout cases and 11/11 scenarios**. Preserve the report even if it fails. Once you use holdout details to tune code, those cases become development data for your next iteration.

## A meaningful regression

Temporarily change your policy so every ticket escalates. Predict which metrics will fall, run the training gate into a new directory, and confirm it exits nonzero. Restore your implementation.

Then temporarily cite an unknown article for one supported case. Confirm the output validator prevents saving a draft. Restore your implementation and rerun the affected checks. These experiments prove the gates can detect plausible failures; a permanently green dashboard alone does not.

## Portfolio review

Produce a release note with:

1. Problem and new behavior.
2. Trust boundary: what the policy proposes and what the dispatcher authorizes.
3. Training and holdout results with exact report locations.
4. A failure example caught by the gate.
5. Recovery evidence showing one write after replay.
6. Limitations: synthetic data, finite rules, substring checks, and no real-model evaluation.
7. Your next experiment and the evidence required to justify it.

A reviewer should reproduce your result with Python alone. Do not claim this proves production readiness or a commercial valuation.

## Stretch capstone

Choose one:

- Add version-aware evidence selection and conflict escalation.
- Create 20 new cases authored before changing the policy.
- Add a fake provider transport with malformed responses and deadlines.
- Replace JSON storage with a transactional local database and test concurrent replays.

Specify the smallest behavior change, its acceptance cases, and its failure modes before implementing it.

[Hints](hints/08.md) · [Solution discussion](solutions/README.md#lab-08) · [Lab index](README.md)
