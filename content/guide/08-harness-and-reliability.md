# Make agent work reliable enough to operate

In this course, a **harness** is the surrounding software that manages an agent's execution: assembling context, exposing tools, enforcing limits, preserving state, recording events, and deciding when to stop or ask for help. Products use the term somewhat differently, so inspect actual responsibilities rather than relying on a label.

Context engineering concerns what information reaches the model and when. Harness engineering concerns how the wider execution behaves over time. They meet when a long-running task needs a checkpoint, a safe restart, or a compact and accurate handoff.

## Real failures cross several boundaries

Imagine an agent sends a request to create a test run, but the response is lost. Restarting the agent and sending the same request again could create two runs. Reliable recovery needs a way to determine what actually happened, such as an operation identifier and a status lookup. Asking the model to remember that it already tried is not sufficient.

Now imagine two agents editing the same test file. Even if both changes are individually reasonable, their combined result can be wrong. Isolated work, explicit ownership, integration checks, and a final review reduce that risk. These are software engineering controls, not prompt tricks.

## Bound the work and make it observable

A useful runtime can limit steps, time, spending, and tool access. A trace records the requests, results, errors, and relevant versions needed to investigate a failure. Avoid retaining secrets or unnecessary personal data in logs. A polished summary cannot replace the trace when an action's actual effect is disputed.

Keep human review at consequential boundaries appropriate to the task. Test what happens when review is denied, the process is interrupted, credentials expire, or a tool returns partial data. Exercise the recovery path before relying on it.

## Security is part of correctness

The selected OWASP material names common risks, including prompt injection, sensitive information disclosure, and excessive agency. Read those entries first. A retrieved page should not be able to grant itself permission to run a command. A model-generated script should not become trusted merely because the assistant wrote it.

## Where to go after this path

You now have a map from everyday AI assistance to testing AI applications and controlling agents. This is orientation and understanding, not a claim of engineering mastery. Choose deeper study based on your work: generated tests, RAG evaluation, tool integration, or agent reliability.

The original 24 lessons, 15 labs, incident investigations, and capstones are retained as optional practice. The practice shelf explains where each fits. You can ask your tutor to explain a topic further without being assigned a diagram or a document. If you choose an exercise, the tutor should give one step at a time and keep its answer hidden until you try.
