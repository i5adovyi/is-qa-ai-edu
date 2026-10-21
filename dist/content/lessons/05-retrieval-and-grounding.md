# 05 · Retrieve evidence before generating answers

> Optional practice edition. You can read this explanation without completing its exercises. For the guided SDET route, use [Start here](../../docs/START-HERE.md).

Stage 2 · 110 minutes · Foundation

Build a small retrieval experiment that exposes why finding a document and supporting a claim are different tasks.

## What you will be able to do

- Create a lexical retrieval baseline and measure recall.
- Choose chunks that preserve exceptions and identifiers.
- Audit whether citations actually support generated claims.

## The idea

Retrieval is the process of selecting potentially useful material. Grounding is the relationship between the final claim and the selected evidence. A search engine can retrieve the right document while the answer misreads it. An answer can include a real citation that does not support the sentence beside it. Evaluate both stages separately.

Begin with a small corpus and a lexical baseline. Split documents into useful units, normalize words and rank by term overlap. This approach is deliberately simple. It makes errors inspectable and establishes a reference before embeddings, rerankers or agentic search. Preserve document IDs and section boundaries so results can be traced back to source material.

Chunking is a decision about what context remains together. If “refunds are allowed within fourteen days” and “except annual enterprise contracts” land in separate chunks, retrieval can return a misleading half-rule. Chunk boundaries should reflect the questions users ask and the exceptions that change answers. Larger chunks preserve context but can introduce irrelevant material. Measure the tradeoff on your own cases.

For each evaluation ticket, identify required evidence IDs before retrieving. Recall at k asks how much of that required evidence appears in the first k results. It does not measure correctness of the answer or sufficiency of the corpus. Include an explicit no-answer case where no document supports a resolution. Otherwise, your system learns that every search must yield an answer.

## Worked example

Use three synthetic notes:

```text
KB-1: Reset links expire after 30 minutes. Request a fresh link.
KB-2: Enterprise SSO users must contact their identity administrator.
KB-3: Export jobs above 100 MB require the batch export workflow.
```

Ticket SD-105 says, “My company login reset link expired; we use SSO.” A keyword query for “reset link expired” strongly matches KB-1. However, SSO makes KB-2 decision-critical. The answer should not blindly promise that a fresh password-reset link solves enterprise access. The retrieval query or selection rule needs to account for authentication mode, and the draft should preserve that distinction.

## Optional starter practice

Before inventing your own cases, use the [lesson 05 starter pack](../practice/lesson-05-starter.json) and [fixture workflow](../practice/README.md). Label one or two cases yourself before deliberately opening a separate key. These are warm-up examples; complete the original exercises below with new learner-authored cases. Supplied practice examples are not untouched evaluation evidence.

## Exercise 1 · Guided corpus

Write eight short knowledge notes with IDs, applicability and one exception each. Create six queries including synonyms, a misleading keyword and an unanswerable request. Label the required evidence for each query before running any retrieval. Include the SSO example.

**Deliverable:** corpus and relevance labels. **Pass:** at least one query requires two notes; one requires no answer; labels explain why each source matters.

## Exercise 2 · Build and measure

Implement term-overlap retrieval in a spreadsheet, by hand, or in a small script. Return the top three notes for every query. Compute recall at three for cases with required evidence; report the no-answer case separately. Improve one variable, such as synonym expansion or chunk boundaries, and compare on the same queries. Optional model use: generate drafts from the retrieved notes only.

**Deliverable:** rankings, metric calculation and a one-change comparison. **Pass:** no hidden manual reranking; missing required evidence remains visible in the result table.

## Exercise 3 · Adversarial citation audit

Write a draft that cites KB-1 while claiming SSO users can reset credentials through Signal Desk. Write another that cites KB-3 while promising an immediate export. Audit each sentence against its cited excerpt. Add a plausible but nonexistent source ID and confirm that a source-existence check catches it.

**Deliverable:** claim-to-evidence table. **Pass:** you identify both unsupported implications and the nonexistent source; a valid ID alone never earns a grounding pass.

## Hints and solution outline

Token overlap can be calculated as the number of shared normalized terms. Break ties deterministically, for example by source ID. For the SSO ticket, the desired retrieval set includes KB-2; KB-1 can explain why the ordinary reset route is tempting but insufficient. Use “No applicable source found” as a valid outcome. A source existence check is automatic; an entailment check asks whether the cited text actually warrants the claim. Keep those checks separate in your report.

## Reflection

After lessons 16–17, extend this first experiment with [lab 14's versioned retrieval comparison](../labs/14-retrieval-comparison.md). It supplies a richer corpus and separates recall, source applicability, and claim support. Complete this lesson's basic reasoning before adding retrieval complexity.

Would your proposed improvement help unseen wording or only your six queries? What happens when a new document contradicts an old one? Which failure belongs to search, which to chunking, and which to answer generation?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
