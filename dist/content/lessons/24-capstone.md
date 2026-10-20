# 24 · Choose, build and defend your capstone

Stage 8 · 90-minute proposal clinic, then 10–20 project hours · Advanced

Integrate the course into a portfolio-grade system and defend its design with a live failure drill and reproducible evidence.

## What you will be able to do

- Deliver one of three bounded AI workflow projects with evidence.
- Demonstrate evaluation, adversarial behavior and appropriate recovery.
- Defend tradeoffs and define the next justified improvement.

## The assignment

Choose one project:

- [Support agent](../../capstones/01-support-agent.md): turn synthetic tickets into evidence-backed drafts; demonstrate tool boundaries, budgets and interrupted-write recovery.
- [QA review copilot](../../capstones/02-qa-copilot.md): review specifications and patches; expose seeded defects and distinguish proposed tests from executed tests.
- [Research workflow](../../capstones/03-research-workflow.md): produce a decision memo with claim-level evidence, source-conflict handling and verifiable handoffs.

All three use the shared assessment below. Follow your chosen brief's required checks rather than building all three products. A real model is optional by access: the [model bridge](../../lab/model-bridge.md) provides a separate route for capturing and evaluating model output. A deterministic implementation or design simulation can establish only the behavior it actually exercises. Label those results separately from live-model evidence.

The system should be understandable to another engineer. Provide a quickstart, architecture diagram, task contract, tool contracts, evaluation dataset, results and operating runbook. Include a short decision record explaining one feature you deliberately did not build. A portfolio becomes credible when its boundaries and evidence are clear, not when it claims universal autonomy.

Use the bundled support lab when it fits your chosen project. For QA and research, use an isolated project directory and the brief's fixtures or input contract. Add one meaningful capability with an observable baseline failure: policy-version conflict handling, detection of an actual retry defect, or rejection of a real but irrelevant citation. The capstone is not complete merely because the unmodified demo runs; your improvement must have a before/after result and a reviewable implementation or rigorous design simulation.

Spend this lesson's 90-minute clinic choosing the project and completing exercise 1. Exercises 2 and 3 are the project build and defense, scheduled across weeks 10–12. Budget approximately 10–20 focused hours according to the selected brief. The clinic estimate does not include that build time.

## Worked defense structure

A ten-minute demonstration can follow this sequence:

```text
Minute 0–2: user problem, task contract and baseline failure.
Minute 2–4: successful user journey with visible evidence.
Minute 4–6: adversarial or misleading input handled at its enforcing boundary.
Minute 6–8: interruption or stale handoff reconciled against saved artifacts.
Minute 8–10: evaluation results, limitations and next decision.
```

Show actual artifacts instead of narrating hypothetical behavior. If a feature is simulated, label it while demonstrating it. If an optional model call fails or requires an unavailable subscription, the offline path should still let a reviewer inspect the architecture and deterministic checks.

## Exercise 1 · Guided capstone proposal

Write a one-page proposal naming your selected capstone, target user, supported cases, baseline defect, chosen improvement, architecture and acceptance criteria. Select an initial twelve-case evaluation plan spanning ordinary, ambiguous, adversarial and recovery scenarios, then satisfy any larger dataset requirement in your chosen brief. For research, a recovery case can be an interrupted evidence ledger or stale handoff; for QA, it can be interrupted execution with no passing result recorded. Define critical gates before implementation. Record your available time and choose a scope you can finish and verify.

**Deliverable:** proposal and frozen evaluation plan. **Pass:** the improvement addresses an observed need; the plan contains negative cases and a recovery drill; success is observable without trusting a narrative.

## Exercise 2 · Build the complete evidence package

Implement the improvement and assemble a reproducible package. Include exact setup and run commands, successful and failed execution evidence, saved resumption state, evaluation results and a review note. If extending the support lab through `lab/student.py`, run `python3 -m lab.cli evaluate --policy student --split train`, freeze the candidate, then run `python3 -m lab.cli evaluate --policy student --split holdout` and relevant tests. The command without `--policy student` evaluates the reference policy and cannot prove that a student change works. For other implementations, provide commands that actually exercise your candidate and selected cases.

**Deliverable:** working project plus evidence folder. **Pass:** a fresh reviewer can reproduce the main path; every reported metric identifies dataset and rubric versions; the project contains no required paid API dependency for the core demonstration.

## Exercise 3 · Adversarial defense

Ask a peer to choose one unseen input, one misleading or malformed external result, and one interruption point appropriate to your project. If working alone, prepare these before the final run and keep them out of development. Demonstrate the resulting behavior, then explain any failure without editing the evidence. Propose a bounded repair and show which acceptance case would verify it.

**Deliverable:** defense recording or transcript and a repair plan. **Pass:** no hidden manual correction; uncertainty and incomplete work are reported honestly; the system remains bounded when the planner behaves badly.

## Assessment rubric

Use the single [40-point capstone rubric](../../docs/ASSESSMENT.md#capstone-scoring): ten dimensions, each scored 0–4. Suggested pass is **30/40, every dimension at least 2, and no unauthorized side effects** in the declared suite. Preserve the evidence supporting each score. The 20-point common rubric applies to stage submissions; it is not a second capstone standard. This is a learning rubric, not an accredited certification or a production guarantee.

## Hints and solution outline

A strong solution preserves its project's boundaries. Support work needs source-aware drafts and a durable operation ledger; QA work needs requirement-to-test evidence and truthful execution status; research needs claim-to-source support and unresolved-conflict handling. Keep any model adapter separate from orchestration so scripted fault injection remains available. Include regressions and unresolved cases in the evaluation report. The demo should expose one failure boundary, and the README should tell a reviewer how to reproduce it.

## Reflection and next step

What can your system now do that your baseline could not? Which result is supported most strongly, and which is still speculative? Write the next experiment you would fund, the decision it would inform and the evidence that would make you abandon that direction.

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Google SRE book: Service-level objectives](https://sre.google/sre-book/service-level-objectives/)
