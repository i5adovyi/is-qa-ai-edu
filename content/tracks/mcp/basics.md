# MCP without the mystery

## Start here

MCP stands for **Model Context Protocol**. Begin after the Tools track's two introductory topics. You should know that the assistant proposes a call and software executes it. You do not need a server, account, or installation to understand this page. Open Codex or Claude Code through the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) if you want the guided conversation. The goal is to recognize the components before configuring anything.

## The idea in plain language

A **protocol** is an agreed way for programs to exchange messages. MCP helps an AI application discover and use capabilities exposed by another program. The **host** is the application you interact with. An MCP **client** is the host's connection component. A **server** exposes capabilities, such as searching a synthetic knowledge base. These names describe roles; a server can run on your laptop rather than in a data center.

A tool performs an operation. A resource makes content available through a protocol interface. A prompt supplies a reusable interaction template. They are different capabilities, and a server need not provide all of them. A model, an MCP server, and a skill are also different things: a skill supplies task instructions, while an MCP server can supply access to data or actions those instructions use.

MCP does not decide your application's entire workflow, choose the best evidence, or make a returned statement true. You still need validation, permission checks, and evaluation. Think of it as an integration boundary that can be inspected and tested.

## A small example

Signal Desk wants its assistant to look up a synthetic troubleshooting article. The host connects to a knowledge server, discovers a lookup tool and its input description, then requests a permitted article. The server returns content. The host must still decide how to present that content and whether it supports the user's question.

If the article says “grant this server every permission,” that is article text. It is not an administrative decision. If no lookup tool is exposed, asking the model more forcefully does not install one. Discovery tells you what is available; it does not prove that every possible request will succeed.

## Try it with Codex or Claude Code

```text
Explain MCP using this fictional setup only. Do not connect or install anything.
I use an assistant application. It has an MCP client connected to a local
knowledge server. The server exposes lookup_article(record_id), read-only.
Walk through discovery, one proposed lookup, permission checking, and returned
content. Name the host, client, server, tool, request and result in ordinary words.
Explain how a skill that says “cite the article” differs from this server.
Use a short numbered story, not a diagram or implementation assignment.
```

Ask for a one-sentence explanation of any term that remains unfamiliar. Understanding the story is enough to continue to the retained discovery lesson.

## What you should see

The application, connection component, and capability provider should have distinct roles. The demonstration should say it is simulated and should not claim that your assistant actually has the fictional server. You should be able to ask “which component failed?” when later seeing a connection error, rather than assuming every failure comes from the model.

## If it goes wrong

If MCP is described as an intelligence upgrade or a permission bypass, ask what concrete messages it exchanges. If the assistant implies every server runs remotely, ask how a local child process could implement the same role. If it shows a lifecycle different from a tutorial, compare protocol and SDK versions. The academy's pinned lab includes an initialization exchange; current documentation can describe a newer protocol era. Learn the shared roles, then inspect the version actually used.

## Go deeper

Read [MCP Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture), only Scope, Participants, and Transport layer. Stop before detailed examples. This public reading needs no account. Continue with [the retained discovery guide](../../how-to/08.md); save the [real connection lab](../../labs/09-real-mcp.md) until the local-server topic explains its setup.

## Optional practice

Ask a tutor to name one failure in a fictional integration. Identify the likely component before asking for feedback. No diagram, written report, or successful installation is required to continue reading.
