# Check retrieval, evidence, and the final answer separately

## Start here

Read the evaluation basics and dataset lesson first. You should know that **retrieval** means finding source material for a question. You do not need a vector database or a working RAG application. This demonstration uses three short pieces of text in an ordinary assistant conversation; the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) provides the entry steps.

Your goal is to identify where an answer went wrong. “The chatbot hallucinated” is too broad to tell an SDET whether to test search, source freshness, or answer generation next.

## The idea in plain language

**Retrieval-augmented generation**, or **RAG**, supplies retrieved material to a model before it answers. Three different checks matter. Retrieval coverage asks whether the necessary evidence was found. **Faithfulness** asks whether the answer's claims are supported by the material actually supplied. Task correctness asks whether the final answer meets the real requirement using authoritative, applicable information.

These checks can disagree. A model may faithfully repeat an obsolete policy. It may answer correctly from prior knowledge while citing an irrelevant document. Neither case establishes that your retrieval system works reliably.

Evidence also needs identity and scope. A refund rule for one plan, country, tenant, or date may not apply to another. A citation is a pointer, not proof. Open the cited passage and check whether it supports the exact claim. When permission filtering excludes a document, correctness does not justify leaking it.

## A small example

Signal Desk's invented policy collection contains:

- P1, current, Basic plan: “Audit exports are retained for 7 days.”
- P2, current, Team plan: “Audit exports are retained for 30 days.”
- P3, retired, Team plan: “Audit exports are retained for 14 days.”

A Team customer asks how long their audit export remains available. Run A retrieves P1 and answers 7 days with a P1 citation. It uses its evidence faithfully but retrieves the wrong plan. Run B retrieves P2 and answers 60 days. Retrieval succeeded; generation introduced an unsupported value. Run C retrieves only P3 and answers 14 days. The claim matches its evidence, but freshness handling failed.

These are synthetic teaching cases. They are not real product policies, and you should not test them against a customer's environment.

## Try it with Codex or Claude Code

Paste this prompt. You may keep the original text visible while reading the assistant's response.

```text
Explain three different RAG failures using only these synthetic policies:
P1 current Basic plan: audit exports retained for 7 days.
P2 current Team plan: audit exports retained for 30 days.
P3 retired Team plan: audit exports retained for 14 days.
Question: How long is a Team customer's audit export available?
Run A retrieved P1 and answered 7 days, citing P1.
Run B retrieved P2 and answered 60 days, citing P2.
Run C retrieved P3 and answered 14 days, citing P3.
For each, separate retrieval coverage, claim support, and applicability.
Explain the smallest component to investigate, without inventing logs.
Then show how an honest answer should behave when no applicable source
is available. Do not browse, create files, or implement a RAG system.
```

Ask the assistant to point to the exact words establishing plan and freshness. If it collapses everything into “bad answer,” request the three separate judgments again.

## What you should see

You should see why improving the prompt alone cannot repair missing or wrongly scoped evidence. You should also see that a source with the right number is insufficient when the plan or version is wrong. An answer with insufficient evidence should acknowledge that limitation or request clarification rather than invent a policy.

For larger evaluations, keep the question, expected relevant source IDs, actual retrieved IDs, source versions, generated answer, and claim-level judgments together. These fields help reproduce failures. A retrieval change and a prompt change should be compared separately before combining them.

## If it goes wrong

If the assistant uses outside knowledge, constrain it to the supplied fictional corpus. If it counts any citation as success, ask which exact sentence proves the numerical claim. If it labels a refusal universally correct, show a case with sufficient permitted evidence: unnecessary refusal is also a quality failure.

Check ambiguous questions separately. “How long are exports kept?” lacks a plan; guessing Team because most examples use Team is not reliable behavior. Duplicate documents can also inflate apparent retrieval coverage unless you count distinct useful evidence.

## Go deeper

Read Ragas's [Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) definition and How It's Calculated section. Skip the code samples and stop before Legacy Metrics API. Public reading needs no account. Executing its examples requires separate packages and model configuration; this lesson has not executed them. The metric is one component, not a complete test of truth, source authority, permissions, or usefulness.

The retained [grounding and evaluation lab](../../labs/06-grounding-and-evaluation.md) is optional engineering practice. [Evaluation versus a convincing demo](../../articles/evaluation-vs-demo.md) provides additional interpretation guidance.

## Optional practice

Ask your tutor for one new three-document policy case containing a missing date or conflicting plan. First identify the extra evidence you need. Request feedback after your attempt; do not ask for the completed evaluation in advance.
