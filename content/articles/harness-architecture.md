# Build the runner you can trust

**Stage 5 · Original field guide · 30-minute lesson plus a 60-minute design exercise**

An agent is more than a model call. Something supplies the task, presents tools, validates proposed actions, executes them, records observations and decides when work is finished. In this course, **harness** means that surrounding execution system. The exact term varies between products; define your own boundary before comparing implementations.

Imagine a release-readiness assistant. It reads a change request, inspects test reports and drafts a recommendation. The model helps decide which evidence matters. The harness determines whether a report can be read, whether a malformed tool call runs, whether a timeout consumes the remaining budget, and whether a draft recommendation is mistaken for an approved release.

Anthropic's long-running agent article is a useful example of persistent artifacts supporting continuity. OpenAI's runtime overview illustrates that state and tool execution can belong to different layers depending on the integration. Study those sources, then make the ownership explicit in your own system. [Long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Agent runtime choices](https://developers.openai.com/api/docs/guides/agents).

## Begin with invariants

An invariant is a condition that must hold regardless of what the model proposes. For the release assistant, choose these:

1. A run can read only the fixture directory assigned to it.
2. A report identifier must exist before its contents are returned.
3. No recommendation can execute a deployment.
4. Every tool attempt has a recorded outcome, including rejection.
5. A run stops when its call or elapsed-time budget is exhausted.
6. Completion requires a valid result plus evidence references.

These are testable claims about software. “Be careful” is not an invariant. Put enforcement at the boundary where the effect happens: path resolution in the file reader, input validation in the tool dispatcher, authorization in the service, budget checks in the runner.

## Model the run as a state machine

A minimal set of states is `created`, `running`, `waiting`, `completed`, `failed` and `cancelled`. Store a reason for every transition. `waiting` could mean required human input, an external job or a retry deadline; these reasons should not be conflated.

A model saying “done” is a proposal to complete. The harness should check the output shape, verify that cited artifacts exist and determine whether required work is still pending. If the assistant claims a test passed but there is no successful test event, completion should fail or be marked incomplete.

Here is conceptual pseudocode, not a provider SDK example:

```text
while state == running:
    enforce_budget_and_deadline()
    proposal = ask_model(build_context(events, task))
    if proposal is final_answer:
        validate_answer_and_evidence(proposal)
        save_result_and_complete()
    else:
        validate_tool_name_and_arguments(proposal)
        authorize_with_server_side_policy(proposal)
        observation = execute_with_timeout(proposal)
        append_event(proposal, observation)
```

Real implementations must also record failures from validation and execution. Avoid a broad exception handler that turns all failures into “no results.” The difference between an empty result and an unavailable service changes the next decision.

## Make tool responses unambiguous

A useful response envelope includes `status`, `data`, `error_code`, `retryable`, and an evidence identifier. Return a bounded preview plus a retrievable artifact reference for long results. An unknown ticket might produce `not_found`; a timeout might produce `temporary_failure`. Only the latter may justify a retry, and only within a configured limit.

Do not hide policy enforcement inside natural-language tool descriptions. A description can teach the model the expected use. The actual tool must still reject an absolute path outside its allowed root, even if the model claims the user approved it.

For side-effecting systems, handle retries carefully. A network timeout after sending a request does not prove the request failed. A practical design uses an idempotency key tied to the intended operation, then reconciles the operation status before retrying. The local laboratory can simulate this with a ledger: crash after recording an action but before returning the acknowledgment, then resume. The ledger should contain one action, not two.

## Persist the right history

Use an append-only event log for observations and transitions. Each event should carry a run ID, sequence number, timestamp, action type and result status. Store configuration versions alongside the run: model identifier, prompt revision, tool schema revision and dataset revision. These make failures explainable later.

Logs should avoid secrets and unnecessary personal data. A secret-redaction policy is more reliable when structured fields are known before text is written. Do not assume a logging platform will discover every sensitive string after ingestion.

A checkpoint is not just the last assistant paragraph. It should point to completed artifacts, remaining tasks, active deadlines and any operation whose outcome is uncertain. The resuming process must reconcile that state with the environment.

## Test failure paths before adding autonomy

Use a mock model that emits a scripted sequence: valid lookup, malformed arguments, repeated call, unsupported tool name, false completion and budget exhaustion. This separates runner correctness from model capability. Your mock tests prove how the runner handles these inputs; they do not prove that a real model will choose good actions.

Then connect a live model, if desired, and measure task success separately. Inspect whether it recovers from allowed errors, wastes calls, or cites observations it never saw. Keep the same invariants. A model upgrade should not silently relax the execution policy.

## Submission and review

Submit a state diagram, tool contract, example event log and three failure demonstrations. Include a crash-resume test and a completion rejection caused by missing evidence. Pass when another person can explain what happened from the artifacts, identify the stop condition and verify that prohibited actions remain impossible through the exposed interface. A useful harness makes both successful and unsuccessful runs legible.
