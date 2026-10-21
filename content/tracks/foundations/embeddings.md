# Embeddings: finding similar meaning with numbers

## Start here

You know that models process tokens and that plausible text needs verification. Now learn a different use of a model: representing text so software can compare it. You do not need algebra, a vector database, or Python to begin. This concept prepares you for the separate retrieval track.

## The idea in plain language

An **embedding** is a list of numbers representing some properties of an input. A **vector** is the mathematical name for that list. An embedding model places inputs into a representation where a chosen similarity calculation can help find related items.

Imagine sorting test failures on a desk. “Cannot sign in” and “Login rejected” might belong near each other even though they share few words. A text embedding can help software make that kind of comparison. It does not produce a human-readable reason automatically, and individual coordinates usually do not correspond to neat labels such as “login” or “severity.”

Similarity is not truth, permission, or equivalence. “Refunds are allowed” and “Refunds are not allowed” concern the same subject and may appear close. Two duplicate-looking defects might affect different product versions. A similarity score is meaningful only in relation to the model, comparison method, and task; it is not a universal probability that a document answers the question.

## A small example

Signal Desk has three invented tickets:

| ID | Description | Version |
| --- | --- | --- |
| T1 | Login returns 403 for support users | 2.1 |
| T2 | Sign-in denied for help-desk staff | 2.1 |
| T3 | Login returns 403 after account suspension | 1.8 |

T1 and T2 may describe a similar issue. T3 shares exact words but could be expected behaviour under a different policy. An embedding search might retrieve all three. You still need version, account state, and an actual reproduction before merging reports as duplicates.

This separates **candidate retrieval**, finding items worth inspecting, from **decision making**, deciding whether the evidence supports a conclusion. An embedding is useful for the first without being sufficient for the second.

## Try it with Codex or Claude Code

Open chat using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md). Paste the table and this prompt:

```text
Explain embeddings using the three synthetic tickets above.
First compare their wording and meaning in ordinary language.
Then explain what an embedding search could help find and what it cannot
decide about duplicate defects. Do not invent vectors or similarity scores.
Show which metadata I must inspect before treating two tickets as the same.
Keep this conceptual: no model downloads, database, API calls, or file edits.
```

Ask it to explain “metadata” if unfamiliar: metadata is information about a record, such as its version, owner, date, or source. The actual ticket description is its content. Both can matter to a useful search result.

## What you should see

The response should distinguish conceptual similarity from a measured embedding result. It should avoid pretending that a hand-written list of numbers came from a real model. It should retain the version and account-state differences, and should not claim that a high score authorises exposing a private ticket.

## If it goes wrong

If it recommends a vector database immediately, ask for the smallest example that teaches comparison without infrastructure. If two embedding sets were created with different models, do not assume they are comparable even if the lists have the same length. If a model changes, the stored representations and search evaluation may need rebuilding. Test with examples from your domain rather than choosing a threshold from a blog.

## Go deeper

Read the food-similarity example and explanation of representations in Google’s [Embeddings](https://developers.google.com/machine-learning/crash-course/embeddings). Stop before pursuing the mathematical prerequisite modules. The diagrams are supplied by the reading; you are not asked to draw one. Continue later with the academy’s [retrieval guide](../../how-to/05.md) to see embeddings in a larger evidence pipeline.

## Optional practice

Ask your tutor for four new bug summaries, including one misleading near match. Predict which are useful candidates and state what extra fact would confirm a duplicate. Submit your choices before asking for feedback; no numeric vector calculation is required.
