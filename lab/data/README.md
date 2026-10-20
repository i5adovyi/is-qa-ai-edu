# Synthetic fixture register

All ticket text, customer names, knowledge articles, product behavior, and expected outputs in this directory were created for this learning project. No real support data or proprietary manuals are included. Product policy claims such as “3 business days” and “24 hours” apply only to fictional Signal Desk fixtures.

| File | Purpose | Size |
|---|---|---|
| `knowledge.json` | Approved handbook excerpts with ID, topic, version, answer, source label | 4 articles |
| `cases.json` | Synthetic tickets, split labels, expected action/category/citations/content constraints | 28 cases |

Training cases: `train-01` through `train-18`. Holdout cases: `holdout-01` through `holdout-10`. Splits have different ticket IDs, but intentionally share product domains and article facts.

The train set covers normal requests, unsupported requests, multi-topic ambiguity, pressure to overpromise, and several explicit instruction attacks. The holdout uses different wording and combinations. Neither split is representative of a population of real customers.

## An evaluation discipline

1. Use training cases to understand and improve your implementation.
2. Before holdout, write down the version, intended change, metric, expected result, and known weaknesses.
3. Run holdout and preserve its report, including failures.
4. Once you inspect a holdout case to fix a failure, treat it as development data. Add a fresh, separately authored slice for the next final evaluation.
5. Never change a label just because your implementation disagrees. Explain the domain rule that justifies a label correction.

Add adversarial cases that distinguish plausible implementations: multi-topic wording, absent evidence, citation to the wrong article, malformed tool output, a safe request containing quoted attack text, and redaction that removes too much useful context.

The current policy intentionally escalates quoted instruction attacks. That tradeoff is visible in `train-16`; a more useful policy must evaluate safe quotations separately from actual attempts to redirect behavior.
