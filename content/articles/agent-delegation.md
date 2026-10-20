# Delegate work through contracts, not personalities

**Stage 7 · Original field guide · 25-minute lesson plus a 60-minute coordination lab**

You have one agent implementing a feature, another generating tests and a third reviewing security. The arrangement sounds sensible. Then two workers change the same interface, the tests encode an outdated assumption, and the reviewer approves a file that has changed since inspection. More workers have created more activity without producing a coherent result.

Delegation is a coordination problem. Each worker needs enough information to make progress independently, a clear boundary around what it owns and a return format the coordinator can verify. Isolated contexts can help, but isolation also means assumptions must be transmitted explicitly. Claude's subagent documentation describes separate contexts and configuration; Anthropic's architecture article provides a useful starting distinction between fixed workflows and model-directed agents. [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Agent architecture patterns](https://www.anthropic.com/engineering/building-effective-agents).

## Ask whether parallelism removes a bottleneck

Consider a feature with four pieces: define the data contract, implement the parser, write contract tests and document the behavior. The parser and tests both depend on the contract. Starting everything immediately creates avoidable uncertainty. First agree on the contract. Then implementation and test design can proceed independently. Documentation may begin from the contract but must be reconciled with the final behavior.

For a rough planning estimate, total completion time is the longest dependent path plus coordination, integration and verification time. Three ten-minute tasks do not imply a ten-minute delivery if merging and checking take fifteen minutes. Measure the overhead in your own environment.

Parallel investigation often helps when results can be independently checked: one worker locates relevant source files, another examines failing tests, another reads a specification. Parallel editing helps when file ownership and interfaces are stable. A tightly coupled change in one small function may be easier with one worker and a later independent review.

## Write a task contract

Here is a complete delegation brief for a fictional ticket normalizer:

```text
Outcome: implement normalization of ticket priority values.
Inputs: spec/priority-contract.md at revision 2; fixtures/tickets.json.
Ownership: src/priority.py only. Do not edit tests or the specification.
Behavior: map documented aliases; preserve unknown values as unknown.
Constraints: no network access; no new dependencies.
Verification: run the priority unit tests and report exact results.
Return: changed files, behavior summary, checks run, failures, open questions.
Stop: report a contract conflict rather than inventing a new public behavior.
```

This gives the worker a way to detect that the task is underspecified. “You are a world-class engineer” does not resolve any of these questions. Role framing can establish perspective, but it cannot replace scope, inputs or acceptance criteria.

The coordinator should also communicate what the worker need not know. A parser specialist may need the schema and fixtures, not the entire product discussion. Reducing irrelevant history can make the task easier to understand while preserving the constraints that matter.

## Separate ownership from influence

A test author may discover that the contract is impossible to implement as written. They should report the conflict with a concrete case. They should not quietly rewrite the contract and modify the implementation owned by another worker. The coordinator makes or obtains the decision, updates the contract and tells affected workers which assumptions changed.

Use isolated branches or worktrees when your environment supports them. In a shared checkout, exclusive file ownership becomes more important. Neither mechanism eliminates integration work. Independent changes can still disagree semantically even when Git merges them without conflict.

A practical ownership table has four columns: artifact, owner, consumers and freeze condition. For example, the schema owner freezes revision 2 after review; implementation and tests both record that revision. If the schema changes, both consumers must explicitly acknowledge the new version.

## Require evidence in every return

A useful worker response distinguishes completed work from recommendations. It names changed files and actual commands, describes failures and states whether its conclusions depend on unverified assumptions. Ask for artifacts rather than a long conversational recap.

For a researcher, require URLs and the claim each supports. For an implementer, require the patch and test output. For a reviewer, require findings tied to the inspected revision. An agent's statement that another agent did good work is not independent evidence.

Keep handoff summaries short enough to use, but provide links to detailed artifacts. A coordinator can then investigate one questionable claim without loading every worker's full transcript.

## Reviewers need different conditions

Independent review is most useful when the reviewer can inspect the requirement and result without inheriting all the implementer's justifications. Otherwise it may repeat the same assumptions. Give the reviewer the acceptance criteria, relevant code and verification scope. Ask for counterexamples and missing evidence, not merely agreement.

Disagreement is a diagnostic signal. If two workers interpret a requirement differently, inspect the requirement. Do not settle the issue by majority vote among agents with nearly identical inputs. Resolve it against the user's intent, specification, observable behavior or a targeted experiment.

A final integrator remains accountable for the complete result. Passing worker tests does not guarantee the combined application works. Run the checks that exercise the seams: data passed between modules, shared error handling and end-to-end completion.

## Run a coordination experiment

Choose a small task and perform two runs from the same starting state. In run A, use one worker. In run B, use two workers with a written contract and separate ownership. Record completion time, total model/tool work, merge conflicts, defects discovered and time spent reviewing.

Do not award success merely because run B produced more text or files. Compare usable outcomes. If delegation is slower, identify whether the task was too small, the contract was unclear or verification dominated the schedule. That result is valuable: it tells you where delegation is useful rather than making it a default ritual.

Submit the task graph, briefs, worker returns, integration report and comparison. Pass when every artifact has a clear owner, every claim has a checkable basis and the integrated result meets the original task.
