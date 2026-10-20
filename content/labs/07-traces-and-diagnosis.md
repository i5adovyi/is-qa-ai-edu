# Lab 07 — Turn events into an explanation

**Outcome:** summarize a trace and diagnose failure without exposing raw user data or relying on a model's self-report. Suggested time: 60–90 minutes.

## The problem

“The agent failed” is not enough to repair a system. You need to distinguish a bad decision, denied tool, exhausted budget, repeated timeout, and a successful mutation followed by a failed next action.

Signal Desk traces state transitions and boundary events. Its sequence number gives order within one run. Timestamps help inspection but do not replace causal events. The logs omit full ticket and draft bodies.

## Observe

```sh
python3 -m lab.cli demo --scenario timeout-once --out .lab-runs/lab07-retry
python3 -m lab.cli demo --scenario denied-tag --out .lab-runs/lab07-denied
python3 -m lab.cli demo --scenario duplicate --out .lab-runs/lab07-duplicate
python3 -m lab.cli trace .lab-runs/lab07-denied/trace.jsonl
```

The denied-tag command intentionally exits nonzero. Identify the first event that establishes a saved draft and the later event that establishes the permission rejection. Write a two-sentence account that includes both.

Compare the number of tool attempts with durable writes in the duplicate run. Explain why those metrics should differ.

## Build

Implement `summarize_trace(events)`, returning exactly:

```python
{
    "tool_attempts": 0,
    "rejections": 0,
    "retries": 0,
    "replay_hits": 0,
}
```

Count events named `tool_attempt`, `tool_rejected`, and `retry_scheduled` in their corresponding fields. Count a replay hit only when the event is `tool_result` and `replayed` is the Boolean value `True`. The string `"false"` is not a Boolean and must not count.

Unknown events do not affect these totals. An empty trace produces zeroes.

## Completion gate

```sh
python3 -m lab.cli practice --lab 07
```

All three public checks must pass. Add a mixed trace with two rejections and a successful completion. Add a non-tool event containing `replayed=True` and confirm it does not count.

## Write an incident note

Use one trace to produce:

1. User-visible outcome.
2. First failing boundary and error code.
3. Effects that definitely committed.
4. Effects that definitely did not commit.
5. Any uncertain effect requiring reconciliation.
6. Safe next action and evidence supporting it.

Do not include raw sensitive content just to make the report feel thorough. Refer to bounded IDs and event sequence numbers.

Read `read_trace` in `lab/storage.py`. It rejects malformed JSON, broken sequence numbers, and mixed run IDs. Discuss the tradeoff of failing loudly on a partial trailing write versus attempting recovery. Automatic repair must not silently hide lost events.

## Stretch

Define an alert for repeated retries across runs. Distinguish “a run emitted a rejection” from “a run failed”: a recovered timeout can contain both rejection and successful completion. Draft a dashboard with task success rate, useful completion rate, mutation count, timeout count, budget exhaustion, and replay rate.

Deliver one annotated trace and an incident note another learner can use to reproduce the failure.

[Hints](hints/07.md) · [Solution discussion](solutions/README.md#lab-07) · [Next lab](08-ship-an-evaluated-policy.md)
