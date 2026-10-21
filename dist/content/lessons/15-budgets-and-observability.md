# 15 · Make cost, latency and behavior observable

> Optional practice edition. You can read this explanation without completing its exercises. For the guided SDET route, use [Start here](../../docs/START-HERE.md).

Stage 5 · 120 minutes · Practitioner

Instrument the harness so you can explain what happened, where time went and why a run stopped.

## What you will be able to do

- Design a trace that correlates steps, tools and outcomes.
- Enforce separate step, time and cost budgets.
- Minimize sensitive data while preserving diagnostic value.

## The idea

A final answer hides most of the system's behavior. Two runs can produce the same draft while one makes two tool calls and the other makes forty. A trace records meaningful events so you can diagnose errors, compare designs and explain outcomes. Observability should answer specific questions rather than collect every possible byte.

Use a run ID to connect events and a step ID for each action. Record event type, timestamp, tool name, status, duration and relevant artifact IDs. Preserve prompt and policy versions, model identifier when applicable, and a stop reason. For a failed tool call, record a structured error category. Avoid storing raw credentials or unnecessary customer content. Synthetic fixtures make the course safe to inspect freely; real deployments need deliberate retention and access policies.

Budgets constrain different resources. A step limit bounds orchestration even when tools are fast. A time limit protects user experience when tools stall. A monetary budget matters when using paid providers. Token counts may help estimate cost, but prices and billing details are provider-specific and change. Use actual current pricing only for a real integration; offline simulations should label costs as assumptions.

For a cost simulation, define integer accounting units and reserve the maximum permitted cost of a call before starting it. If a call reserves 7 units, then reports 4 units of usage, release the unused 3. A lost response does not prove zero usage: keep the reservation until reconciliation, or stop if another call would exceed the remaining allowance. This is a local accounting policy, not a guarantee about a provider's billing. A real integration needs documented pricing and usage behavior, bounded output, and accounting for retries and all workers.

Measure distribution, not just averages. One slow run can dominate a user's experience even when the average is low. Track median and a high percentile when sample size permits, alongside counts and maximum. Do not report a precise high percentile from three observations as though it represents a stable production distribution. Small samples are still useful for detecting obvious bottlenecks.

## Worked example

A synthetic trace for SD-115 includes:

```text
run_started run=R15 policy=v2
search_started step=1 query_hash=abc
search_finished step=1 duration_ms=40 sources=2
draft_proposed step=2
validation_failed step=2 code=unknown_source
draft_revised step=3
run_finished status=draft_ready steps=3 stop_reason=validated
```

This trace explains a revision without storing the entire draft in every event. The artifact can be inspected separately through its ID. If a run ends after the search, the missing terminal event is itself a signal to investigate interruption rather than assume success.

## Exercise 1 · Guided trace design

Choose ten event fields and justify each by a diagnostic question. Define three terminal statuses and five stop reasons. Mark fields that could contain sensitive data in a real system. Decide whether to omit, redact, hash or retain each, explaining the diagnostic tradeoff.

**Deliverable:** event schema and retention notes. **Pass:** you can reconstruct event order and tool outcomes without logging secrets or duplicating every input.

## Exercise 2 · Build a budget dashboard

Run ten scripted scenarios with different step counts and simulated tool durations. Calculate total calls, successful outcomes, failures, median duration and maximum duration. Add a step budget and a time budget; compare outcomes before and after enforcement. Use `python3 -m lab.cli trace <trace.jsonl>` to inspect an actual lab-generated trace when available.

Add a separate cost ledger with a 10-unit budget and a maximum reservation of 7 units per call. Run three independent cases: a call reports 4 units then another requests 7; a call reports 3 then another requests 7; and a call loses its response while holding its 7-unit reservation. Predict which next calls are admitted, then check the ledger. Record consumed, reserved, and available units separately. These are invented teaching units, not currency or current token prices.

**Deliverable:** trace files, comparison table, and cost ledger. **Pass:** budget stops are distinguishable from task failures; the three cost cases respectively reject, admit, and reject a subsequent 7-unit call; unknown usage is not recorded as zero. Label virtual time and invented cost assumptions. The bundled harness implements step and virtual-time limits; this cost ledger is a separate exercise, not a feature already implemented by `lab.contracts.Budget`.

## Exercise 3 · Adversarial logging

Insert a synthetic secret marker into a ticket and force a tool error that echoes its arguments. Check every event and error path for the marker. Then remove the final event from one trace and create a negative duration in another. Make your trace reader flag incomplete or impossible records.

Use the event schema you designed in exercise 1 and add these integrity checks to your own reader or apply them mechanically in a documented review. The bundled `lab.cli trace` checks JSON structure, sequence numbers, and run IDs; it does not require a terminal event or validate your new duration field. Its successful exit alone cannot satisfy these two checks.

**Deliverable:** leakage check and trace-integrity report. **Pass:** the synthetic marker is excluded from retained logs according to your policy; malformed traces cannot silently produce reassuring metrics.

## Hints and solution outline

Start with questions such as “Why did this stop?” and “Which tool consumed most time?” Trace fields should answer them. A timer around the actual tool boundary measures tool latency; it does not measure model planning time unless separately instrumented. A cost estimate should preserve its rate assumptions and timestamp. Use stable IDs to join events to artifacts, but remember that hashes of low-entropy personal values can still reveal information through guessing.

## Reflection

What failure could you not explain from your current trace? Which logged field could you remove without losing diagnostic power? What would trigger an operator alert instead of merely appearing in a report?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [OpenTelemetry: Traces](https://opentelemetry.io/docs/concepts/signals/traces/)
- [Google SRE book: Service-level objectives](https://sre.google/sre-book/service-level-objectives/)
