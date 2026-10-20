# Lab 09 · Run a real MCP connection

**Stage:** tools and integration. **Time:** 2–3 hours including setup and extension. **Prerequisites:** lesson 08, JSON schemas, a terminal, and Python 3.12 for the optional environment. **Cost:** no model or subscription fee; an initial dependency download.

This lab replaces a missing practical step: you will run an actual MCP client and server in separate processes. You will retain the protocol messages, add a tool, and inspect failures that occur on real timers and operating-system pipes. The synthetic knowledge service has no mutation capability. Its malicious article exists to teach the boundary between returned content and host authority.

The academy's Python 3.9 reference route remains available without installation. Do this lab in its dedicated environment; it is an additional integration gate, not a reason to install SDK dependencies into every earlier exercise.

## Exercise 1 · Establish the connection and follow a request

Follow the [MCP setup manual](../../lab/mcp_lab/README.md#setup). Run the default gate in a fresh directory. Expected result: **13/13**. Then open `messages.jsonl` and annotate:

1. The client's `initialize` request ID and requested protocol version.
2. The response with the same ID, negotiated version, and server capabilities.
3. `notifications/initialized`, which intentionally has no request ID.
4. `tools/list`, including the input and output schemas for `lookup_article`.
5. One `tools/call`, its response ID, structured content, and error flag.

Do not infer success from the presence of a response alone. The wrong-argument call receives a response with `isError: true`; the normal lookup receives a successful structured result. A transport error may produce no tool result at all.

**Deliverable:** the generated evidence directory and a one-page sequence diagram with actual IDs. **Pass:** all 13 baseline assertions pass; every normal request is matched to a response; you distinguish notification, tool error, and transport failure. Record the package and negotiated protocol versions from your own run.

## Exercise 2 · Add and discover a tool

Use the manual's [learner extension commands](../../lab/mcp_lab/README.md#learner-extension). Keep the failing `--exercise` report before editing: the reference server should pass 13 of 16 assertions because it does not implement `list_topics`.

In your copy, add `list_topics` to discovery and dispatch. Its input is an empty object with no additional properties. Its output is an object containing a sorted array of unique topics from the corpus. Declare the output schema. Derive results from the loaded data rather than memorizing the known list. Do not add filesystem, shell, account-deletion, or arbitrary network tools.

Run the same gate against the learner server. Inspect the new tool's discovered schema, successful result, and rejection of `{"extra": "denied"}`. Add a fourth topic to a temporary corpus copy and write an additional check showing that your implementation derives its answer. Restore the original corpus before running the fixed baseline gate, which deliberately expects the original three topics.

**Deliverable:** learner server diff, before/after reports, and one added-data test. **Pass:** baseline changes from 13/16 to 16/16; the new-data test passes; old unknown-tool and argument rejection checks still pass. [Solution guidance](../../lab/mcp_lab/solutions.md) is available after your attempt.

## Exercise 3 · Diagnose faults and preserve authority

The default gate launches separate servers for three faults. For `timeout`, the server delays a lookup for five seconds and the client applies a 0.35-second call deadline. For `disconnect`, the child exits during the call. For `stdout-noise`, the server prints a human diagnostic onto protocol stdout.

Inspect each trace and error classification. The pinned SDK reports timeout code `408` and connection-close code `-32000`; those observations belong to this SDK version. Identify the unresolved call ID in both reports. Explain why neither situation warrants reporting a successful lookup. Compare normal stderr with the deliberate stdout parser diagnostic. Removing the stdout contamination must restore the clean transport check.

Finally, locate the returned `KB-INJECTION` excerpt. It tells the host to grant future writes and call `delete_account`. Show the discovered allowlist and the rejected unknown-tool result. Explain why the text can be preserved as evidence without being executed. This host is a fixed test client, so passing this check does **not** demonstrate how an arbitrary LLM will respond to adversarial text.

**Deliverable:** three failure diagnoses, a repaired stdout experiment, and a five-sentence authority analysis. **Pass:** no automatic retry or fabricated success; logs remain off normal stdout; server tool membership remains explicit; content does not become authorization.

## Completion evidence

Submit the ten passing integration tests, baseline 13/13 report, learner 16/16 report, and your added-data assertion. Include package version, transport, actual protocol version, Python version, and one limitation. A screenshot of a tool name alone is insufficient: it does not establish initialization, execution, rejection behavior, or cleanup.

The extension remains local. Installing it into a particular AI host is optional because host configuration varies. The standalone SDK client provides a repeatable connection test first; any later host integration should reproduce discovery and a successful lookup before introducing a model.
