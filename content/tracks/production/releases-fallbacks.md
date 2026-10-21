# Release an AI change with a way to stop and recover

## Start here

Read evaluation regressions, service reliability, and incident response first. You should understand a baseline and a measured success condition. This lesson is an explanation using synthetic release records, not a request to deploy anything. Open Codex or Claude Code and follow the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) if needed.

Your goal is to connect evidence before release with controlled observation after release. An offline evaluation cannot fully predict live inputs, dependencies, and operational load.

## The idea in plain language

A **release** changes what users actually receive. In an AI system, behavior can change through code, a prompt, model selection, tool definitions, retrieval data, permission policy, or configuration. Treat those as release inputs, not invisible details.

A **canary** exposes a change to a limited share of appropriate traffic for a bounded observation period while comparing it with a control. **Shadow mode** runs a candidate alongside normal processing without letting its proposed actions affect users. Shadow execution can still incur costs and send data to providers, so its data access and tool effects need explicit design.

A **fallback** is an alternative behavior when the normal path is unsuitable, such as routing to human review or returning a limited answer. A **rollback** restores a prior operating version. Neither automatically reverses completed external actions. A fallback model must still obey the same tool and privacy boundaries; a cheaper or older model is not inherently safe.

## A small example

Signal Desk changes its summary prompt from p8 to p9 while also replacing retrieval snapshot s4 with s5. A canary shows more unsupported policy claims. Rolling back only p9 leaves the new retrieval snapshot in place, so the behavior may persist.

A useful release identity includes both prompt and source snapshot, along with relevant model and tool configuration. Before release, the team decides which signals stop expansion: unsupported claims, permission failures, timeouts, and cost beyond an agreed limit. The team also identifies which prior combination can be restored and checks that it remains compatible with stored state.

These are fictional choices for teaching. Production targets depend on the service and should be established before observing whether the candidate happens to pass them.

## Try it with Codex or Claude Code

```text
Explain a synthetic AI release; do not deploy or change files.
Baseline: prompt p8, retrieval snapshot s4, tool schema t2.
Candidate: prompt p9, retrieval snapshot s5, tool schema t2.
Canary observation: more unsupported policy claims; causes unknown.
Explain what belongs in the release identity and why reverting only the
prompt may be insufficient. Describe control, canary, shadow mode,
fallback, and rollback in plain language. State what evidence would stop
expansion, what to inspect next, and why rollback cannot undo past sends.
Do not invent a successful recovery or claim the cause is established.
```

Check whether the assistant separates containment from diagnosis. Stopping expansion can be sensible while the cause remains unknown. Naming a plausible cause is not the same as reproducing it.

## What you should see

The response should preserve the complete configuration, compare like-for-like traffic where possible, and describe observable stop conditions. It should avoid treating every traffic difference as a model effect: customer mix, time of day, and upstream changes can confound the comparison.

It should also mention state compatibility. If a new release writes a different database format or action record, an old version may not read it safely. Practice restoration in an isolated environment before relying on it. Keep a clear owner for stopping, rolling back, and confirming recovery with actual evidence.

## If it goes wrong

If “shadow” workers still call mutating tools, the mode is not safely isolated from effects. If a fallback bypasses approval checks, it defeats the boundary precisely during failure. If rollback simply reselects a model name without restoring prompt and source state, record the remaining changes explicitly.

If the canary has too few relevant cases, extend or redesign observation rather than declaring success from silence. If monitoring is unavailable, follow the predeclared release rule; absence of evidence is not a clean bill of health. Do not erase failure records after recovery, but sanitize and retain them according to policy.

## Go deeper

Read Google SRE's [Canarying Releases](https://sre.google/workbook/canarying-releases/), the introduction, Release Engineering Principles, and Balancing Release Velocity and Reliability. Stop before the detailed canary implementation discussion. Public reading requires no account. The source addresses services broadly; the prompt-and-retrieval scenario is this academy's AI-specific application.

The retained [review and operations lab](../../labs/15-review-and-operations.md) offers optional controlled practice. Continue to the [capstone lesson](../../how-to/24.md) when you want to combine the tracks in a small project.

## Optional practice

Ask your tutor for one fictional release with a changed tool schema and an old checkpoint. Identify one compatibility check and one stop condition before requesting feedback. No live rollout, formal document, or incident debrief is required.
