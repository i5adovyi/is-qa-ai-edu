# Find the layer that broke

## Start here

You have followed a local connection and learned how remote access differs. Now use an SDET habit: reproduce one fault, identify the earliest failing boundary, and change one variable. The [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) supports a reading-only route. The optional bundled lab requires its own Python environment; the MCP Inspector is a separate tool with its own current Node requirement. Neither is required to continue reading.

## The idea in plain language

An MCP integration has several observable layers. Process startup can fail before messages exist. Transport can connect but carry malformed data. Protocol discovery can succeed while a particular tool is unavailable. A valid tool call can fail because its arguments or underlying operation are rejected. A successful result can still be irrelevant to the user's question.

**Diagnosis** means identifying which explanation the evidence supports. Request IDs, timestamps, exit status, discovered schemas, and redacted error fields help. A screenshot of “connected” is weak evidence for execution. Conversely, a failed business operation does not automatically imply that the connection is broken.

Version differences matter. A failure code observed with the academy's pinned SDK belongs to that SDK and test case. A newer server or transport may report a different code or lifecycle. Compare documented behavior and actual messages rather than memorizing a number as the universal meaning of a failure.

## A small example

Consider three fictional observations. First, the server process exits before discovery. Second, discovery works but a call supplies an undeclared argument. Third, a valid call is sent and no response arrives before the caller's deadline. These suggest startup, contract, and timing investigations respectively.

A fourth case is subtler: the tool returns a document from the wrong project. The transport and schema may work perfectly while the application violates scope. SDETs need both integration checks and semantic checks. Fixing the connection will not fix the wrong-project result.

## Try it with Codex or Claude Code

```text
Act as my MCP troubleshooting tutor. Use only these synthetic observations:
A: child process exits before discovery; stderr says module unavailable.
B: tools are listed; lookup rejects an unexpected argument.
C: a request was sent; no result arrived before the client deadline.
D: a successful-shaped result contains a different project's document.
For each, identify the likely layer and one next observation, not a speculative
fix. Explain request ID, stderr and deadline. Do not install or run anything.
Then explain how I could inspect one real baseline trace in lab/mcp_lab without
opening the extension solution or pretending it has already passed.
```

If you have run the baseline, let the assistant read only the relevant redacted excerpt from your evidence directory. Preserve the original record and distinguish its observation from the fictional examples above.

## What you should see

The assistant should propose checking the active interpreter for case A, the actual declared contract for B, timing and outcome uncertainty for C, and project scope for D. These are teaching examples, not answers to the retained extension assignment. A useful investigation stops once it has a specific hypothesis and a check; it does not rewrite the whole server immediately.

## If it goes wrong

If it repeatedly retries a timed-out write, return to the Tools track's side-effects topic. If logs contain human text on protocol stdout, keep diagnostics on stderr in a disposable server copy. If the assistant recommends upgrading all dependencies, first reproduce under the documented pinned environment. Changing several versions at once removes your comparison baseline and can hide the original cause.

## Go deeper

Read the [MCP Inspector introduction and Quickstart](https://modelcontextprotocol.io/docs/tools/inspector), then stop before choosing a client guide. Public reading is enough. Optional execution downloads software and requires the documented Node version; inspect that requirement first. The [real MCP lab](../../labs/09-real-mcp.md) already includes controlled timeout, disconnect, and stdout-noise scenarios with explicit evidence boundaries.

## Optional practice

Choose one lab fault only after the normal baseline works. Predict the first observable difference, run into a new private evidence directory, and ask your tutor to check your diagnosis. Keep unrelated faults unchanged so the comparison teaches something.
