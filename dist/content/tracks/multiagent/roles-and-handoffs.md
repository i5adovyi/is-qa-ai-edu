# Understand what one agent hands to another

## Start here

This is the entry point for multi-agent work. First know that an **agent** is software that uses a model to choose steps and may call tools. You do not need to build one. Open a normal Codex or Claude Code conversation; the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) explains the mechanics.

Your first goal is to understand responsibility and information flow. Asking an assistant to pretend to be three specialists in one reply is a useful explanation exercise, but it does not prove that three independent workers ran.

## The idea in plain language

A **worker** receives a bounded task and returns a result. A **coordinator** decides what work is needed, assigns it, and checks the results. A **handoff** transfers responsibility for the next step, along with enough context to continue correctly. Frameworks use these terms differently, so always ask who controls execution after the transfer.

Consider two common arrangements. In a supervisor arrangement, workers report back to one owner, who decides the final response. In a transfer arrangement, control moves to another specialist. Neither is automatically better. A simple request may need only one agent; every added worker creates communication, cost, and failure handling.

A useful handoff includes the goal, relevant inputs, allowed actions, required evidence, and unresolved questions. Copying the entire chat may expose unnecessary information and still bury the important requirement. Summarizing too aggressively can remove a constraint. Select context deliberately and keep source references available.

## A small example

Signal Desk wants a summary of a synthetic failed test. A log reader receives the supplied trace and reports observations. A test reviewer receives the requirement and test code and checks whether the assertion matches. The coordinator combines those results and owns the final explanation.

The log reader says, “The request timed out after 2 seconds; the server's final outcome is unknown.” A bad handoff compresses that to “The server failed.” The next worker might then recommend a retry that duplicates a completed operation. A good handoff preserves the uncertainty and says what evidence could resolve it.

Workers should not infer permission to edit production data because another worker suggests a fix. A recommendation is information; execution authority comes from the task and enforced permissions.

## Try it with Codex or Claude Code

```text
Teach multi-agent handoffs through a text-only demonstration.
Synthetic case: test T-9 sends a create-ticket request. The client times
out after 2 seconds. No server log or ticket lookup is supplied.
Use three labeled roles: log reader, test reviewer, coordinator.
First explain each role's responsibility. Then simulate a short handoff
that preserves what is known, what is unknown, and what evidence is needed.
Do not claim actual subagents ran. Do not call tools or send requests.
Show one example of a harmful summary that loses uncertainty, then explain
why the coordinator must not treat that summary as execution evidence.
```

Read the role boundaries before the simulated dialogue. If your assistant supports real worker tools, this prompt still asks for a simulation. Actual delegation belongs in later optional practice with inspectable worker records.

## What you should see

The coordinator should not assert that the ticket was created or that it was not created. The handoff should preserve the timeout observation and the missing final outcome. The test reviewer may discuss what the assertion checks, but cannot invent absent test code.

Notice that useful collaboration depends on explicit uncertainty as much as expertise. A confidently phrased worker answer is not stronger evidence than the source it cites. A later worker must be able to trace a claim back to the original observation.

## If it goes wrong

If all three roles repeat the same conclusion, ask what unique input or responsibility each has. If the coordinator treats majority agreement as proof, ask whether all workers relied on the same mistaken summary. Shared assumptions create correlated errors, meaning the errors can move together rather than cancel out.

If the demonstration becomes a long debate, request one handoff with five fields: goal, observations, constraints, uncertainty, and next evidence. If it produces code before explaining responsibility, return to the text example. You are learning the boundary first.

## Go deeper

Read LangChain's [Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs), the opening explanation, Key characteristics, and When to use. Stop before Implementation. Public reading needs no account; running framework examples requires separate dependencies. Its handoff mechanism is one implementation, not a universal API for every assistant.

Continue to the retained [delegation lesson](../../how-to/19.md). The [delegation article](../../articles/agent-delegation.md) and [brief template](../../../templates/delegation-brief.md) are optional references when you are ready to assign real work.

## Optional practice

Ask your tutor for one incomplete handoff about a different synthetic test failure. Identify the most important missing fact before asking for feedback. You do not need to draw an agent architecture or write a specification to continue.
