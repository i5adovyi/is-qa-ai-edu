# Remote MCP, authentication and authorization

## Start here

Read local MCP first so host, client, server, and transport are familiar. A remote service adds network and identity questions. This lesson uses a fictional endpoint, not an invitation to connect your company systems. Open a conversation using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md). You can understand the complete example without credentials, a subscription, or a server to deploy.

## The idea in plain language

An **endpoint** is the network address a client contacts. **Authentication** establishes an identity. **Authorization** determines what that identity may access. Signing in successfully does not imply permission to read every project or modify every record.

**HTTP** is the request-and-response protocol used by web services. For protected HTTP-based MCP servers, authorization commonly involves **OAuth**, a standard for delegated access: the host obtains permission to act within a defined scope and receives a token. A **scope** describes an allowed category of access; the server must still enforce individual-object and tenant boundaries. A tenant is a separately protected company or workspace. A token is a credential, not ordinary debugging text. Never paste a real one into a learning prompt.

The HTTP authorization flow differs from local stdio credential handling. A local process may receive narrowly scoped configuration through its environment or a host-managed mechanism. Copying a browser login token into a random local server is not a universal solution. Check your actual host and server documentation before configuring either route.

## A small example

Signal Desk's fictional remote service permits project `demo-store` reads. Its connection initially receives HTTP 401, indicating that usable authentication is needed. After an appropriate sign-in flow, the client can request allowed data. A request to another project can still be denied. The user should see an access limitation, not fabricated empty results.

If a previously working connection stops after an hour, possible causes include token expiry, revoked permission, a changed endpoint, or a network fault. These lead to different repairs. Increasing permissions before diagnosing the layer can create a larger problem while leaving the original fault unresolved.

## Try it with Codex or Claude Code

```text
Explain a remote MCP connection using synthetic values only. Do not open a
network connection, change settings, or ask me for a real token.
Host contacts https://mcp.example.invalid/demo. First observation: HTTP 401.
After a hypothetical authorized sign-in, demo-store reads succeed, but another
project is denied. Explain authentication, authorization, scope, endpoint,
token expiry and account mismatch. Show what evidence to inspect for each
failure without printing secrets. Treat the endpoint as deliberately fictitious.
```

Read the explanation as a troubleshooting story. If you later configure a real server, first identify its owner, intended account, required scopes, and the exact documented host setup procedure. This lesson does not authorize new access to your work systems.

## What you should see

The assistant should distinguish connecting to a service, signing in, discovering capabilities, and successfully accessing a specific object. It should name the relevant account or tenant concept without requesting credentials in chat. A useful diagnostic summary preserves status codes and redacted error categories while excluding token values and sensitive document content.

## If it goes wrong

If the assistant says every 401 means a wrong password, ask about missing or expired tokens. If it suggests granting all scopes, restate the read-only task. If the wrong account is selected, reconnect through the host's documented account flow; do not exchange credential files between accounts. If a URL changed, verify the service owner's official endpoint rather than following a link inside untrusted tool output.

## Go deeper

Read [Understanding Authorization in MCP](https://modelcontextprotocol.io/docs/tutorials/security/authorization), beginning with When Should You Use Authorization? and following the flow through token use. Stop before implementation. The reading is public; an actual connection requires an authorized server and account. The [local MCP manual](../../../lab/mcp_lab/README.md) remains an offline alternative for learning message behavior.

## Optional practice

Ask for one redacted, fictional connection failure and choose the first diagnostic check. Try before seeing the explanation. Do not experiment by revoking or expanding real organizational permissions just to reproduce the example.
