# Budget time, tokens, retries, and useful outcomes

## Start here

Read request tracing and service reliability first. You should understand that an agent may make several model and tool calls for one user request. You do not need a provider billing account. This lesson uses fictional units and timings in an existing assistant conversation; see the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md).

Your goal is to choose measurements that describe the whole workflow. A cheap individual model call can belong to an expensive or slow system.

## The idea in plain language

**Latency** is elapsed time until a defined outcome. Specify whether you measure time to first visible text, final answer, or completed action. **Throughput** describes how much work completes in an interval. **Cost per successful task** divides total relevant cost by successful tasks, including costs spent on failures and retries.

A **token** is a unit used by a model's text processing; it is not reliably one word. Provider billing can distinguish input, output, caching, and other categories. Use observed usage and current provider terms for real estimates. Do not assume the fictional numbers in this lesson are prices.

A **budget** limits work: maximum calls, tokens, elapsed time, or expenditure. A **retry** repeats an operation after a failure under a bounded rule. Uncoordinated retries can increase load precisely when a dependency is struggling. **Backpressure** means limiting new work when downstream capacity is insufficient, rather than accepting unlimited requests into a growing queue.

## A small example

Signal Desk compares two synthetic workflows over 10 tasks. A simple workflow costs 100 units total and completes 8 tasks acceptably: 12.5 units per successful task. A larger agent workflow costs 180 units including retries and completes 9: 20 units per successful task.

The second has better success on this tiny sample, but it is not cheaper. Whether its improvement is worth the cost depends on the task and consequences. The example is too small to establish a stable production rate.

Now suppose two independent tool reads each take 2 seconds. Running them sequentially takes roughly 4 seconds plus overhead; running them in parallel may approach 2 seconds plus overhead. Parallelism does not eliminate the work or necessarily lower its cost, and it can encounter concurrency limits.

## Try it with Codex or Claude Code

```text
Explain workflow cost using fictional units, not real provider prices.
Workflow A: 10 tasks, 100 total units including failures, 8 acceptable.
Workflow B: 10 tasks, 180 total units including retries, 9 acceptable.
Calculate cost per acceptable task and explain the comparison's limits.
Then explain sequential versus parallel execution for two independent
2-second tool reads. Distinguish elapsed time from total work.
Propose clear call/time/retry limits for a synthetic demonstration, naming
them illustrative choices rather than universal production thresholds.
Do not call paid APIs, change billing settings, or invent usage measurements.
```

Check the denominators yourself. If the assistant divides only successful-call cost by successful tasks, ask where failed attempts went. They still consumed resources.

## What you should see

The answer should calculate 12.5 and 20 units, describe the quality tradeoff, and avoid declaring a universal winner. It should distinguish queue time, model time, tool time, and time spent retrying. A faster first token can coexist with a slow final completion.

In real testing, inspect median and tail latency. A **95th percentile** is a value at or below which approximately 95 percent of measured durations fall, depending on the calculation method. Do not report a stable percentile from a handful of examples. Keep timeouts and abandoned tasks visible rather than measuring only survivors.

## If it goes wrong

If the system becomes slower after adding workers, inspect duplicated context, coordination calls, queueing, and shared limits. If caching improves speed, check that its keys include relevant version and permission scope; a fast stale answer is not a success.

If retries create a traffic spike, bound total attempts and apply delays appropriate to the dependency's guidance. If a budget stops a run, return an honest incomplete outcome rather than fabricating success. Verify that cancellation actually stops work where possible; a caller timeout alone may leave costly work running.

## Go deeper

Read Google SRE's [Handling Overload](https://sre.google/sre-book/handling-overload/), the introduction and The Pitfalls of Queries per Second. Stop before Per-Customer Limits. Public reading needs no account. The chapter concerns general services; applying its resource perspective to model calls is this lesson's adaptation.

The [harness architecture article](../../articles/harness-architecture.md) and [review and operations lab](../../labs/15-review-and-operations.md) provide optional implementation context. Continue to incident response when you can describe what a budget exhaustion would look like in evidence.

## Optional practice

Ask your tutor for two new fictional workflows with failure and retry costs. Compute one meaningful comparison and state what evidence is missing before requesting feedback. No paid execution or spreadsheet is required.
