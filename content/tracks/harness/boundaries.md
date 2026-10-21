# What a harness is responsible for

## Start here

The word **harness** can sound more complicated than the idea. Here it means the surrounding software that turns model proposals into controlled execution. Begin after the Tools and Agentic Development introductions. You do not need to build a state machine or write a framework. Open a conversation through the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and follow a simple request through its checks.

## The idea in plain language

A model can suggest the next action, but the application must decide which actions are available and whether a proposed call is valid. The harness prepares relevant context, obtains a proposal, validates it, invokes an allowed operation, records the observation, and decides whether another step is permitted. Different systems divide this work differently; the important point is that these responsibilities exist somewhere.

A **dispatcher** routes an approved request to the matching tool implementation. A **policy** is a rule governing allowed behavior, such as “read only this ticket” or “stop after three calls.” A **runtime boundary** is an enforced check during execution. These are stronger than an instruction asking the model to remember the same rule, though the implementation still needs testing.

The harness also needs honest terminal states: succeeded, failed, cancelled, or awaiting a decision, for example. “Failed” does not necessarily mean that nothing happened. A draft may have been saved before a later trace check failed. Recording effects separately from final status is essential for recovery.

## A small example

Signal Desk's fictional assistant can look up a synthetic test report but cannot send messages. The model proposes `send_notification`. The harness rejects that unknown or unauthorized operation before dispatch. It can return a useful explanation or request a different proposal within a bounded attempt limit.

If the model instead proposes a permitted read with a malformed ID, schema validation blocks it. If the call succeeds but returns irrelevant content, answer evaluation remains necessary. The harness does not become correct merely by enforcing one allowlist. Several boundaries cooperate, and the SDET can inspect each independently.

## Try it with Codex or Claude Code

```text
Explain an agent harness using a fictional read-only test-report assistant.
Do not build code or run tools. Available operation: read_report(report_id).
Allowed report: DEMO-77. Maximum tool calls: 2. No external messages.
Walk through one permitted proposal, one malformed proposal, and one request
to send a message. Explain which component checks each rule before execution.
Define dispatcher, policy, state and budget in ordinary words.
Use a numbered story, not a required diagram or implementation task.
```

**State** means the information the program currently remembers about the run: what step it is on, what it observed, and how much budget remains. The next lesson explains changes of state with a small example before introducing the original engineering exercise.

## What you should see

The demonstration should distinguish model suggestions from runtime decisions. It should not claim that a prompt alone enforces limits. You should recognize where to inspect evidence for rejection before dispatch and where successful tool results enter the next decision. The examples are simulated; no real tool use has been measured here.

## If it goes wrong

If the assistant introduces a framework immediately, ask it to name the required responsibilities first. If it calls a Python validation function an operating-system sandbox, ask what prevents arbitrary code outside that function. If it counts only successful calls toward a budget, ask whether rejected or failed attempts also consume time and cost. The exact accounting rule must be explicit and tested.

## Go deeper

Read [Building effective agents](https://www.anthropic.com/research/building-effective-agents), the introductory workflow/agent distinction only. Stop before framework selection. Then use the academy's retained [harness architecture article](../../articles/harness-architecture.md) and [bounded-loop beginner guide](../../how-to/13.md). The [complete harness lab](../../labs/11-complete-student-harness.md) is optional implementation practice after the concepts make sense.

## Optional practice

Ask your tutor for one new fictional proposal and identify the first boundary that should examine it. Try before seeing feedback. You can keep reading without writing code or completing the original exercise.
