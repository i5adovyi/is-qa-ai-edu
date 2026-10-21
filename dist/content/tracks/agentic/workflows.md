# From chat to a controlled workflow

## Start here

This track explains how assisted development progresses through understandable steps. Begin after learning how a tool request differs from its result. You do not need to build an autonomous agent. Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and a new conversation. The first goal is to recognize who decides the next step and what evidence should justify that decision.

## The idea in plain language

A **workflow** is an organized sequence of operations. It may include a branch: if a test fails, inspect the failure; otherwise continue to review. Some workflows follow predefined paths in code. A more model-directed agent selects actions based on observations. Products use “agent” in different ways, so ask what decisions the system actually makes rather than relying on the label.

**Orchestration** is the coordination of those steps. It includes passing information forward, respecting dependencies, and deciding when to stop. For an SDET, a familiar workflow is reproduce a failure, make a small change, run a relevant check, inspect the diff, then report the result. AI can help at several points without being allowed to decide every boundary.

More autonomy introduces more ways to wander, repeat work, or overstep scope. The useful question is whether flexibility solves a real problem. If the next action is already known and deterministic, a fixed command or workflow may be easier to verify. If evidence determines the next investigative step, model assistance can be useful inside explicit limits.

## A small example

Signal Desk asks for a small improvement to a synthetic test helper. A controlled workflow first reads the helper and its tests. It reproduces the stated behavior, proposes a focused patch, runs the relevant check, and reviews the diff. It stops when the acceptance criteria are met or when missing information prevents a sound change.

Now compare “improve all testing in this repository.” That task leaves scope, success, and stopping unclear. Even a capable assistant can keep finding more work. The problem is partly task design, not merely model intelligence. A beginner should learn the bounded workflow before attempting open-ended delegation.

## Try it with Codex or Claude Code

```text
Teach me agentic workflows using a fictional SDET task. Do not inspect or edit
my repository. Task: a tiny test helper should trim surrounding whitespace from
a label but preserve internal spaces. Explain read, reproduce, propose, verify,
review and stop in plain language. At each step say what evidence is needed.
Compare a fixed workflow with allowing a model to choose the next investigation.
Do not write the implementation or a complete test suite; I am learning the flow.
```

Ask the assistant to pause after explaining one step if the entire story feels too dense. You can read the later retained lessons one at a time: task scope, verification, then review.

## What you should see

The explanation should connect each step to an observable result. “The assistant thinks it is fixed” should not replace a check. The review should still inspect scope and unintended changes after tests pass. A stop condition should distinguish successful completion from blocked work. A workflow can correctly stop without completing the requested change when required evidence or authority is absent.

## If it goes wrong

If the assistant jumps straight into code, restate that this is a conceptual walkthrough. If it proposes unrelated refactoring, ask how that supports the stated behavior. If the workflow repeats identical failed checks indefinitely, ask what new evidence a repeat would provide. If it claims a simulation ran tests, correct the evidence label before continuing; teaching examples are not execution records.

## Go deeper

Read [Building effective agents](https://www.anthropic.com/research/building-effective-agents), only What are agents? and When (and when not) to use agents. Stop before framework choices. This public conceptual reading applies across providers and requires no API access. Continue with [the retained task-scoping guide](../../how-to/10.md). The [coding and workers lab](../../labs/13-coding-and-workers.md) is optional later practice.

## Optional practice

Describe one small fictional QA task and identify its first evidence-gathering step and stop condition. Try this before asking your tutor to improve the workflow. No diagram or implementation is required to move to the next reading.
