# Cite evidence and know when to abstain

## Start here

You can explain chunking and candidate retrieval. Now learn the final step: producing an answer that the retrieved evidence actually supports. A citation is helpful only when its source backs the associated claim. This lesson also teaches when an honest partial answer is better than filling a gap.

## The idea in plain language

**Grounding** connects a model’s output to verifiable information. A **citation** identifies the source supporting a claim. **Faithfulness** asks whether the answer stays consistent with that evidence. These checks are different from asking whether the answer sounds useful or happens to be true for another version.

**Abstention** means declining to make a claim that the available evidence cannot support. It can be partial: answer the supported part and explain what remains unknown. A useful abstention identifies the missing evidence or next check. It need not be a vague refusal to help.

Check four things: the cited source exists; it contains the relevant statement; that statement applies to the question; and the answer does not add unsupported details. A real URL can accompany a false claim. A correct quotation can still be applied to the wrong account, date, region, or product version.

## A small example

Signal Desk asks: “Can a trial account upload a 12 MB attachment to an archived ticket?” Source A says trial accounts have a 5 MB attachment limit. Source B says archived tickets do not accept new attachments. Neither source says why a particular failed request returned 403.

The policy question can be answered with both constraints. A separate claim that “the 403 was caused by the size limit” would go beyond those sources without execution evidence or documented error mapping. The assistant should distinguish policy incompatibility from the observed implementation’s causal explanation.

If only Source A was retrieved, it could explain the size constraint and say that archived-ticket behaviour is not established by the supplied evidence. It should not invent Source B merely because that rule seems plausible. This is a useful partial answer and a clear retrieval next step.

## Try it with Codex or Claude Code

Open chat through the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Teach grounded answers with synthetic evidence only.
Question: Can a trial account upload 12 MB to an archived ticket?
Source A, policy-v2: trial attachment limit 5 MB.
Source B, policy-v2: archived tickets accept no new attachments.
Observed request returned 403; no error mapping or trace is provided.
Answer the policy question with source IDs beside supported claims.
Explain why the exact cause of 403 is still unverified. Then show how the
answer should narrow if Source B is unavailable. Do not invent citations.
```

Read each sentence and point to the evidence supporting it. This simple action is more informative than asking the assistant to assign itself a confidence score. A confident numerical score without calibration does not replace checking the source.

## What you should see

The answer should cite A for the size rule and B for the archived state. It should avoid claiming a confirmed runtime cause. With B missing, it should preserve the known size limit while making the archive rule unresolved. It should not turn a citation into permission to expose another user’s private source.

## If it goes wrong

If the citation points to a whole manual, ask for the relevant passage or section. If the source contradicts the answer, fix the claim rather than merely replacing the link label. If the answer is unsupported because retrieval missed evidence, investigate retrieval separately from generation. If sources conflict, preserve their versions and scope instead of synthesising a rule neither contains.

## Go deeper

Read the definition and auditability benefits in Google’s [Grounding overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview). Stop before product integration choices and notebooks. The reading needs no Google Cloud account. The academy’s [grounding and evaluation lab](../../labs/06-grounding-and-evaluation.md) provides optional practice with explicit support checks.

## Optional practice

Ask your tutor for three short sources and an answer containing one unsupported addition. Identify which claim needs correction and whether to retrieve more evidence or abstain. Submit your reasoning before asking for feedback. Do not open an incident debrief to obtain the answer.
