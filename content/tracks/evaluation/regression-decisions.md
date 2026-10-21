# Decide whether an AI change is actually an improvement

## Start here

Read the dataset, grader, and adversarial-testing topics first. You should understand a test case, a rubric, and a baseline: the existing version against which a candidate change is compared. No statistics package or paid evaluation service is needed. Open your existing assistant and use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) if you need help pasting the example.

The goal is a defensible release decision. A higher average score is useful evidence, but it is not automatically permission to ship a change.

## The idea in plain language

A **regression** is behavior that worked acceptably before a change and now fails. A **paired comparison** tests the old and new versions on the same cases, preserving each case's result. That lets you see gains and losses hidden by the overall average.

A **slice** is a meaningful subset, such as a language, ticket category, or permission boundary. Slice results expose uneven changes. A **holdout** is a set kept out of tuning decisions until a planned assessment. Repeatedly looking at its failures and tuning for them turns it into development data. Renaming it “holdout” does not restore independence.

For AI systems, version more than the prompt: record the model identifier, retrieval snapshot, tool definitions, policy configuration, grader, and relevant parameters. A changed judge can change the score without changing the answers. Repeated runs help reveal variation, but ten repeats of one ticket are not ten independent examples of customer needs.

## A small example

Signal Desk compares two synthetic routing prompts on the same 100 tickets. The baseline passes 88 cases. The candidate passes 92. Per-case comparison finds seven newly passing tickets and three newly failing tickets. Those counts reconcile: 88 + 7 - 3 = 92.

All three new failures disclose a restricted queue name. A rule established before testing says any such disclosure blocks release. The candidate therefore fails the release rule despite its better total. This is a teaching decision for a fictional system; real thresholds must match the product's consequences and review process.

The candidate also improves English tickets but worsens a tiny Polish slice from 4/5 to 3/5. One case has a large percentage effect in such a small sample. You should investigate the loss and gather representative evidence, not claim a precise population-wide difference from five tickets.

## Try it with Codex or Claude Code

```text
Walk me through a release comparison using these synthetic counts.
Baseline: 88/100 pass. Candidate: 92/100 pass on the same cases.
Seven cases improved and three regressed. All three regressions reveal
a restricted queue name. A predeclared rule blocks any such disclosure.
Polish slice: baseline 4/5, candidate 3/5.
Explain the arithmetic, the release rule, and the limits of the small slice.
Then explain what to freeze before a repeat and what evidence is still
missing. Do not invent a confidence interval, execute an eval, or publish.
Use plain language and distinguish observed facts from assumptions.
```

Inspect its arithmetic and release interpretation. A response that argues for release solely because 92 exceeds 88 has missed the purpose of the exercise. A response claiming the candidate is worse for every Polish user also exceeds the supplied evidence.

## What you should see

You should see separate decisions about quality gains, unacceptable regressions, uncertainty, and further investigation. Keep infrastructure failures visible: a timeout is an outcome unless the evaluation protocol explicitly distinguishes it. Excluding all failed runs from the denominator can make an unreliable candidate look excellent.

When you later automate this, preserve original responses and individual judgments so a changed rubric can be reviewed. Synthetic fixtures are useful for deterministic boundaries; they do not establish real-user coverage. A gated offline result also does not replace a measured rollout.

## If it goes wrong

If versions were tested on different cases, repeat them on a common frozen set before interpreting the difference. If cases are near-duplicates, group related tickets before splitting development and holdout data. If labels conflict, resolve the rubric with a reviewer before blaming the model.

If a grader is unavailable, mark its result missing and follow a declared rule. Do not quietly substitute a different model judge and compare its score as though nothing changed. If the model or API cannot be pinned fully, record the available identity and date and state that reproducibility is limited.

## Go deeper

Read scikit-learn's [Common pitfalls — Data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage), through How to avoid data leakage; stop before the feature-selection code example. Public reading requires no account. The page discusses model training, while this lesson applies the same separation principle to prompt and workflow tuning; that application is a design inference, not a claim that the library manages your LLM evaluation.

The [evaluation plan template](../../../templates/evaluation-plan.md) is an optional memory aid. Continue to [service reliability](../../how-to/22.md) when you want to connect offline evidence to production decisions.

## Optional practice

Ask your tutor for a new paired-result table with one important regression and a different release rule. State your decision and remaining uncertainty before requesting feedback. A short spoken or typed answer is sufficient; a report is optional.
