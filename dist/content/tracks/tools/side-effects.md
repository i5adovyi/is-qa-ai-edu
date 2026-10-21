# Retries without duplicate effects

## Start here

Finish the results topic first, especially the distinction between a missing response and a failed operation. A **side effect** is a change outside the assistant's answer: creating a draft, adding a label, or sending a message. This lesson uses imagined timelines, so it cannot affect real records. Open a conversation through the [quickstart](../../../docs/ASSISTANT-QUICKSTART.md). You do not need to implement a database.

## The idea in plain language

A timeout tells the caller that it stopped receiving a timely answer. The server might still have completed the operation. Retrying an ordinary create request can therefore create two objects. **Idempotency** means that repeating the same intended operation has the same relevant effect as performing it once.

An **operation key** identifies one intent across retries. The executing service can remember the key together with the accepted arguments and result. If the same key arrives again with the same intent, it returns the existing outcome instead of repeating the change. Reusing that key for different arguments is a conflict, not permission to silently overwrite the first operation.

This requires a real implementation at the effect boundary. A model writing “do not duplicate” in its prompt does not establish atomic storage. **Atomic** means the required changes succeed together or not at all. Saving the effect and its deduplication record separately can leave a crash window between them.

## A small example

Signal Desk creates a synthetic review draft with key `review-demo-62-v1`. The server saves it, but the response is lost. The client now knows only that it did not receive confirmation. Retrying with the same key and payload can recover the recorded result if the service supports that contract.

Generating `review-demo-62-v2` merely because a timeout occurred creates a new intent and may duplicate the draft. Changing the recipient while retaining `v1` also changes meaning. An SDET should test both cases, along with a crash immediately after the effect, because a normal double-click test does not explore every uncertainty window.

## Try it with Codex or Claude Code

```text
Explain idempotency with this fictional timeline; do not call any service.
create_review uses key review-demo-62-v1 and body “Investigate flaky login”.
The server commits the draft and key together, but its response is lost.
Show what the client knows, what the server knows, and what a retry with the
same key and same body should do under that stated contract.
Compare a retry with a new key and a retry with a changed body.
Define atomic, duplicate and reconciliation in ordinary words.
Label all outcomes as hypothetical, not executed evidence.
```

**Reconciliation** is checking the authoritative system to resolve an uncertain outcome. For example, looking up the operation key can establish whether the draft exists. It is different from blindly repeating the write.

## What you should see

The explanation should preserve uncertainty at the client until a reliable observation resolves it. It should not equate a timeout with rollback. The same-key, same-payload case depends explicitly on the service's support; an arbitrary API is not idempotent just because the caller attaches a field named `key`. A useful trace distinguishes attempted writes from actual new effects.

## If it goes wrong

If the assistant proposes endless retries, ask for a limit and a final unresolved status. If it says “exactly once” without describing storage and failure boundaries, ask which assumptions make that claim possible. If it changes the key on every retry, ask how the server could recognize the earlier intent. For real systems, consult the API's retention period for remembered keys; an expired key may no longer prevent duplication.

## Go deeper

Read [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), focusing on retries, side effects, and reused request IDs with changed intent. Skip cloud commands; no AWS account is needed. The retained [recovery lesson](../../how-to/14.md) and [idempotency lab](../../labs/05-idempotency-and-recovery.md) provide a later local implementation route.

## Optional practice

Ask for one new synthetic crash timeline and identify the next safe observation before choosing a retry. Attempt it first; request feedback rather than the lab's reference solution.
