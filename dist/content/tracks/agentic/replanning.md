# Know when to stop or change the plan

## Start here

After learning a controlled development workflow, consider what happens when the first idea fails. A useful assistant can adapt without turning a small task into endless editing. This lesson teaches how to recognize progress, repetition, missing information, and changed scope. Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) with the synthetic case below. No code changes or external actions are needed.

## The idea in plain language

A **plan** is a proposed route toward an outcome. **Replanning** changes that route when evidence makes the current one unsuitable. A **stop condition** states when execution should finish, pause for missing information, or report a limit. A **budget** constrains resources such as attempts, elapsed time, or model calls.

Progress means reducing uncertainty or moving closer to the stated outcome. Repeating the same search without new information is activity, not necessarily progress. Changing unrelated files because a test is difficult can hide the failure instead of resolving it. A good workflow records the hypothesis behind a change and checks whether the expected observation occurred.

Stopping can be correct. The required service may be unavailable, the specification may contradict itself, or the next action may exceed the user's authorization. The assistant should report the concrete blocker and preserve useful evidence. It should not invent completion, silently relax acceptance criteria, or demand unnecessary permission for already authorized ordinary work.

## A small example

Signal Desk investigates a synthetic flaky search test. The first hypothesis is a timing problem. A bounded rerun produces the same failure at the same assertion, and the observed response consistently lacks a required field. Increasing waits again has little support. A better next step is to inspect the fixture or response contract.

If that contract is unavailable, the assistant can explain exactly what is missing and what remains uncertain. It can still inspect unrelated independent evidence if useful, but it should not rewrite the product behavior merely to make the test pass. The task's purpose remains the reference point as the plan changes.

## Try it with Codex or Claude Code

```text
Walk me through replanning using synthetic evidence only. Do not edit files.
Task: investigate a failing search test. Initial guess: insufficient wait.
Two bounded observations show the response is immediate but lacks required field
total_count. The API contract is not supplied. Explain what new evidence changes
the plan, what to inspect next, and what should remain unknown.
Give a reasonable stopping rule and a concise status update. Do not declare the
product or test wrong without a requirement. Define hypothesis and budget.
```

Ask the assistant why each proposed next step is informative. That is a more useful question than asking it to generate a longer plan. A single discriminating check can be better than a list of twenty speculative changes.

## What you should see

The assistant should update its hypothesis from the supplied observations and preserve the missing-contract uncertainty. It should distinguish a limit on repeated attempts from evidence that a cause has been proven. A sensible status update says what was observed, what was ruled out or weakened, what remains unknown, and the next concrete check. It should not produce a fake test result.

## If it goes wrong

If it keeps increasing a timeout, ask what observation supports that change. If it disables the assertion, ask whether the acceptance criterion changed and who established that change. If it generates a new plan after every minor detail, ask it to retain the stable goal and revise only the affected step. If it keeps asking for approval already given, restate the authorized scope and ask for the specific unresolved boundary.

## Go deeper

Revisit [Building effective agents](https://www.anthropic.com/research/building-effective-agents), focusing on the distinction between predetermined workflows and model-directed behavior. Stop before framework selection. The source is public; this lesson's failure story is an original synthetic example. The [verification guide](../../how-to/11.md) and [review guide](../../how-to/12.md) provide retained checks that support better replanning.

## Optional practice

Ask your tutor for one new observation midway through a fictional investigation. State whether you would continue, replan, or stop, and explain which evidence changed your decision. Attempt the decision before requesting feedback.
