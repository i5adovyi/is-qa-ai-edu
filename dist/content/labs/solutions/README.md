# Solution review

**Spoilers.** [reference.py](reference.py) contains one complete implementation of each student function. Read the relevant function after attempting the lab and its progressive hints. Copy only the function you are reviewing if you need a working comparison; the learner module is intentionally separate from the baseline. Include its imports at the top of `lab/student.py`: Lab 01 needs `import re`; Lab 05 needs `import hashlib` and `import json`; Lab 08 needs `from lab.policy import classify`. The other examples need no imports. A `NameError` naming one of these dependencies means the function was copied without its import.

The baseline unit suite executes these solution functions against every public practice check. That proves the examples meet the teaching contract. It does not make them production implementations.

## Lab 01

Two bounded regex substitutions preserve unrelated text. The replacement tokens do not match the original patterns, so the operation is idempotent.

Common wrong answer: replacing everything after `sk-demo-`, which removes useful context. Another is splitting on whitespace and accidentally altering formatting.

Review limit: this is a synthetic redactor, not a comprehensive secret scanner. An encoded credential or unexpected key format can pass through.

## Lab 02

Sort by `(-relevance, id)`, track visited IDs and used characters, and skip any article that does not fit. This gives stable results independent of input ordering for distinct IDs.

Common wrong answer: breaking at the first oversized article. Another is counting selected IDs rather than passage text.

Review limit: greedy selection is not a general optimal-packing algorithm. Duplicate ID records with different content need a source-version policy beyond this exercise.

## Lab 03

A short-circuit Boolean expression checks the known tool, external allowlist, argument type, exact key set, string value, and ticket scope in that order.

Common wrong answer: trusting a tool just because its name appears in the allowlist, or accessing `arguments["ticket_id"]` before validating structure.

Review limit: this pure function does not authenticate the caller or sandbox Python code. It is one layer of a larger authority boundary.

## Lab 04

Reject negative and noninteger values. Handle zero base, short-circuit attempts that necessarily hit the cap, and otherwise compute the bounded exponential.

Common wrong answer: accepting booleans, sleeping inside the pure function, or computing an enormous power before taking `min`.

Review limit: a real retry mechanism also needs retryable-error classification, cancellation, deadlines, and a strategy for uncertain side effects.

## Lab 05

Serialize the three inputs as a JSON list with stable formatting and UTF-8 encoding, then hash that representation with SHA-256. Boundaries remain unambiguous and output length is fixed.

Common wrong answer: colon-joining arbitrary values, creating a new UUID on every retry, or using Python's process-randomized built-in `hash()`.

Review limit: a stable key alone does not ensure idempotency. The effect and its replay record must be stored consistently.

## Lab 06

Validate list shape and string elements before using sets. Require a nonempty list, unique values, and subset membership in retrieved IDs.

Common wrong answer: treating a citation string as a collection of characters, or assuming any known handbook ID was retrieved for this decision.

Review limit: membership does not establish relevance or support for each claim. A separate semantic or human review is needed for those claims.

## Lab 07

Each summary count is a direct event predicate. Replay counting requires both the `tool_result` event kind and the exact Boolean `True`.

Common wrong answer: counting truthy strings or treating every tool rejection as a failed run.

Review limit: aggregate counts cannot establish which effect committed. Preserve sequence and operation identity for diagnosis.

## Lab 08

Classify the ticket, filter evidence to the category, escalate unsafe/unknown/ambiguous inputs, and construct the exact decision contract. Grounded drafting copies the synthetic approved answer and its citation.

Common wrong answer: drafting from the first available article regardless of topic, inventing facts, or omitting required output fields.

Review limit: copying approved answers works for these closed-world cases. It does not demonstrate flexible synthesis, real-model behavior, or production readiness.

## After reading a solution

Close the file, reimplement the function from the contract, and add a case the public checks do not cover. Explain why that case matters. This is more valuable than keeping an implementation you cannot defend.
