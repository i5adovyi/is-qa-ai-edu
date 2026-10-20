# Lab 04 — Recover without retrying forever

**Outcome:** calculate bounded retry delays and explain how attempts, elapsed time, and side effects interact. Suggested time: 60–90 minutes.

## The problem

A timeout does not necessarily mean an operation failed. It means the caller did not receive an answer in time. Retrying a read is often reasonable. Retrying a payment or message without deduplication can create duplicate effects.

Signal Desk retries a synthetic retrieval timeout once. The timeout scenarios use virtual latency, so no network or sleep is needed. Every attempt consumes a call budget, including failed and denied attempts.

## Observe

```sh
python3 -m lab.cli demo --scenario timeout-once --out .lab-runs/lab04-transient
python3 -m lab.cli demo --scenario timeout-always --out .lab-runs/lab04-persistent
python3 -m lab.cli demo --scenario budget --out .lab-runs/lab04-budget
python3 -m lab.cli trace .lab-runs/lab04-persistent/trace.jsonl
```

Before running, predict the number of search attempts in the first two scenarios. Then explain why the persistent scenario stops while its general tool-call budget still has capacity: a retry policy and a global budget are separate limits.

## Build

Implement `retry_delay_ms(attempt, base_ms, cap_ms)`.

Required behavior:

```text
delay = min(cap_ms, base_ms × 2**attempt)
```

`attempt` starts at zero. All inputs must be integers greater than or equal to zero; booleans are not accepted as integers. Reject invalid values with `ValueError`.

Examples: with base 100 and cap 1000, attempts 0–4 yield 100, 200, 400, 800, 1000 milliseconds. A huge attempt number must remain bounded without allocating an enormous integer. A zero base returns zero.

This exercise computes a schedule only. It does not sleep or alter the reference harness. Real integrations need deadlines, cancellation, provider error classification, and possibly jitter.

## Completion gate

```sh
python3 -m lab.cli practice --lab 04
```

All seven public checks must pass, including a zero cap and invalid values in each input position. Add checks for a base above the cap and the exact attempt where the cap is first reached. Explain Python's `bool`/`int` relationship and why a schema may intentionally reject booleans.

## Retry decision table

Write a table for these failures:

| Failure | Retry? | Extra condition |
|---|---|---|
| Retrieval timeout | Usually bounded | Remaining time and call budgets |
| Invalid tool arguments | Usually no unchanged retry | Correct the proposal first |
| Permission denied | No authority escalation | New external authorization required |
| Provider rate limit | Depends | Respect current provider guidance |
| Uncertain mutation acknowledgment | Only with protection | Durable idempotency or reconciliation |

Distinguish retryable transport failures from invalid business requests. A retry loop that treats all exceptions alike hides the source of failure and can amplify load.

## Stretch

Add deterministic jitter using a supplied random seed, then compare delays across ten agents. Explain why identical exponential schedules can cause a synchronized retry spike. Propose a request-level deadline and show a case where the next delay would exceed it.

Deliver a retry policy with maximum attempts, backoff schedule, total deadline, retryable error classes, and a rule for uncertain writes.

[Hints](hints/04.md) · [Solution discussion](solutions/README.md#lab-04) · [Next lab](05-idempotency-and-recovery.md)

## Connect it to the complete harness

This lab teaches one component contract. After completing Labs 01–08, follow [Lab 11](11-complete-student-harness.md) to use this function in real runs with component evidence, crash recovery, and an integrated acceptance gate. The ordinary reference evaluation does not call this student helper.
