# Define an agent task

Copy this template before delegating a task to a model or another engineer. Fill every field that affects whether the result is acceptable; omit irrelevant ceremony.

## Intended outcome

What should a user be able to do after this work?

## Inputs and trust

List required inputs, provenance, permitted scope, and which inputs are untrusted. Identify stale or conflicting sources and the rule for resolving them.

## Output contract

Define fields, types, allowed values, length limits, and required citations. Include one valid example and one invalid example.

## Capabilities and boundaries

What can the worker read? What can it change? Which side effects require human approval? What action is explicitly outside the task?

## Acceptance checks

Describe observable outcomes for a happy path, ambiguous input, tool failure, and unauthorized request. Name the commands or review steps used to check them.

## Resources and stop conditions

Set a step or time budget and a behavior for insufficient evidence. Specify what must be reported when the worker cannot finish.

## Handoff

Expected artifact paths, commands run, results, unresolved questions, and next step. The receiver should not need hidden conversation history.
