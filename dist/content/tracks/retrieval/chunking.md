# Split documents without breaking their meaning

## Start here

You know that retrieval finds evidence before a model answers. Now learn what happens before search: turning source material into useful pieces. This is called ingestion and chunking. You can understand it with a three-sentence policy; no database or cloud account is needed.

## The idea in plain language

**Ingestion** brings documents into a searchable collection. **Chunking** divides them into units that can be retrieved and supplied to a model. A **chunk** may be a paragraph, section, or other meaningful piece. It should retain enough context to make its content understandable and applicable.

Tiny chunks may lose qualifications. Huge chunks may mix unrelated topics and consume unnecessary context. **Overlap** repeats a small amount of neighbouring content to preserve continuity, but too much overlap can make the top results near duplicates. There is no universal correct chunk size for every policy, code file, table, and log.

Keep metadata with each chunk: source ID, heading, version, effective date, and access scope when relevant. A sentence such as “This does not apply to trial accounts” is dangerous if separated from the rule it qualifies. Tables also need their headers; a number without its column meaning can produce a confident but incorrect answer.

## A small example

Signal Desk’s fictional policy says:

> Attachment policy, v2. Support users can upload files up to 20 MB. Trial accounts are limited to 5 MB. Archived tickets do not accept new attachments.

Splitting after the first rule and retrieving only “Support users can upload files up to 20 MB” can mislead an answer about trial accounts. A better chunk preserves the exception or includes metadata that lets the search retrieve the correct associated rule.

The goal is not to force every document into one piece. In a long manual, unrelated billing sections can remain separate. But the heading and local conditions should travel with the relevant rule. Later, retrieval tests can reveal whether the chosen boundaries keep answers intact for realistic questions.

## Try it with Codex or Claude Code

Open chat with the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Teach chunking using this synthetic policy only:
“Attachment policy, v2. Support users can upload files up to 20 MB.
Trial accounts are limited to 5 MB. Archived tickets accept no new attachments.”
Show one harmful split and one useful way to preserve context. Explain
which metadata belongs with a retrieved piece. Do not invent a universal
token size or install a database. Distinguish a conceptual demonstration
from an evaluated retrieval strategy. Stop before independent practice.
```

Ask what would happen if a question used the phrase “free plan” while the policy says “trial.” That connects chunk preparation to the later search strategy. A well-prepared collection still needs a way to find relevant pieces using the words or meaning of a user’s question.

## What you should see

The answer should preserve version and exceptions, and explain the harm of losing them. It should not say that overlap guarantees correctness. It should keep the original source addressable so a reader can inspect the full passage. A chunk is an evidence candidate, not a replacement for the source’s authority or access rules.

## If it goes wrong

If every result repeats the same paragraph, inspect overlap and duplicate handling. If a table answer loses its units, preserve headings and labels. If source text was extracted incorrectly from a PDF, fix ingestion before tuning the search algorithm. If a document changes, decide how old chunks are replaced or retired; appending the new version without handling the old one can create conflicts.

## Go deeper

Read “Common chunking techniques” and “Content overlap considerations” in Microsoft’s [Chunk documents](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents). Stop before implementation examples. The conceptual reading requires no Azure resource. The academy’s [retrieval comparison lab](../../labs/14-retrieval-comparison.md) is optional later practice with explicit evidence.

## Optional practice

Ask your tutor for a short new policy with a heading, main rule, and exception. Propose chunk boundaries verbally and identify what must stay together. Submit your attempt before asking for feedback; you do not need to write a chunking script.
