# Combine exact and semantic search

## Start here

You know why semantic search can find paraphrases. Now consider error codes, product IDs, dates, and technical terms that must match exactly. A useful retrieval system often combines methods. This lesson teaches the tradeoff with a tiny synthetic corpus before introducing any infrastructure.

## The idea in plain language

**Keyword search** uses words or tokens occurring in the indexed material. **BM25** is one common ranking method for text search; it considers term frequency and document characteristics. You do not need its formula to understand why a rare exact identifier can be important.

**Hybrid search** combines different retrieval methods, commonly keyword and vector search. A **rank fusion** method combines their ordered lists. **Reciprocal Rank Fusion**, or RRF, is one way to reward documents ranked highly across lists without assuming that the original scores use the same scale.

**Reranking** reorders an initial set of candidates using an additional relevance check. It cannot rescue a relevant document that never entered the candidate set. **Filtering** restricts eligible records by metadata such as product version or access scope. A filter is different from a soft relevance preference; restricted records must not become available merely because they score highly.

## A small example

Question: “What does error SD-429 mean in version 2?” The collection contains:

| Source | Content | Scope |
| --- | --- | --- |
| A | SD-429 means request quota exceeded | version 2 |
| B | Too many requests can delay processing | version 2 |
| C | SD-429 means legacy queue overflow | version 1 |

Exact matching helps find A and C. Semantic matching may find B because it describes a related idea without the identifier. The version filter and actual source text distinguish the useful answer. Neither keyword nor vector score should erase the version boundary.

A tempting but misleading shortcut is adding unrelated raw scores together. A lexical score of 8 and cosine similarity of 0.7 do not represent the same units. Fusion or another explicitly evaluated combination method addresses ranking; the final evidence still needs inspection.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), paste the table, and add:

```text
Teach hybrid retrieval for “SD-429 in version 2” using only the table above.
Explain what keyword and semantic search might each contribute. Define
filtering, rank fusion, and reranking. Do not invent measured search scores.
Show why a version 1 exact match should not answer the version 2 question.
Explain one case where a second retrieval method adds complexity without
helping. Keep this conceptual; do not provision services or run an API.
```

Ask the assistant how it would evaluate the choice on both exact-code questions and paraphrased questions. A realistic evaluation includes both, because a method that improves one category may weaken another. More components are justified by evidence, not by the word “hybrid.”

## What you should see

The answer should preserve the exact code and version, separate ranking from access filtering, and explain why raw score scales are not interchangeable. It should propose evaluating candidate recall and final relevance separately. **Recall** here asks whether the useful evidence appears among the candidates; a fluent final answer cannot compensate for its absence.

## If it goes wrong

If the top results are duplicates, inspect chunk overlap and fusion inputs. If a reranker consistently prefers verbose but irrelevant text, examine its criteria and examples. If a hard identifier is lost during query rewriting, retain it explicitly. If a filter removes the correct document, check metadata quality rather than assuming the embedding model is at fault.

## Go deeper

Read “Why use hybrid search?” and “How does hybrid search work?” in Microsoft’s [hybrid search overview](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview). Stop at the query implementation section. No Azure account is required for this scope. The academy’s [retrieval comparison lab](../../labs/14-retrieval-comparison.md) offers optional evidence-based comparison practice.

## Optional practice

Ask your tutor for one identifier query and one paraphrase query over a small new collection. Choose the retrieval method you would try first and explain the tradeoff. Attempt before receiving feedback; no database deployment is required.
