# Give an assistant only the access its task needs

## Start here

Read trust boundaries first. This lesson explains access design without asking you to change your machine's security settings. You need an existing Codex or Claude Code conversation and the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md). The example is a paper review of fictional permissions; it does not modify your real assistant configuration.

Your goal is to identify unnecessary capability before it causes an unintended action. “The assistant is helpful” is not an access-control policy.

## The idea in plain language

A **permission scope** describes the resources and operations an identity may use. “Read one project” is narrower than “read all projects.” “Create a local draft” differs from “send a message.” **Least privilege** means granting the access needed for the current job, rather than every capability the account could obtain.

A **sandbox** restricts execution, such as filesystem writes, process access, or networking. Its actual boundaries depend on the product and configuration. The word “sandbox” does not prove that credentials are absent, network access is disabled, or all effects are reversible. Inspect the documented configuration and verify relevant behavior in a disposable environment when needed.

Permissions can exist at several layers: assistant tools offered to the model, local process restrictions, credentials used by a connector, and the destination service's own checks. Hiding a tool from a prompt is not the same as revoking its backend permission. An approval dialog is also different from a service refusing an unauthorized operation.

## A small example

Signal Desk wants a daily summary of synthetic CI failures. The workflow needs to read selected job results and produce a local draft. A proposed connector additionally grants repository deletion, secret administration, and posting to every team channel.

Those extra powers do not improve the summary. If the model misinterprets a log line or a tool has a defect, the unnecessary access increases the possible damage. A narrower configuration reads the designated CI results and writes only the draft. Sending the draft is a separate action with its own destination and authorization.

The draft directory also matters. Permission to write one working folder should not be assumed to allow edits anywhere on the machine.

## Try it with Codex or Claude Code

```text
Review fictional permissions; do not inspect or alter my actual settings.
Task: summarize CI failures from project DEMO into a local draft folder.
Proposed access: read DEMO CI results, read all organization secrets,
delete repositories, write drafts in work/demo, send messages to all channels.
For each permission explain whether the stated task needs it and why.
Explain the differences among a tool being available, sandbox restrictions,
connector credentials, and destination authorization. Define each term.
Finish with one small synthetic check that would reveal excess access,
without executing anything or providing destructive commands.
```

You should be able to follow the review without knowing a specific provider's permission syntax. Product-specific configuration comes later, using current official documentation for the host you actually use.

## What you should see

The review should connect each permission to an explicit task requirement. It should identify the draft location and selected project as meaningful scope. It should also recognize that reading secrets is unnecessary even if the assistant claims it will not print them.

In real validation, a useful negative test checks that an attempted access outside the allowed scope is rejected by the enforcing component. A message saying “I shouldn't do that” is weaker evidence than a backend denial. Both model behavior and system enforcement can be evaluated, but label them separately.

## If it goes wrong

If a setup guide suggests disabling restrictions to fix a tool error, first identify the exact failed operation and smallest missing permission. If the task needs only reading, a write permission error may indicate that the wrong tool was selected.

If the assistant proposes one global administrator credential for convenience, ask how separate users and projects remain isolated. If the term “read-only” appears, ask whether indirect effects such as network calls, audit entries, or expensive queries matter for the task. Scope is about actual behavior, not a friendly label.

## Go deeper

Read OWASP's [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), Common Examples of Risks and the first four Prevention and Mitigation Strategies. Stop before user-approval guidance, which appears later in this track. Public reading requires no account or live environment.

The [tool contract template](../../../templates/tool-contract.md) can help record a boundary when you choose to implement one. Continue to [injection defenses](injection-defenses.md) to see how untrusted content can attempt to misuse available powers.

## Optional practice

Ask your tutor for one new fictional task and a mixed list of permissions. Choose the smallest sufficient set before requesting feedback. You can answer in a few lines; changing your real account is unnecessary.
