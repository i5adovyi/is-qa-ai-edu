# What a tool call actually does

## Start here

You can follow this lesson in a conversation with Codex or Claude Code. You do not need an API key, a terminal command, or an application to build. Know only that an assistant generates a response from the information it receives. If opening the assistant is unfamiliar, use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then return here. The goal is to recognize the difference between requesting an action and observing its result.

## The idea in plain language

A **tool** is an operation exposed to an assistant: read a file, search a knowledge base, or run a test. An **API** is an interface through which software requests another component's behavior. A tool can wrap an API, a local function, or a command. A **function call** names an operation and supplies its inputs, also called arguments.

The model does not make a ticket appear by writing “ticket created.” It proposes a call. The surrounding application checks the request, executes an allowed operation, and returns a result. The model can then explain that result. These are separate events, and any one can fail. A familiar SDET analogy is a test that asks a browser to click: the request to click, the browser action, and the assertion about the resulting page are different evidence.

## A small example

Signal Desk has a read-only teaching tool named `lookup_build`. It takes a build ID and returns its status. A proposed request might be:

```json
{"tool":"lookup_build","arguments":{"build_id":"DEMO-42"}}
```

This is a teaching envelope, not a universal provider API format. Suppose the supplied result is `{"status":"failed","failed_tests":2}`. The assistant can report two failing tests. It cannot infer their names, root cause, or whether a later build passed. Those facts were not returned. If the result is missing, the honest status is unknown, even when the proposed request looks perfect.

## Try it with Codex or Claude Code

Open a new conversation and paste this prompt. Everything needed is included; it asks for a demonstration rather than access to your real CI system.

```text
Teach me tool calling using this synthetic example. Do not run tools or
connect to any service. Available operation: lookup_build(build_id), read-only.
Request: lookup_build with build_id DEMO-42.
Supplied result: status failed; failed_tests 2.
Show the proposed request, the application check, the supplied result, and
a final answer in four short steps. Explain which facts are still unknown.
Then repeat with no supplied result. Label both as simulations.
Define any new technical term before using it.
```

Read the four steps slowly. Ask the assistant to explain one unfamiliar word if needed. You do not have to implement anything or produce a diagram to continue.

## What you should see

The demonstration should keep the requested build ID, use only the supplied facts, and distinguish the second run's missing observation. No real build has been checked. In a genuine tool-enabled session, you would additionally inspect the visible tool event and returned data; the assistant's final sentence alone is insufficient. This distinction will help when you later test an AI system that reports actions it never completed.

## If it goes wrong

If the assistant invents test names, point to the supplied result and ask which field supports them. If it tries to connect to a real service, stop that action and restate that this is a conversation-only example. If JSON feels unfamiliar, ask it to translate each key and value into ordinary words. Curly braces simply group named values here.

## Go deeper

Read [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts): the opening comparison and the Tools example only. Stop before implementing a server. It is public reading with no account requirement; MCP is one way to expose tools, not a prerequisite for every tool call. The next topic retains [lesson 07's tool-contract explanation](../../how-to/07.md). The [authority lab](../../labs/03-tool-authority.md) is optional after that explanation.

## Optional practice

Ask your tutor for one fresh synthetic tool request involving a test report and predict what can be claimed before seeing its result. Attempt your interpretation first. Request feedback when ready; do not ask the tutor to supply both the exercise and its solution together.
