# Understand semantic search before installing a database

## Start here

You understand embeddings and chunking. Now connect them: how can a question find relevant material when it uses different words? This lesson explains semantic search and its failure cases before you choose libraries or services. A simple conceptual ranking is enough to begin.

## The idea in plain language

**Semantic search** compares representations of meaning to find potentially relevant material. A typical embedding-based pipeline represents the question and document chunks as vectors, compares them, and returns a ranked list. The **corpus** is the collection being searched; **top k** means the first k candidates returned.

The query and stored documents must use compatible representations. A **vector index** is a structure that helps find nearby vectors efficiently. A vector database adds storage and management features around such data. Small collections can sometimes be searched directly; a database is not the definition of semantic search.

**Cosine similarity** compares vector directions. You do not need to calculate it by hand to understand its role: it helps rank candidates according to one representation. A high score does not establish truth, applicability, access permission, or a calibrated probability of a correct answer.

Some search tasks compare similar-length texts, such as two questions. Others compare a short query with a longer answer passage. The model and its query/document handling should suit that task. Choosing an embedding model merely because it is popular can miss important differences in language or domain.

## A small example

Question: “Why can’t help-desk staff sign in?” Candidates include “Support users receive an access-denied response,” “How to create invoices,” and “Suspended accounts cannot log in.” The first may be relevant despite different words. The third shares the general topic but may apply only to suspended users.

A human can predict which candidate seems useful, but that prediction is not a measured embedding result. An actual run would require a chosen model, inputs, and recorded outputs. After retrieval, inspect the source conditions before presenting an answer. Retrieval finds possibilities; it does not finish the investigation.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and paste:

```text
Explain semantic search using this synthetic question and three candidates.
Question: Why can't help-desk staff sign in?
A: Support users receive an access-denied response.
B: How to create invoices.
C: Suspended accounts cannot log in.
Predict useful candidates in ordinary language, clearly labelled as a
prediction rather than an embedding run. Define corpus, vector index,
top k, and cosine similarity. Explain what still needs checking after
retrieval. Do not invent scores, download models, or call APIs.
```

If you later choose to run the bundled retrieval comparison, follow its prerequisites and distinguish its specific implementation from this conceptual explanation. A lexical or simulated comparison is useful evidence for its own behaviour, but should not be described as a real embedding model run.

## What you should see

The answer should explain why A can match despite different vocabulary and why C needs applicability checks. It should avoid numeric scores unless they come from an actual calculation. It should say that changing the embedding model can require rebuilding stored representations and reevaluating search, rather than mixing incompatible vectors.

## If it goes wrong

If exact identifiers are missed, consider keyword search or a hybrid strategy. If irrelevant documents dominate, inspect chunk contents, query wording, language coverage, and metadata filters before changing the answer prompt. If the right passage never enters the candidates, the generator cannot cite it reliably. If results contain private records, access filtering must be corrected before generating an answer.

## Go deeper

Read “Background” and “Symmetric vs. Asymmetric Semantic Search” in the [Sentence Transformers semantic search guide](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html). Stop before “Manual Implementation.” Public reading needs no installation; optional model execution has separate dependencies and download requirements. Revisit [embeddings](../foundations/embeddings.md) if the representation terminology is unfamiliar.

## Optional practice

Ask your tutor for a new question and four passages, including an exact-word trap. Predict useful candidates and explain what metadata could rule one out. Attempt this before feedback. You do not need to produce real vector scores to show conceptual understanding.
