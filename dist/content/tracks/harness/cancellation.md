# Timeouts, cancellation and unfinished work

## Start here

Read the retained loop, recovery, and observability topics first. You should know what a run remembers, what a side effect is, and how a trace records events. This lesson explains why a visible “Stop” or “Timed out” status may leave work to reconcile. Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) for a synthetic timeline. You do not need to implement asynchronous programming to understand the boundary.

## The idea in plain language

A **timeout** limits how long a caller waits. **Cancellation** requests or enforces that work stop. **Cleanup** releases resources such as child processes, open files, or temporary locks. These are related but distinct operations. Stopping the caller's wait does not automatically reverse an effect already committed by a remote service.

Some runtimes use **cooperative cancellation**: code notices a cancellation request at a defined point and exits while cleaning up. A blocked or badly behaved operation may not respond promptly. Stronger process boundaries can terminate local workers, but killing a local worker still cannot prove that a remote action never happened. The system needs an outcome record or reconciliation path.

Budget enforcement also needs a clear location. A prompt saying “finish quickly” is guidance. A real deadline checked by the runtime is an enforceable mechanism, within its implementation limits. A virtual clock in a deterministic simulation tests accounting rules; it does not measure actual wall time or prove process termination.

## A small example

Signal Desk launches a synthetic report job. At two seconds the caller stops waiting. At three seconds the worker writes a local result. If the user interface says “cancelled; nothing happened,” it overstates the evidence. A better report distinguishes the timeout, whether cancellation was requested, whether the worker exited, and whether any result or external effect exists.

Now suppose a remote write finished before cancellation reached the worker. Repeating the request without checking its operation identity may duplicate the effect. This connects cancellation to the Tools track's idempotency lesson rather than treating it as a purely cosmetic UI feature.

## Try it with Codex or Claude Code

```text
Explain this synthetic timeline without running processes or changing files:
0 seconds: report job starts.
2 seconds: caller deadline expires; it stops waiting and requests cancellation.
3 seconds: worker saves a result because it had not processed cancellation yet.
Explain timeout, cancellation request, confirmed exit, cleanup and known effects.
Show a truthful final status. Then compare a cooperative local worker with a
remote service whose result is still unknown. Define unfamiliar terms first.
```

If you later request a runnable demonstration, ask for a separate disposable script compatible with your installed Python version, using synthetic data only. Do not modify the student harness or conclude that a demonstration covers every subprocess and network failure mode.

## What you should see

The assistant should preserve the distinction between requested cancellation and observed termination. It should avoid claiming rollback from a timeout alone. A good terminal record includes known effects and unresolved outcomes, not just a single color or success flag. Evidence of child-process cleanup requires observing that process's exit; the parent finishing is not enough.

## If it goes wrong

If the assistant says cancellation always happens immediately, ask where the operation can receive the request. If it swallows every exception and returns success, ask how cancellation and failures remain visible. If it recommends retrying a remote write immediately, ask how the prior outcome will be reconciled. If copied Python examples use unavailable APIs, inspect the documented version requirements rather than changing the academy's core runtime casually.

## Go deeper

Read [Python's Coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html), Task cancellation and the `Task.cancel` explanation only. Stop before `uncancel`. The public current reference contains features newer than Python 3.9. The [real MCP lab](../../labs/09-real-mcp.md) offers actual timed failure observations, while [the budget lab](../../labs/04-retries-and-budgets.md) documents its deterministic accounting scope.

## Optional practice

Ask for one new synthetic cancellation timeline and list what is confirmed versus unresolved. Predict the next safe observation before requesting feedback. Keep any executable trial isolated from real external writes.
