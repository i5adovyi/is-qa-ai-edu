# Understand an agent before building one

An agent uses a model to help decide what to do next, often by selecting tools, observing their results, and continuing toward a goal. Different products use the word differently. Focus on who chooses the next action, what actions are possible, and what stops execution.

A fixed workflow could always fetch a failed test, collect its log, and produce a summary in that order. A more flexible agent might choose which log to inspect next based on the previous result. That flexibility can help when the path is uncertain; it also creates more behavior to test.

## A familiar investigation

Suppose an agent investigates a CI failure. It reads the failed job, notices an environment mismatch, requests the runner configuration, and proposes a cause. Each action produces an observable result. A tool error is information to handle, not proof that the requested task occurred.

The surrounding application should decide which tools are available, validate arguments, enforce permissions, and stop after bounded work. The model should not be the sole authority deciding whether its own dangerous action is allowed.

## What an SDET tests

The final answer is only part of the behavior. An agent can give a correct diagnosis after accessing an unauthorized file or repeating an expensive operation unnecessarily. Inspect the sequence of requested actions, their actual effects, and the stopping condition.

Include cases where evidence is missing, a tool times out, the same action is suggested twice, or a document contains misleading instructions. A timeout does not always mean nothing happened. If an operation has side effects, retrying it may duplicate work. This is where idempotency and reconciliation become useful, familiar engineering concepts.

## Multiple agents add coordination work

Specialized agents can investigate independent parts of a problem. They also introduce duplicated work, inconsistent assumptions, stale handoffs, and conflicting edits. More agents are not automatically better. Compare against a simpler workflow and decide whether the improvement justifies the added coordination.

The selected Hugging Face unit explains tools and the action/observation cycle. You can read its conceptual sections without building the demonstration agent or completing a certificate. Next, learn the harness: the software that makes repeated agent work controllable and inspectable.
