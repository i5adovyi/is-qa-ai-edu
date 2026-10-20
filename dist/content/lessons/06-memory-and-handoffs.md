# 06 · Make memory resumable, inspectable and forgettable

Stage 2 · 90 minutes · Foundation

Preserve useful progress across sessions without turning stale summaries into permanent truth.

## What you will be able to do

- Design a handoff that supports safe resumption.
- Separate durable facts from working hypotheses.
- Specify invalidation and deletion rules for stored context.

## The idea

An agent session can end before a task is complete. The next session needs more than a transcript summary. It needs the goal, current state, evidence locations, completed actions, unresolved decisions and the next useful step. A good handoff minimizes rediscovery while making stale assumptions easy to detect.

Use three kinds of memory. Task state records what this run has done. Reference knowledge stores information intended to be reused across tasks. User preferences record authorized choices that remain relevant. These have different lifetimes and authority. A hypothesis about one export failure must not become a permanent fact about every customer. A user's preference for concise drafts must not override a required disclosure.

Every durable item needs provenance and a rule for when to reconsider it. “API unavailable” may be true at 10:00 and false at 10:05. “Customer uses SSO” may be a report requiring verification. “Draft saved at path X” should be checked against the file before resuming. Memory is an index into evidence, not an infallible substitute for it.

A checkpoint also has a consistency problem. If you save “draft complete” before writing the draft, a crash leaves misleading state. If you write the draft first and crash before the checkpoint, resumption may repeat work. Later lessons build durable execution; here, make the discrepancy visible with artifact IDs and verification steps. Design the next session to reconcile reality before continuing.

## Worked example

A weak handoff says, “Investigated export issue; probably fixed.” A useful one says:

```text
Task SD-106: prepare troubleshooting draft; no external send permitted.
Completed: retrieved KB-EXPORT-2; saved draft D-106 locally.
Evidence: KB-EXPORT-2 applies to version 2.4; browser still unknown.
Hypothesis: browser extension conflict, not verified.
Open decision: ask for clean-session reproduction.
Resume: verify D-106 exists; read its validation report; request review.
Invalidation: reload knowledge if its version changed.
```

The second handoff distinguishes work performed from a possible explanation. A new agent can resume without converting “probably fixed” into a customer-facing claim. If D-106 is missing, it can repair the state rather than reporting completion.

## Exercise 1 · Guided handoff

Write a handoff for SD-106 after retrieval but before draft validation. Limit it to 250 words. Include a next action that is executable without guessing. Then remove all previous chat context and use only the handoff to explain what is known and what remains.

**Deliverable:** handoff and resumption notes. **Pass:** no claim of validated completion; all referenced artifacts have IDs or locations; one hypothesis is explicitly marked unverified.

## Exercise 2 · Build a memory ledger

Create ten memory items spanning task state, knowledge and preferences. Give each an owner, source, recorded time, scope and invalidation condition. Add a deletion policy for synthetic personal information. Implement the ledger as a local JSON file or table; an API is unnecessary. Simulate a new policy version and identify exactly which items need review.

**Deliverable:** ledger and invalidation report. **Pass:** a policy update does not silently preserve conflicting old rules; task-specific observations cannot leak into unrelated tasks as established facts.

## Exercise 3 · Adversarial stale state

Alter the handoff to claim that D-106 passed validation, but leave a failed validation result in the artifact folder. Separately, mark an unavailable tool as permanently broken. Resume from each handoff. Write reconciliation rules that prefer current observable evidence and treat temporary failures as time-bounded observations.

**Deliverable:** two recovery traces. **Pass:** neither stale summary causes an incorrect completion claim or permanent avoidance of a recovered capability.

## Hints and solution outline

Use fields such as `kind`, `value`, `source`, `scope`, `observed_at` and `recheck_when`; exact naming is your choice. Keep the full evidence elsewhere and store a reference. Before resuming, verify the artifact and current policy version. When state and artifact disagree, record the mismatch and recompute the status. For preferences, distinguish “user explicitly requested” from “we inferred from one example.” Optional model use can test whether another session follows your handoff, but the ledger exercise is fully offline.

## Reflection

What should Signal Desk deliberately forget? Which stored item would be most dangerous if treated as timeless truth? How will a future maintainer discover why a memory item exists?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
