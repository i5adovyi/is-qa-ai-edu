# Lab 14 — Compare retrieval and claim support

Allow 90–150 minutes after lessons 04–05 and 16–17. Python 3.9+; no packages, model account, or network required.

## Inspect the experiment before running it

The [versioned corpus](../practice-corpus/retrieval.json) includes ten notes and twelve classroom queries: paraphrases, version applicability, an exception, an unapproved conflicting draft, copied evidence, and unanswerable questions. Expected source IDs and candidate claim labels are evaluation data. The retriever receives only the query, records, selected version, and retrieval configuration.

Predict three things: which query may fail a literal word match, which old source should disappear under version filtering, and why a search hit might still fail to answer a question. Keep these predictions outside the corpus.

## Run three controlled variants

```sh
python3 -m lab.practicum.retrieval --out work/retrieval-v1
```

Inspect `report.json`. It records the corpus version and hash, per-case source rankings, recall at three for answerable cases, separate no-answer cases, and claim judgments. The variants are:

1. Lexical term overlap with version filtering.
2. Hybrid lexical scoring plus explicit synonym groups, with the same filter.
3. The same hybrid method without version filtering.

This hybrid uses inspectable synonym expansion; it is not an embedding model. Compare variants 1 and 2 to study expansion, then 2 and 3 to study filtering. Do not attribute both changes to one cause.

Recall is the number of required evidence IDs retrieved divided by the number required. An unanswerable query has no such denominator; it is reported separately. The label-based claim checker distinguishes supported, contradicted, not established, and not retrieved. It matches authored claim identifiers; it does not understand arbitrary prose.

**First gate:** reproduce all twelve rows, reconcile the ten answerable cases, identify changed rankings, and explain why the two unanswerable cases cannot be counted as ordinary recall successes.

## Test a real retrieval tradeoff

Make a copy of the corpus under `work/`. Freeze the original labels before changing retrieval. Choose one experiment:

- Replace a title term with a synonym and predict how each method changes.
- Split the exception from its policy, then test whether the needed pair still appears.
- Introduce a newer source with explicit applicability and inspect the refresh decision.
- Compress a passage while retaining its exception, then deliberately omit the exception and inspect the resulting loss.

Run your copy with `--corpus work/your-corpus.json --out work/retrieval-v2`. Preserve a case-level before/after table. A copied passage should not be described as independent corroboration.

If an embedding retriever is part of your chosen project, add it as a separate adapter using current official model documentation and record its exact model revision and dependency versions. Use the same query/corpus/ID interface and evaluation labels. That extension is optional; the supplied hybrid already gives a complete offline comparison. Add reranking only after identifying a concrete ranking failure, with its cost included.

## Audit answer quality separately

Choose three retrieved sets. Write a short answer from each and label every factual sentence against its source excerpt. Include one real-but-irrelevant citation, one contradicted claim, and one missing-evidence case. Compare your human judgments with the authored claim-ID checks in the report.

**Final gate:** report retrieval and answer quality independently; identify at least one retrieval failure or limitation; show one before/after change; preserve a source conflict; explain why a valid citation alone does not establish a correct answer. Do not silently revise evaluation labels to improve your score.

[Retrieval implementation](../../lab/practicum/retrieval.py) · [Evaluation plan](../../templates/evaluation-plan.md)
