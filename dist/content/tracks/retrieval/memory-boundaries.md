# Design memory that respects users and change

## Start here

You understand retrieval and grounded answers. Now consider information that persists beyond one request: preferences, task state, previous outcomes, or knowledge extracted from conversations. Memory can improve continuity, but stale or wrongly shared memory can produce serious errors. This lesson uses invented users and stores nothing.

## The idea in plain language

**Working memory** is information used during the current task. **Persistent memory** survives beyond that task or session. It may live in a database, files, or a product-specific service. Retrieving an old note into context is different from retraining the underlying model, and persistence alone does not make an agent improve.

Every stored item needs a purpose and scope. **User scope** restricts an item to one person; **tenant scope** restricts it to an organisation or customer boundary. Shared knowledge may be intentionally reusable, while personal preferences or private incident details may not be. A similarity match does not override those boundaries.

Memory also needs a lifecycle: create, inspect, correct, expire, and delete. **Retention** is how long it is kept. A stale preference can be worse than no preference if it silently overrides the user’s current request. Deleting an item from one table is insufficient if a cached copy or derived summary continues to reveal it.

## A small example

Fictional user Mira at tenant North prefers short explanations. Fictional user Leon at tenant South is investigating a private ticket. A shared assistant stores both records. When Mira asks about her own ticket, Leon’s incident notes must not appear just because the wording is similar.

Later Mira asks for a detailed explanation. Her older “short answers” preference should not erase this explicit request. If she asks to remove that preference, future behaviour should reflect its deletion across the memory paths actually used by the system.

Now imagine a summary says “Mira completed all tests,” but the original conversation only said a reference demo ran. That is an erroneous memory, not a successful learning feature. Persisting it makes the error more durable. Preserve evidence type and uncertainty when creating summaries.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Teach memory design using invented records only. Do not save anything.
Mira,tenant North: prefers short explanations.
Leon,tenant South: private incident notes about failed ticket export.
Mira now asks for a detailed explanation about her own export problem.
Explain what may be retrieved, what must remain isolated, and how the
current request affects the old preference. Explain deletion, expiry,
and cached summaries in beginner terms. Do not infer real learner progress.
```

Ask which decisions belong in deterministic application controls rather than trusting a model to remember the correct scope. Access checks should be enforced before private records enter the model’s context. A prompt asking it not to reveal the wrong record is not a substitute for preventing that exposure.

## What you should see

The answer should exclude Leon’s private record, respect Mira’s current request, and describe how a stored preference can be inspected or removed. It should distinguish a conceptual design from an implemented memory service. It should not claim that keeping more conversation history automatically produces better judgement.

## If it goes wrong

If memory is shared through one global search index, verify that access filtering applies to every retrieval and cache path. If deleted information returns, inspect derived summaries and backups according to the system’s documented policy. If a preference conflicts with a current request, use the current intent rather than an old generalisation. If your academy progress is missing after account migration, import an authorised export or use the same local database; do not invent continuity.

## Go deeper

Read “Understanding AI Agent Memory” and “Types of Memory” in Microsoft’s [Memory for AI Agents](https://github.com/microsoft/ai-agents-for-beginners/blob/main/13-agent-memory/README.md). Stop before implementation and service setup. Treat improvement claims as hypotheses that need evaluation. The academy’s [local data guide](../../../docs/LOCAL-DATA.md) explains its actual progress storage and transfer boundaries.

## Optional practice

Ask your tutor for three new fictional memory records and one request. Decide which records are eligible, which are relevant, and which need rechecking. Attempt those three separate decisions before receiving feedback. Do not use real customer or personal data for this exercise.
