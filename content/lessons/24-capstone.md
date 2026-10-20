# 24 · Build and defend your Signal Desk capstone

Stage 8 · 240 minutes · Advanced

Integrate the course into a portfolio-grade system and defend its design with a live failure drill and reproducible evidence.

## What you will be able to do

- Deliver an end-to-end bounded agent system with evidence.
- Demonstrate recovery, evaluation and adversarial behavior.
- Defend tradeoffs and define the next justified improvement.

## The assignment

Your capstone is a Signal Desk assistant that turns synthetic tickets into useful, evidence-backed local drafts or explicit review outcomes. It must retrieve relevant knowledge, preserve provenance, validate proposed actions, record traces, respect budgets and recover from interruption. A real model is optional. A deterministic planner proves the harness mechanics; a live model extension tests language behavior and must be evaluated separately.

The system should be understandable to another engineer. Provide a quickstart, architecture diagram, task contract, tool contracts, evaluation dataset, results and operating runbook. Include a short decision record explaining one feature you deliberately did not build. A portfolio becomes credible when its boundaries and evidence are clear, not when it claims universal autonomy.

Use the bundled lab as a starting point, then add one meaningful capability. Examples include policy-version conflict handling, better retrieval for SSO cases, a stricter evidence-scope validator or a selective multi-agent review path. Choose a change with an observable baseline failure. The capstone is not complete merely because the unmodified demo runs; your improvement must have a before/after result and a reviewable implementation or rigorous design simulation.

## Worked defense structure

A ten-minute demonstration can follow this sequence:

```text
Minute 0–2: user problem, task contract and baseline failure.
Minute 2–4: successful ticket with visible evidence and local draft.
Minute 4–6: malicious input blocked at the execution boundary.
Minute 6–8: interruption and resume without duplicate work.
Minute 8–10: evaluation results, limitations and next decision.
```

Show actual artifacts instead of narrating hypothetical behavior. If a feature is simulated, label it while demonstrating it. If an optional model call fails or requires an unavailable subscription, the offline path should still let a reviewer inspect the architecture and deterministic checks.

## Exercise 1 · Guided capstone proposal

Write a one-page proposal with target user, supported cases, baseline defect, chosen improvement, architecture and acceptance criteria. Select twelve evaluation cases spanning ordinary, ambiguous, adversarial and recovery scenarios. Define critical gates before implementation. Record your available time and choose a scope you can finish and verify.

**Deliverable:** proposal and frozen evaluation plan. **Pass:** the improvement addresses an observed need; the plan contains negative cases and a recovery drill; success is observable without trusting a narrative.

## Exercise 2 · Build the complete evidence package

Implement the improvement and assemble a reproducible package. Include exact setup and run commands, a sample successful trace, a failed trace, a checkpoint, evaluation results and a review note. Run `python3 -m lab.cli demo`, `python3 -m lab.cli evaluate --split holdout` and the relevant tests when using the bundled implementation. Adapt additional commands to your actual extension.

**Deliverable:** working project plus evidence folder. **Pass:** a fresh reviewer can reproduce the main path; every reported metric identifies dataset and rubric versions; the project contains no required paid API dependency for the core demonstration.

## Exercise 3 · Adversarial defense

Ask a peer to choose one unseen ticket, one malformed tool response and one crash point. If working alone, prepare these before the final run and keep them out of development. Demonstrate the resulting behavior, then explain any failure without editing the evidence. Propose a bounded repair and show which acceptance case would verify it.

**Deliverable:** defense recording or transcript and a repair plan. **Pass:** no hidden manual correction; uncertainty and incomplete work are reported honestly; the system remains bounded when the planner behaves badly.

## Assessment rubric

Score five dimensions from zero to four: task usefulness, evidence quality, harness reliability, evaluation rigor and reproducibility. Zero means absent; one means described only; two means demonstrated on the happy path; three means tested on relevant failure cases; four means reproducible evidence plus a clear account of limitations. A course pass requires at least fifteen of twenty, no zero, and no critical authority-boundary failure in the declared suite. This is a learning rubric, not an accredited certification or a production guarantee.

## Hints and solution outline

A strong solution uses a narrow tool set, an explicit state machine, source-aware drafts and a durable operation ledger. It keeps the model adapter separate from orchestration, so scripted fault injection remains available. Its evaluation report includes regressions and unresolved cases. Its demo makes the failure boundary visible. Its README tells a reviewer where to start and how to reproduce the evidence. Do fewer things well if necessary; an honest bounded system is a stronger artifact than a sprawling unverified claim.

## Reflection and next step

What can your system now do that your baseline could not? Which result is supported most strongly, and which is still speculative? Write the next experiment you would fund, the decision it would inform and the evidence that would make you abandon that direction.

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Google SRE book: Service-level objectives](https://sre.google/sre-book/service-level-objectives/)
