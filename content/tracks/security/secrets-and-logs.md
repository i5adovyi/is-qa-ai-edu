# Debug an AI workflow without leaking its data

## Start here

Read permission scopes and injection defenses first. No secret manager or logging platform is needed for this lesson. Open your usual assistant conversation and use only the synthetic fields below. If you need help opening the conversation, follow the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md).

Your goal is to keep enough evidence to diagnose behavior while avoiding unnecessary exposure. A detailed trace can be useful and still be unsafe to upload unchanged.

## The idea in plain language

A **secret** is a value that grants access or protects information, such as an API token, password, or private key. **Personal data** identifies or relates to a person. **Redaction** removes or replaces sensitive content before a record leaves its permitted location. **Retention** specifies how long a record is kept and how it is removed.

An AI workflow may copy information across prompts, tool requests, responses, traces, error messages, screenshots, and generated files. Removing a token from the final answer does not remove earlier copies. The destination also matters: a private repository is still an external location, and an access token can remain dangerous in old commits after a later edit removes it.

Use references when content is unnecessary. A trace can record a request ID, tool name, outcome, duration, input schema version, and permitted metadata without including the full customer message. Some investigations need more detail, but that should be an explicit, limited decision with appropriate access and expiry.

## A small example

Signal Desk has this fictional log entry:

```text
request=demo-81 tool=lookup_ticket duration_ms=240 status=403
authorization=DEMO-NOT-A-REAL-TOKEN
customer_email=person@example.invalid
ticket_text=My private contract number is DEMO-999
```

To investigate the permission failure, the tool, status, request ID, policy decision, and sanitized account scope may be enough. The token and entire ticket text do not explain why authorization was denied. The correct next evidence might be a permission-rule identifier, not a larger dump of customer content.

The placeholder token is deliberately fake. Do not replace it with a real credential to make the demonstration “more realistic.”

## Try it with Codex or Claude Code

```text
Review this fictional log only; do not inspect my environment or files.
request=demo-81 tool=lookup_ticket duration_ms=240 status=403
authorization=DEMO-NOT-A-REAL-TOKEN
customer_email=person@example.invalid
ticket_text=My private contract number is DEMO-999
Explain which fields help diagnose the permission failure, which should
be omitted or redacted before sharing, and what additional non-secret
evidence would help. Show a sanitized example using placeholders.
Then explain why deleting a token from the latest file is insufficient
if a real token was already committed or uploaded. Do not invent a leak.
```

Check that the assistant works only with supplied data. It does not need your environment variables, shell history, or actual account settings to teach this concept.

## What you should see

The response should preserve useful operational fields while removing sensitive values. It should distinguish sanitizing a record from revoking an exposed credential. Revocation or rotation changes whether a credential works; deleting a local copy does not. Any real exposure response must use the provider's current process and your organization's authority.

Also consider who can read traces, whether exports are encrypted appropriately, and how long they remain available. A hash or shortened value is not automatically anonymous; predictable identifiers may still be linkable. Logging design is part of the application, not an afterthought added when something breaks.

## If it goes wrong

If the assistant asks for a real key to diagnose this example, continue with placeholders. If redaction destroys every useful field, preserve stable non-secret correlation IDs and error categories. If a checker scans only the final response, include intermediate logs and generated artifacts in the controlled test.

If an actual credential is exposed, stop propagating it and follow the owner's revocation process. Do not paste it into another assistant to ask whether it looks valid. Keep personal academy progress and chat transcripts outside shared course source and uploads.

## Go deeper

Read OWASP's [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), Event attributes and Data to exclude. Stop before Customizable logging. Public reading needs no account. Focus on choosing fields; implementing a production logging system is outside this demonstration.

The [local data guide](../../../docs/LOCAL-DATA.md) applies the same separation to your academy progress. The retained [traces and diagnosis lab](../../labs/07-traces-and-diagnosis.md) is optional practice with controlled fixtures.

## Optional practice

Ask your tutor for one synthetic trace with a different unnecessary sensitive field. Propose the smallest useful sanitized record, then request feedback. Do not submit real logs until you have separately checked whether sharing them is authorized.
