# Lab 05 — Recover a committed operation without duplicating it

**Outcome:** construct stable operation keys and inspect a crash at the effect/acknowledgment boundary. Suggested time: 75–120 minutes.

## The problem

An agent saves a draft. The store commits it. Before the orchestrator records success, the run stops. On restart, the checkpoint still says “save.” Repeating the action might create a second draft unless the operation has a durable identity.

Idempotency is a property of the effect and its replay handling, not merely a clever key string. A system must store the operation's identity, payload fingerprint, result, and effect consistently.

## Observe

```sh
python3 -m lab.cli demo --scenario duplicate --out .lab-runs/lab05-duplicate
python3 -m lab.cli demo --scenario crash-after-write --out .lab-runs/lab05-crash
```

The crash command intentionally exits `3`. Before resuming, open `store.json` and `checkpoint.json`. Verify that the store contains a draft while the checkpoint phase is still `save`.

```sh
python3 -m lab.cli resume .lab-runs/lab05-crash/checkpoint.json
python3 -m lab.cli trace .lab-runs/lab05-crash/trace.jsonl
```

Expected: one draft, one durable write, a resumed run, and a replayed tool result. The second call consumes budget even though it does not repeat the mutation.

## Build

Implement `operation_key(run_id, ticket_id, action)`.

The key must:

- Be stable for identical inputs.
- Differ when the run or action changes.
- Avoid delimiter collisions.
- Be a nonempty string of at most 160 characters.

Naive concatenation is ambiguous: inputs `("a:b", "c", "d")` and `("a", "b:c", "d")` can produce the same joined text. Use a canonical structured representation before hashing, or a similarly unambiguous encoding.

Do not include a new timestamp or random value on every retry. That makes identical retries look like new operations.

## Completion gate

```sh
python3 -m lab.cli practice --lab 05
python3 -m unittest discover -s tests -p 'test_lab_engine.py' -v
```

All five student checks must pass. The baseline recovery test verifies one effect after crash/resume and preserved usage accounting. Add a test for a ticket-ID change and one for unusually long input strings.

## Read the commit boundary

Inspect `Store.mutate` in `lab/storage.py`. A replay with the same key and same fingerprint returns the previous result. Reusing that key with different arguments raises `idempotency_conflict`.

Draw these cases:

1. Crash before commit: no effect; retry may perform it.
2. Crash after commit, before acknowledgment: effect exists; retry must return it.
3. Same key, changed payload: reject; do not guess which intent was correct.
4. A brand-new logical action: use a new operation identity.

The JSON store places the effect and deduplication record in one atomic file replacement. It is a single-process teaching model. A distributed database needs transactional guarantees and concurrency handling; a remote provider may have its own idempotency rules.

## Stretch

Design expiration rules for idempotency records. What happens if a retry arrives after expiration? What if the remote side committed but your local write failed? Explain when reconciliation is necessary and why “exactly once” is usually a claim about a constrained system boundary.

Deliver a recovery runbook: symptoms, files to inspect, safe resume command, expected invariants, and when a human must stop automated retries.

[Hints](hints/05.md) · [Solution discussion](solutions/README.md#lab-05) · [Next lab](06-grounding-and-evaluation.md)
