# Make approvals match the action that actually runs

## Start here

Read permission scopes, injection defenses, and secrets first. You should understand a tool proposal and its possible effect. This advanced topic uses a short text scenario, so no approval service or production system is required. The [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) explains how to open the demonstration in Codex or Claude Code.

Your goal is to distinguish a human reviewing a specific action from a vague “yes” that can be misapplied later.

## The idea in plain language

An **approval** is authorization for a defined action under stated conditions. It should identify what will happen, which resource is affected, the destination, relevant data, and limits. The execution layer must confirm that the proposed action still matches the authorized one when it runs.

The time between review and execution can introduce a **time-of-check/time-of-use** problem: something changes after it was checked. For example, a draft is edited after approval or a recipient changes. The earlier approval should not silently authorize the different action.

An **audit record** connects the proposal, decision, actor, time, policy, actual execution, and observed outcome. Logging “approved” alone does not establish what ran. Audit evidence should avoid unnecessary secrets and personal content while retaining stable operation and version identifiers.

Some actions are already authorized within a task, so asking for confirmation at every harmless step adds noise. Design approvals around meaningful boundaries and consequences. Repeated vague prompts can train a user to click without reading; a concrete preview makes review useful.

## A small example

Signal Desk prepares a fictional status message for a private team channel. The reviewer approves draft version 3 for channel QA-DEMO. Before execution, a worker changes the destination to a public channel and adds a customer log excerpt.

The earlier approval does not cover those changes. A system should compare the current action with the approved version and scope. It can prepare a new reviewable draft, or reject the changed proposal. It should not ask the model to decide that the change is “close enough.”

After a permitted send, a timeout leaves the outcome uncertain. The audit should record that uncertainty and reconcile the operation before retrying. Approval does not prevent duplicate effects by itself.

## Try it with Codex or Claude Code

```text
Teach approval binding with a fictional action; do not send anything.
Approved: draft version 3, destination private channel QA-DEMO,
content a synthetic test summary, one send only.
Current proposal: draft version 4, public channel ANNOUNCEMENTS,
with a customer log excerpt added.
Explain which approved conditions changed and what an execution guard
should compare. Show a minimal audit record with placeholder identifiers,
no sensitive content, and separate approval and execution outcomes.
Then explain how to record a timeout after an otherwise authorized send
without claiming it failed or retrying blindly.
```

Read the explanation before the example record. If it merely suggests another generic confirmation, ask what exact preview the reviewer needs and what prevents a subsequent change.

## What you should see

The answer should bind authorization to scope and version, distinguish proposal from execution, and preserve an unknown outcome honestly. It should not treat a worker's claim that permission exists as authoritative approval evidence.

For a real implementation, test altered arguments, expired decisions, repeated operation IDs, revoked access, and failures in the approval store. Decide what happens when that store is unavailable; silently proceeding may defeat the boundary. The expected behavior depends on the action's policy, which should be explicit before testing.

## If it goes wrong

If approvals are attached only to free-text summaries, important arguments can drift unseen. If a retry creates a fresh identity every time, duplicate protection may not recognize the same intended action. If the audit logs only success, rejected and unresolved attempts disappear from investigations.

If a reviewer cannot understand the preview, reduce it to the destination, effect, meaningful content difference, and reversibility. Keep implementation identifiers available as supporting detail. Do not expose secrets merely to make an approval look complete.

## Go deeper

Read OWASP's [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), Require user approval and Complete mediation. Stop after those sections. Public reading needs no account. The source explains where authorization belongs; the version-bound preview above is this academy's illustrative design.

The retained [review and operations lab](../../labs/15-review-and-operations.md) and [tool contract template](../../../templates/tool-contract.md) connect approval decisions to optional implementation practice.

## Optional practice

Ask your tutor for one approved proposal and one changed execution request. Identify whether the existing approval still applies and what must be checked before any effect. Request feedback after your attempt; do not send a real message as practice.
