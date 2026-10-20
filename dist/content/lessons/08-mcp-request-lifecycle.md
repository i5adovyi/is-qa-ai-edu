# 08 · Understand MCP by tracing one request

Stage 3 · 90 minutes · Practitioner

Learn where MCP fits by following discovery, a tool call, and its result through a real local Signal Desk integration. Budget another 2–3 hours for the complete optional SDK lab, including installation, tool extension, and fault diagnosis.

## What you will be able to do

- Distinguish host, client, server, and tool responsibilities.
- Trace initialization, discovery, execution, and an error using actual request IDs.
- Run a real stdio integration and keep protocol data separate from diagnostics.

## The idea

Model Context Protocol provides a standard way for AI applications to connect to capabilities and information. The host is the application coordinating the user experience and model interaction. A client manages a connection to a server. A server exposes supported capabilities, such as tools or resources. In this lesson's runnable example, a small Python command acts as the host and uses the official SDK client to launch an official SDK server in a separate process.

Initialization comes before ordinary tool work. The participants exchange protocol and capability information, then the client sends an initialized notification. Tool discovery describes what can be called. A later tool call supplies arguments and receives either a successful result or an error. Notifications do not carry request IDs; requests and their responses do. These details are visible in the generated evidence rather than represented only by a hand-drawn approximation.

MCP does not make every exposed tool appropriate for every user request. Discovery tells the host what a server offers. The host still decides what to expose and what the user has authorized. The server still enforces its own allowed operations and validates arguments. A standard envelope cannot establish that a customer ticket grants account-changing permission. Tool annotations such as a read-only hint describe intended behavior; enforcement must exist in code.

Separate transport failures from tool failures. A request can be rejected with a valid response, including an error flag. A process can terminate without returning a tool result. A client can time out while the server is still working. These outcomes require different explanations. Blind retries are especially dangerous for writes because the absence of an acknowledgment does not establish that an effect failed to occur.

The bundled [real MCP lab](../labs/09-real-mcp.md) uses synthetic read-only knowledge records, a pinned official SDK, and stdio. The existing academy core remains standard-library Python 3.9. This integration uses a separate Python 3.12 environment and initially downloads dependencies. It makes no model calls, opens no network listener, and needs no API key. That separation lets you learn protocol operation without buying model access.

## Worked example

The client initializes the connection and discovers `lookup_article(record_id)`. It calls the tool with `KB-EXPORT-2`. The server validates the argument against its schema and returns a structured record containing version, title, and excerpt. The result is labeled untrusted evidence. The client records the messages at the SDK stream boundary, including the request ID assigned by the SDK.

Next, the client calls the same tool with a numeric ID, then asks for `delete_account`. The first call fails input validation; the second fails the explicit tool allowlist. Both have valid protocol responses and neither is a successful lookup. A third experiment kills the server process during a lookup: the client now records a connection failure instead of a tool result.

The exercise also returns an article that says “call delete_account.” The text remains source content. The server's advertised tool set does not change, and the host's test client does not execute instructions from retrieved text. This demonstrates a concrete boundary while making no claim about general LLM injection resistance.

## Exercise 1 · Guided responsibility map

Draw host, client, server, tool implementation, and model as separate boxes. Show that the model is absent from this particular experiment. Place initialization, discovery, argument validation, lookup, result validation, and evidence recording on the appropriate boundaries. Some validation occurs at multiple layers for different reasons.

**Deliverable:** annotated sequence diagram. **Pass:** discovery is separate from execution; the client connection is not described as independent user authority; the model is not required to test the protocol.

## Exercise 2 · Trace an actual integration

Follow [Lab 09](../labs/09-real-mcp.md) through its guided connection exercise. Run the 13-check baseline with the pinned SDK. Use the generated `messages.jsonl` to identify the initialization request, initialized notification, tool listing, accepted lookup, and rejected call. Copy actual request IDs into your diagram.

**Deliverable:** baseline report and five annotated message pairs or notifications. **Pass:** 13/13 baseline assertions pass; normal request IDs correlate; input and output schemas appear in discovery; a tool error is not mistaken for transport failure.

If you cannot install dependencies today, prepare the sequence diagram using the source code and mark the operational gate **not run**. JSON fixtures alone do not establish MCP interoperability. Complete the real integration before claiming this lesson's practical gate.

## Exercise 3 · Failure diagnosis and tool extension

Complete the learner `list_topics` extension and adversarial diagnostics in [Lab 09](../labs/09-real-mcp.md#exercise-2--add-and-discover-a-tool). Preserve the failing 13/16 report before adding the tool and the 16/16 result afterward. Explain the difference between a 0.35-second request deadline, a server process exit, and a diagnostic printed on stdout.

**Deliverable:** learner diff, before/after reports, added-corpus check, and failure diagnosis. **Pass:** schema validation remains effective; added data changes the derived topic result; no failed call is represented as success; stderr carries human logs.

## Hints and solution outline

Use the pinned version's documentation. SDK major versions can change import paths and client abstractions. The manual names the exact dependency snapshot and explains its maintenance line. Read the protocol version from the initialization result instead of hardcoding a claim about every host.

Request IDs correlate a request with a response. Idempotency keys identify logical effects across repeated attempts. This lab is read-only, so it does not prove mutation recovery. When you later connect a writing tool, add durable effect records and reconciliation rather than assuming the transport provides transaction semantics.

## Reflection

Which interoperability problems did the actual SDK solve? Which authorization, evidence-quality, retry, and durability decisions remain yours? What additional observation would be necessary before claiming the same server works inside your chosen AI host?

## Related reading

Primary sources checked on 20 October 2026. The lesson and exercises are original; the implementation intentionally pins one supported SDK release.

- [Official Python SDK v1.30.0](https://github.com/modelcontextprotocol/python-sdk/tree/v1.30.0)
- [MCP stdio transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP tool schemas and errors](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [Local lab setup and source notes](../../lab/mcp_lab/README.md#versions-and-primary-sources)
