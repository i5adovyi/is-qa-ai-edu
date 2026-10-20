# 16 · Build an evaluation set that reflects the job

Stage 6 · 115 minutes · Advanced

Create a versioned benchmark with meaningful coverage, defensible labels and explicit limits.

## What you will be able to do

- Design cases around risks and real decision boundaries.
- Separate dataset splits and preserve label provenance.
- Handle ambiguous cases without manufacturing certainty.

## The idea

An evaluation dataset is a model of the work you care about. If it contains only easy, well-phrased tickets, a high score says little about incomplete evidence, contradictory reports or tool failures. Begin with a task taxonomy and failure taxonomy. Signal Desk needs categories such as access, billing and export issues, but it also needs dimensions such as missing facts, stale policy, malicious text and unsupported action claims.

Construct cases by crossing important dimensions selectively. You do not need every possible combination. Include representative normal cases, known difficult boundaries and severe failures that must be blocked. Keep the source of each case: synthetic authoring, sanitized incident, or transformed development example. The course uses synthetic data; do not imply its distribution matches a real support queue.

Labels should describe acceptable behavior, not just one preferred sentence. A case can require a category, supporting evidence, a missing-information question and a forbidden claim. For ambiguous cases, allow multiple acceptable outcomes if each is justified. If experts disagree because policy is unclear, fix the policy or preserve the ambiguity. Averaging disagreement does not create a valid ground truth.

Use development cases for improvement and a held-out split for a final comparison. Keep adversarial tests separately visible so strong average performance cannot hide a severe boundary failure. Version the dataset and rubric together. If expected behavior changes, record the reason and review which historical comparisons remain meaningful.

## Worked example

A useful case record for SD-116 might contain:

```text
Input: customer reports duplicate charge; settlement status absent.
Available evidence: billing policy requires settlement verification.
Required: billing route; request or review settlement status.
Forbidden: claim refund completed; assert duplicate settlement confirmed.
Acceptable variations: ask for invoice IDs or route to billing review.
Tags: missing-evidence, billing, action-claim.
Provenance: synthetic; label reviewed against policy v2.
```

This record tests the behavior that matters without requiring an exact draft. It also states why the label exists. A future policy change can be traced to the affected cases.

## Optional starter practice

Before inventing your own cases, use the [lesson 16 starter pack](../practice/lesson-16-starter.json) and [fixture workflow](../practice/README.md). Label one or two cases yourself before deliberately opening a separate key. These are warm-up examples; complete the original exercises below with new learner-authored cases. Supplied practice examples are not untouched evaluation evidence.

## Exercise 1 · Guided coverage matrix

Create a matrix with five ticket topics and six failure dimensions. Select twelve cells to cover first, explaining the selection. Include at least two normal cases, two ambiguous cases, two malicious-input cases and two tool-failure cases. Identify one important real-world dimension your synthetic set cannot represent well.

**Deliverable:** coverage matrix and case plan. **Pass:** selection is driven by user impact and observed failure modes, not merely easy-to-write examples.

## Exercise 2 · Build a versioned dataset

Author twelve complete cases with input, evidence, expected behavior, forbidden behavior, tags and provenance. Split eight for development and four for held-out evaluation before tuning. Ask a reviewer to label four cases independently, or relabel them after a delay without consulting your first answers. Resolve disagreements explicitly.

**Deliverable:** dataset v1, rubric and disagreement log. **Pass:** labels are supported by policy; ambiguous cases are represented honestly; split membership is stable and visible.

## Exercise 3 · Adversarial contamination

Place one held-out answer inside a prompt example and another inside a knowledge note. Explain how this contaminates the evaluation. Create paraphrases of a development ticket that preserve its facts and compare behavior. Decide whether the paraphrases are truly independent held-out examples or a robustness family related to the original case.

**Deliverable:** contamination audit and repaired split. **Pass:** leaked cases are removed from claims of unseen performance, and related variants are documented rather than counted as wholly independent evidence.

## Hints and solution outline

A simple JSONL file works well because each line can contain one independently reviewable case. Give cases stable IDs and keep expected outputs separate from runtime inputs. The evaluator may read labels; the system under test should receive only the ticket and allowed evidence. Report the synthetic nature and sample size with results. Use the bundled `python3 -m lab.cli evaluate --split holdout` as an example of split-aware evaluation, after inspecting what it measures.

## Reflection

Which real failure would your dataset currently miss? How could the system score highly while remaining unhelpful? What event should cause a dataset version change instead of a quiet label edit?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
