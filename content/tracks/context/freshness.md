# Check whether evidence is still true

## Start here

You can select and compact evidence. Now learn to recognise a subtler failure: the source is real, but it no longer applies. This happens with cached tool results, old policies, previous test runs, copied setup commands, and assistant handoffs. The question is not just “Do I have a citation?” but “Does it support this claim now?”

## The idea in plain language

**Provenance** describes where information came from. **Freshness** concerns whether it is current enough for the decision. **Applicability** concerns whether it matches the relevant version, environment, account, and scope. A source can be recent but inapplicable, or old but still valid for a historical question.

An **invalidation trigger** is an event that makes you recheck a previously accepted fact. A code change can invalidate an earlier test result. A policy revision can invalidate a cached answer. A user’s permission change can invalidate a retrieval result that was once allowed. Merely adding a timestamp does not keep a fact fresh.

For important claims, keep the source identifier, relevant date or revision, scope, and observation method. “Tests passed” is weaker than identifying the executed command and the code revision it tested. A date without a version may not tell you whether a deployed system matches the tested source.

## A small example

Signal Desk has policy P7 from Monday: “Refund requests can be submitted within 14 days.” A new P8 becomes effective Thursday and says 30 days. On Friday, an assistant cites P7 accurately. The quote is real but may be wrong for a new Friday request.

For a question about a request made last Tuesday, P7 might still be the relevant source, depending on the policy’s transition rules. You cannot decide only by choosing the newest document. You need the question’s effective date and applicability. If the transition rule is absent, the answer should expose that uncertainty.

Likewise, a green test run on commit A does not prove commit B passed after a later change. The old result remains historical evidence; it simply supports a narrower claim than “the current project is verified.”

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Teach freshness using synthetic policies. P7: Monday, 14-day window.
P8: effective Thursday, 30-day window. Today is Friday.
Question 1 concerns a new Friday request. Question 2 concerns last Tuesday.
No transition rule is supplied. Explain which source might apply and what
must remain unknown. Then compare a passing test on commit A with changed
code at commit B. Do not invent a policy transition or claim tests ran.
Name an event that should trigger rechecking each kind of evidence.
```

You may answer the source questions verbally. The point is to track the conditions that make evidence useful, not to create another spreadsheet. In real work, preserve exact dates and versions instead of the relative words used in this small example.

## What you should see

The assistant should distinguish the Friday request from the historical one and preserve the missing transition rule. It should not say that every old source is wrong or that a timestamp alone proves applicability. For tests, it should connect the evidence to the actual revision and scope checked.

## If it goes wrong

If the assistant mixes old and new rules, ask it to attach each claim to a source and effective period. If a cached answer survives a permission change, ensure the retrieval system rechecks access before reusing it. If you cannot verify a volatile fact, label it unverified rather than presenting the last known value as current. Stable conceptual definitions do not need the same refresh frequency as live deployment state.

## Go deeper

Read the definition and benefits in Google’s [Grounding overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview). Stop before notebooks or product choices. It explains connecting output to verifiable sources; this academy’s example adds the practical question of applicability. The retained [handoff guide](../../how-to/06.md) applies those checks to resumed work.

## Optional practice

Ask your tutor for three claims with source dates, versions, and a current question. Identify one safe claim, one stale claim, and one unresolved claim before receiving feedback. No policy document or formal audit report is required.
