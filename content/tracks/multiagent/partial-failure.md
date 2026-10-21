# Recover when only part of an agent team finishes

## Start here

Read shared state, conflict resolution, and team evaluation first. Understand that a worker can fail independently of other workers. This advanced topic is still approachable through a small text example; you do not need to implement a scheduler. Open Codex or Claude Code and consult the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) if needed.

Your goal is to distinguish incomplete work, failed work, and work whose outcome is unknown. These require different recovery decisions.

## The idea in plain language

A **deadline** is the latest time a result is useful. A **timeout** means a caller stopped waiting; it does not necessarily mean the worker stopped. **Cancellation** asks execution to stop, but the system must establish whether cancellation actually took effect. A **checkpoint** saves enough execution state to resume under a defined policy.

For read-only analysis, retrying may mainly cost time and tokens. For an action that creates or changes something, retrying can duplicate the effect. An **idempotency key** identifies one intended operation so a supporting service can recognize repeat submissions. It helps only when the receiving service actually enforces the intended semantics.

A coordinator needs terminal outcomes such as succeeded, failed, cancelled, and unresolved, along with evidence. “No message received” is not the same as failed. A late success may also be unusable if its input revision is no longer current. Recovery must check both execution state and result relevance.

## A small example

Signal Desk assigns three synthetic jobs: classify a ticket, retrieve a policy, and create a draft record. Classification succeeds. Retrieval fails with a temporary connection error. The draft request times out after being sent, so the service may or may not have created it.

The coordinator can preserve the classification if its inputs remain valid. It can retry the read-only retrieval under a bounded retry rule. It should reconcile the draft's operation identity with the receiving service before creating another draft. Repeating all three jobs blindly wastes work and risks duplicates.

If the coordinator process restarts, its saved “request sent” state still does not prove the remote draft's outcome. Durable local records and external effects are separate systems.

## Try it with Codex or Claude Code

```text
Teach recovery from a partial agent-team failure using this fictional run:
Task C classification: succeeded on ticket revision 7.
Task R policy lookup: temporary connection failure, read-only.
Task D create draft: request sent with operation ID draft-42, then timeout;
the receiving service's final outcome is unknown.
The coordinator restarts from a saved record containing those facts.
For each task explain what is known, safe next evidence to obtain, and
what must not be assumed. Define timeout, cancellation, checkpoint, and
idempotency in everyday language. Do not execute requests or claim recovery.
Finally explain what changes if the ticket is now revision 8.
```

Inspect whether the assistant distinguishes the external draft operation from the coordinator's own saved record. Ask it to make the unknown outcome explicit if it labels D simply “failed.”

## What you should see

The walkthrough should retain valid work, bound retries, and reconcile uncertain side effects. It should say that revision 8 may invalidate conclusions made on revision 7. It should not imply that a saved checkpoint recreates a running process or reverses a remote operation.

For real tests, record when a cancellation request was sent and whether execution stopped. A text simulation of cancellation is not evidence that a subprocess was killed. Test lost responses and late results deliberately in a disposable environment, with synthetic data and controlled effects.

## If it goes wrong

If recovery restarts everything, ask which completed results are still valid. If it retries forever, define a maximum attempt count, total time budget, and escalation outcome. If a timeout becomes “success” after an unverified worker message, require evidence from the system that owns the effect.

If all state disappears after restart, inspect whether it lived only in memory. If old work is accepted after cancellation, include task identity and revision in result acceptance. Do not use an agent's natural-language promise as a substitute for enforcing those checks.

## Go deeper

Read LangGraph's [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), the Checkpointer vs. store table and the troubleshooting entry about memory savers not surviving restarts. Stop after that restart explanation. Public reading requires no account. Persistent framework backends need additional dependencies; none are needed for this demonstration.

The retained [coordination lesson](../../how-to/20.md) and [coding and workers lab](../../labs/13-coding-and-workers.md) connect this reasoning to inspectable examples. Follow their setup separately when you choose execution.

## Optional practice

Ask your tutor for one late worker result arriving after the coordinator has changed the input. Decide whether to accept, reject, or recheck it, and identify the evidence needed. Request feedback after your attempt, without revealing incident debriefs.
