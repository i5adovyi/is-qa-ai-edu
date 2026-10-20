# 13 · Build the agent loop as an explicit state machine

Stage 5 · 90 minutes · Practitioner

Turn model proposals into a bounded execution loop with clear transitions and useful terminal outcomes.

## What you will be able to do

- Separate proposal, validation, execution and observation.
- Define terminal states and enforce an iteration budget.
- Replay a loop using scripted responses before adding a model.

## The idea

An agent loop repeatedly observes state, proposes a next action, executes an allowed action and incorporates the result. The loop becomes difficult to reason about when these steps blur together. A model might propose a tool call, but proposal is not execution. A tool might succeed, but success is not task completion. An explicit state machine makes those distinctions inspectable.

For Signal Desk, use states such as ready, proposing, validating, executing, observing, complete and needs_review. Add failed or cancelled when appropriate. Define which transitions are legal. A malformed proposal should move to a controlled repair or review path; it should not reach the executor. A final draft should be validated before moving to complete.

The harness owns budgets and stopping conditions. A prompt can ask the model to stop after several attempts, but a runtime counter can enforce it. Set limits for steps, repeated identical actions and elapsed time. When a budget expires, return the partial artifact, reason and next useful action. “Budget exhausted” is an operational result, not proof that the customer request was impossible.

Use scripted model responses first. A list of proposed actions lets you test the loop deterministically: search, inspect result, draft, finish. You can inject an unknown tool or an endless search sequence without paying for model calls. This establishes orchestration behavior. Later, a live model adapter can supply proposals through the same interface, with its nondeterminism measured separately.

## Worked example

A minimal conceptual loop is:

```text
while steps_remaining:
    proposal = planner(current_state)
    checked = validate(proposal, allowed_tools, task_policy)
    if checked requests completion:
        validate_final_artifact(); finish_or_review()
    else:
        result = execute(checked)
        record_result_and_update_state(result)
    decrement_budget()
return needs_review with partial work and stop_reason
```

Suppose SD-113 repeatedly searches “export broken” and receives the same result. After two identical calls with no new evidence, the harness can stop or require a changed query. It should not invent an answer simply because the search budget ended. A useful final status identifies what was found and what remains unresolved.

## Exercise 1 · Guided transitions

Draw the state machine and label every transition with its triggering event. Include malformed proposal, tool failure, valid draft, budget exhaustion and user cancellation. Identify where the step counter changes and where a final artifact is validated.

**Deliverable:** transition table or diagram. **Pass:** every state has a defined exit or terminal meaning; no unvalidated proposal can reach execution.

## Exercise 2 · Build a deterministic loop

Implement the state machine in a small script or use the bundled lab as an inspectable example. Feed scripted proposals for a successful run, a malformed tool call and a repeated search. Run `python3 -m lab.cli demo` to compare the lab's behavior, adapting your vocabulary to its actual states rather than assuming exact names.

**Deliverable:** implementation or annotated trace for three runs. **Pass:** each run terminates with an explicit reason; the executor receives only validated proposals; step limits are enforced by code or a mechanically applied simulation rule.

The bundled lab follows a fixed retrieval/decision/write workflow. Its injected policy supplies a bounded final decision, not arbitrary next-tool proposals. Inspect it as an example of controls, or build the scripted loop above to practice planner-driven action selection. The [model bridge](../../lab/model-bridge.md) exercises the decision seam; adding a model-controlled tool loop requires the separate proposal contract described in the [adapter brief](../../lab/provider-adapter-design.md).

After labs 01–08, use [lab 11](../labs/11-complete-student-harness.md) to connect all eight of your helper functions to this workflow. Inspect its component evidence to identify the exact implementation that redacted the ticket, packed evidence, authorized the read, scheduled a retry, created an operation key, checked citations, summarized events, and proposed the decision. It remains a fixed workflow, but the selected student components now affect its actual execution.

## Exercise 3 · Adversarial completion

Supply a planner response that says “done” before a draft exists. Supply another that requests an unknown tool and a third that loops forever. Use your exercise 2 planner-driven script, or mechanically apply your transition table to these three scripted proposal sequences and label the results as simulations. The bundled `lab.cli demo` does not accept arbitrary planner proposals and cannot by itself execute this exercise. Verify that your execution or simulation rules detect all three independently of the planner's confidence. Optional model use can generate proposals, but keep the scripted cases as deterministic regression checks.

**Deliverable:** three failure traces and expected terminal states. **Pass:** no false completion, no unknown-tool execution and no unbounded loop.

## Hints and solution outline

Represent state as data rather than hidden control flow. Store the task ID, evidence IDs, proposed action, results, step count and stop reason. Validate completion against the artifact, not the wording of the planner's response. A repeated-action detector can hash normalized tool name and arguments, but consider whether a repeated read might legitimately observe changed data. Your first implementation can use a narrow rule for the synthetic static corpus and document that assumption.

## Reflection

Which transitions require model judgment, and which should always be deterministic? What should a user receive when the agent stops halfway through useful work? How can you tell a legitimate retry from a loop that makes no progress?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
