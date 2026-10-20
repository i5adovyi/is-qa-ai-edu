# Lab 02 — Select evidence under a context budget

**Outcome:** implement deterministic evidence packing and distinguish cumulative observation budgets from a model context window. Suggested time: 60–90 minutes.

## The problem

An agent often has more available information than it can use well. Dumping everything into context can increase cost, hide relevant facts, and introduce conflicting instructions. The first useful question is not “How much context can my model accept?” It is “What evidence changes this decision?”

The reference harness charges serialized tool results against `max_context_chars`. This is cumulative exposure accounting. Your exercise packs a set of candidate passages into one bounded selection; these are related but different mechanisms.

## Observe

```sh
python3 -m lab.cli demo --scenario context-overflow --out .lab-runs/lab02-overflow
python3 -m lab.cli trace .lab-runs/lab02-overflow/trace.jsonl
```

The first command intentionally exits nonzero. Predict whether the policy gets to decide, whether a draft exists, and which tool triggers the error. Confirm those three points in the result and trace.

Read `Usage.consume` in `lab/contracts.py` and the output-budget check in `lab/tools.py`. Explain why rejecting an oversized observation after retrieval does not undo retrieval cost.

## Build

Implement `pack_context(articles, max_chars)`.

Each article has `id`, `text`, and numeric `relevance`. Return selected **IDs**, following this algorithm:

1. Rank by descending relevance; break ties by ascending ID.
2. Visit each unique ID once, using its first ranked occurrence.
3. Charge exactly `len(article["text"])`.
4. Include an article only if it fits the remaining budget.
5. Skip oversized candidates and continue trying later ones.
6. Reject a negative budget with `ValueError`.

For article lengths `A=8`, `B=5`, `C=2`, with A ranked first and B before C, a budget of 10 selects `["A", "C"]`. A budget of 5 selects `["B"]`. Stopping after the first oversized item is a bug.

## Completion gate

```sh
python3 -m lab.cli practice --lab 02
```

All five public checks must pass. Add tests for exact-fit boundaries and two equal-relevance candidates arriving in opposite input orders. State whether input order should affect the result.

## Review the tradeoff

This greedy selector is deterministic and easy to explain. It does not maximize every possible utility function. A long high-ranked passage might displace two shorter passages whose combined value is greater.

Create a three-passage counterexample. Calculate the selected relevance sum for greedy packing and for a better combination. Decide whether the extra optimization complexity is justified for your use case.

Also account for what this toy budget omits: role framing, instructions, article metadata, separators, conversation history, output allowance, tokenizer variation, and UTF-8 byte size. Do not label characters as tokens.

## Stretch

Add a provenance envelope containing article ID, revision, source label, retrieval query, and selection reason. Compare selecting only relevant excerpts with selecting whole documents. Introduce one conflicting article and describe how a robust decision policy should respond.

Deliver a context-allocation table with fixed policy allowance, evidence allowance, task data, and reserved response budget. Clearly state which numbers you measured and which you assumed.

[Hints](hints/02.md) · [Solution discussion](solutions/README.md#lab-02) · [Next lab](03-tool-authority.md)
