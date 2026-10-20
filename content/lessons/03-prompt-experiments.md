# 03 · Run prompt experiments without fooling yourself

Stage 1 · 110 minutes · Foundation

Use controlled comparisons to discover whether a prompt revision improves Signal Desk rather than merely looking better.

## What you will be able to do

- Separate development cases from held-out cases.
- Compare prompts using a fixed rubric and paired cases.
- Record uncertainty and avoid premature performance claims.

## The idea

Prompt work becomes engineering when you can tell whether a change helped. Start with a hypothesis: “Adding a missing-facts field will reduce unsupported diagnoses.” Then choose a measure that tests that claim. A prettier response is not evidence of fewer unsupported diagnoses. A single successful demonstration is not evidence of reliability.

Create a development set for revision and a held-out set for the final comparison. If you repeatedly inspect the held-out answers and tune against them, those cases have become development data. You can still use them, but rename them honestly and create a new final set. The separation protects your conclusion from memorizing examples.

Use paired comparisons: run prompt A and prompt B on the same tickets with the same evidence. Record the model and settings if using a live model, plus prompt version and date. For the offline track, compare authored candidate outputs; you are learning evaluation procedure rather than claiming model performance. Score before discussing style. Otherwise, a confident voice can influence factual judgment.

Small samples are useful for finding failures and weak for estimating precise production rates. If B scores 9/10 and A scores 8/10, you have observed one extra success on ten cases. You have not demonstrated that B is universally ten percentage points better. Report counts, the actual changed cases and uncertainty. A practical decision may still favor B if its cost is low and it introduces no serious regressions.

## Worked example

Suppose four development tickets produce this result:

| Case | A: unsupported claim | B: unsupported claim |
|---|---:|---:|
| Missing invoice | 1 | 0 |
| Export regression report | 1 | 0 |
| Known password reset | 0 | 0 |
| Conflicting incident evidence | 0 | 1 |

B improves two cases and regresses one. The aggregate moves from two failures to one, but the conflict regression may matter more than both improvements. Inspect the output: B treated its new “most likely cause” field as a demand to guess. Revise the field to “supported explanation or unknown,” then test on development cases again. Keep the old result in the log.

## Exercise 1 · Guided rubric

Write a four-dimension rubric: factual support, next-step usefulness, output validity and authority compliance. Give each dimension a binary pass rule with an example. Define an overall hard failure for claiming an action that never occurred. Score three drafts you write yourself, including one polished but unsupported answer.

**Deliverable:** rubric and scored examples. **Pass:** the polished false answer fails; two reviewers could apply each rule using the supplied evidence.

## Exercise 2 · Build a paired experiment

Create twelve tickets, reserving four before prompt revision. Compare a minimal contract with your lesson 02 contract on eight development cases. Use a model optionally or write candidate outputs explicitly marked as simulations. Record case-level scores, runtime or manual effort, and the exact prompt change. Evaluate the four reserved cases only after selecting a candidate.

**Deliverable:** experiment table, prompts and one-paragraph decision. **Pass:** case counts reconcile; simulated data is labeled; the decision discusses at least one regression or limitation.

When assistant access is available, follow the [model bridge](../../lab/model-bridge.md) to capture raw model decisions and run them through the same validation boundary. This is the practical bridge from a paper experiment to actual AI use. A recorded response is replay evidence for that response; it does not establish how often future generations will behave similarly.

## Exercise 3 · Adversarial measurement

Have a second reviewer change names, product wording and ticket order while preserving facts. Re-score the outputs without revealing the prompt version. Check whether the apparent improvement depended on recognizable examples or on one evaluator's stylistic preference. If working alone, randomize filenames and review after a break.

**Deliverable:** a blind scoring sheet and disagreement notes. **Pass:** disagreements are resolved by refining rules or recording uncertainty, never by silently selecting the preferred score.

## Hints and solution outline

The rubric should evaluate evidence relationships rather than exact wording. “Asks for browser version” can pass in many phrasings. “Claims a refund happened” is a hard failure even if the rest is excellent. Compute differences case by case before totals. Preserve the conflicting-evidence regression as a named case. Keep a prompt changelog with hypothesis, changed text, results and decision. Your final statement might be: “B passed three of four held-out cases; one conflict case still failed; no production claim yet.” That is stronger engineering than declaring a winner from one attractive screenshot.

## Reflection

What would change your mind about the winning prompt? Which failure would outweigh a higher average score? What evidence would you need before enabling an action beyond creating a local draft?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
