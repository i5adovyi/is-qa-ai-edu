# Tools, MCP, and skills without the jargon pile

These terms describe different parts of an assistant's working environment. Understanding the difference makes product documentation much easier to follow.

## A tool performs an operation

A tool might read a file, query a test result, or run a command. The model can propose a tool call with arguments. Application code decides whether the call is permitted, executes it, and returns a result. A valid request is not proof that execution succeeded. Permission denial, invalid arguments, network failure, and stale data are separate outcomes.

For an SDET assistant, a read-only tool that returns the last failed CI job has a narrower consequence than a tool that can rerun deployments. Access should match the actual task. An instruction such as “be careful” does not replace enforcement in the tool or host application.

## MCP connects hosts to capabilities

The Model Context Protocol, or MCP, defines how a host connects through a client to a server exposing capabilities such as tools, resources, and prompts. It is a protocol for integration. It does not make a tool trustworthy, approve its use, or guarantee a model will call it correctly.

For example, an MCP server could expose a tool for fetching test-run details. You still need to understand which credentials it uses, which projects it can access, what its returned data means, and how errors appear. Those are normal integration-testing questions.

## A skill supplies reusable instructions

A skill packages instructions and potentially supporting files or scripts for a recurring task. It might explain how your team reviews a test change or interprets a particular trace format. Hosts differ in how they discover, load, and run skills. Having a file installed does not prove the assistant loaded or followed it.

A useful distinction: a skill describes how to carry out a kind of work; a tool provides an operation the assistant can request; MCP can connect that tool to the host. Skills can refer to tools, but they are not interchangeable. Plugins may bundle capabilities for installation, while hooks run at particular lifecycle events in hosts that support them.

## Learn the vocabulary before installation

The Hugging Face course below brings these ideas together across several coding agents. Read its skills and MCP explanations first. Its hands-on route assumes Python, a terminal, and a configured coding agent. You can defer installation until you choose a tool and a real use case.

The existing real MCP and skill-installation labs remain available under optional practice. Next, see how an agent selects and combines tool calls over multiple steps.
