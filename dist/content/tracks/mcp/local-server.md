# Follow your first real local MCP connection

## Start here

This topic has two routes. You can inspect the existing files with your assistant, or optionally run the real SDK lab. Reading requires only the academy source in Codex or Claude Code. Execution additionally requires Python 3.12 and the pinned dependencies described in the lab manual. The main portal still runs on Python 3.9+. Follow the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) if you have not opened a project folder before.

## The idea in plain language

The bundled lab launches a client and a server as separate local processes. A **process** is a running program. They communicate through **stdio**: the standard input and output streams connected by the parent program. Normal server stdout carries protocol messages; human diagnostics go to stderr, the separate error/diagnostic stream. Printing an ordinary greeting into the protocol stream can confuse its parser.

An **SDK** is a library that implements protocol details for your program. This lab pins `mcp==1.30.0` so the teaching transcript and failure classifications are reproducible within its documented environment. It uses an initialization exchange followed by tool discovery and calls. Do not assume that this lifecycle describes every future MCP version. Record the actual protocol version in your own run and compare it with the documentation version you read.

## A small example

The lab's `lookup_article` operation reads synthetic content. You can locate its input schema in the server and its invocation in the client before running either. The client asks what tools exist, calls one with a known article ID, and checks the returned evidence. The server has no general shell or filesystem tool exposed through this interface.

That last statement describes the exposed interface, not a sandbox guarantee. The Python server is still a local program running with its operating-system permissions. This is why inspecting a server's source and dependencies matters before launching an unfamiliar package.

## Try it with Codex or Claude Code

Open the academy repository and paste:

```text
Help me inspect my first MCP connection. Read lab/mcp_lab/README.md,
lab/mcp_lab/server.py and lab/mcp_lab/client.py. Do not edit student files,
install packages, run the extension exercise, or show its solution.
First explain how the client starts the server and where lookup_article is
declared. Then show the exact setup section and explain each command, including
which Python environment it uses. Stop before execution and let me choose it.
Distinguish source inspection from an actual successful connection.
```

For the optional execution route, follow the manual's [Setup section](../../../lab/mcp_lab/README.md#setup) in order, using its dedicated environment and a fresh evidence directory. Ask the assistant to explain an error before proceeding. You do not need to complete the separate extension assignment to learn from the baseline.

## What you should see

Source inspection should identify discovery, dispatch, and the client call. An executed baseline should produce a report and message transcript; the retained lab documents a 13-check baseline. Inspect your actual result rather than copying that expected count into a report. Match one request ID to its response and identify whether the response represents success or a tool error. Merely finding a tool name in a menu proves less.

## If it goes wrong

If Python 3.12 is missing, stay on the inspection route or follow the setup manual; do not replace the system interpreter. If the SDK import fails, check that installation and execution use the same virtual environment. If the server appears to wait silently, remember that stdio servers expect a client, not typed conversational input. If a log breaks parsing, inspect stdout versus stderr before changing schemas.

## Go deeper

Read [MCP Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture), focusing on transport and comparing its version with your transcript. Stop before implementing a new server. The [full local lab](../../labs/09-real-mcp.md) remains optional practice. No model key is required for the bundled deterministic client; this does not certify behavior inside every AI host.

## Optional practice

Before a single baseline call, predict which request and result will appear. Run it if you chose setup, then compare. Ask for one hint if stuck; keep the lab's extension solution hidden until you attempt that separate task.
