# 20 · Coordinate workers without losing ownership or state

Stage 7 · 90 minutes · Advanced

Design handoffs, ownership and conflict resolution so parallel work produces a coherent result.

## What you will be able to do

- Define a parent-worker protocol and artifact ownership.
- Handle stale outputs, timeouts and duplicate messages.
- Integrate conflicting findings using evidence and version checks.

## The idea

Coordination is a protocol, even when messages are natural language. A parent assigns work, workers acknowledge scope, produce artifacts and report status. Without explicit ownership, two workers may overwrite the same file or make incompatible changes. Without input versions, the parent may merge a result based on outdated policy.

Use a task identifier and immutable input references. Give each worker a writable area or a clearly exclusive file set. Specify the output format and completion condition. The parent controls the shared integration artifact. Workers can suggest changes outside their scope, but they should not silently make them. These rules make parallelism reviewable and recovery easier.

Distinguish status from result. “Working” is not a partial finding. “Blocked on missing invoice status” is actionable only if it identifies the missing input and what independent work remains possible. A worker that times out may still have produced a useful artifact. The parent should inspect durable output and task state before assigning duplicate work.

Messages can be delayed, repeated or arrive after a task is cancelled. Include task and input versions in the result. Accept only outputs matching the active assignment, or explicitly reconcile older work. Do not let a late worker overwrite a newer approved result. The same principles apply to separate agent processes, human collaborators and background jobs.

## Worked example

The parent assigns `E20` to inspect policy version 2. While the worker runs, policy version 3 becomes available. The worker returns a valid finding for version 2. The result is not necessarily wrong, but it is stale for the current task. The parent records it and requests a narrow recheck against version 3.

```json
{"task_id":"E20","input_version":"policy-v2",
 "status":"complete","artifact":"evidence-E20.json",
 "findings":["KB-EXPORT-2 applies"],"unknowns":[]}
```

A result envelope makes the mismatch visible. A free-floating message saying “all done, use the 100 MB limit” hides the dependency that must be reconsidered.

## Exercise 1 · Guided protocol

Define messages for assignment, progress, blocked, completed and cancelled. Each should include task ID and relevant input version. Write a rule for who may modify the integrated packet. Define how workers report useful partial results without claiming completion.

**Deliverable:** protocol specification and ownership table. **Pass:** duplicate, stale and late messages have explicit handling; every shared artifact has one integration owner.

## Exercise 2 · Build a coordination simulation

Create two worker folders and one parent folder. Assign different analyses of SD-120. Have each worker write an output file with its input version. Integrate matching outputs, then update the policy and rerun only the affected worker. Execute manually or with optional agents; no model API is required.

**Deliverable:** assignments, worker artifacts and integration log. **Pass:** workers do not overwrite each other's files; the final packet names the versions it incorporates; unaffected work is reused deliberately.

## Exercise 3 · Adversarial delivery order

Deliver a completion twice, deliver an old result after a newer result, and deliver a result after cancellation. Also simulate a worker that stops responding after saving a partial artifact. Verify that your protocol avoids duplicate integration and preserves useful evidence without treating incomplete work as final.

**Deliverable:** four event traces. **Pass:** the final artifact is deterministic for equivalent valid results regardless of message order, or any order dependence is explicitly justified and tested.

## Hints and solution outline

A parent can maintain a task ledger keyed by task ID with state, expected input version and accepted artifact ID. Duplicate completion with the same artifact is harmless; conflicting content under the same identity requires review. After cancellation, late artifacts can be retained for inspection but should not automatically update the current result. Use exclusive ownership instead of file locks when the task can be split cleanly; locks solve access collisions but not semantic disagreement.

## Reflection

What did your protocol assume about message delivery? How would you recover if the parent restarted? Which worker output can be reused after a policy update, and what evidence supports that decision?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
