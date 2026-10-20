# Lab 06 — Test useful answers and justified abstention

**Outcome:** validate citation membership and design evaluation checks that reward both useful work and safe escalation. Suggested time: 60–90 minutes.

## The problem

An agent can cite a real article while making a claim the article never supports. Another agent can avoid every risk by escalating everything while accomplishing almost nothing. A useful evaluation must catch both unsupported confidence and unnecessary abstention.

The reference gate checks eight properties per ticket, including expected action, category, citations, required content, and effect bounds. This is stronger than checking whether a run exited successfully, but it is still a small collection of explicit assertions.

## Observe

```sh
python3 -m lab.cli evaluate --split train --out .lab-runs/lab06-training
```

Open `report.json`, then inspect the training case about an immediate refund guarantee. The approved handbook says a refund is not guaranteed before review. Explain why a correct response refuses to adopt the customer's requested promise.

Inspect the “always escalate” regression test in `tests/test_lab_engine.py`. It should fail the acceptance gate because the system is expected to complete supported tasks.

## Build

Implement `citations_valid(citations, retrieved)`.

Return `True` only when:

- Citations are a nonempty list.
- Every citation is a nonempty string.
- No citation is repeated.
- Every citation ID appears in the provided retrieved-ID collection.

Return `False` for empty lists, strings passed as the whole list, nested values, duplicates, and unknown IDs.

This is a provenance check, not a semantic entailment check. Name that limitation in your code comment and review note.

## Completion gate

```sh
python3 -m lab.cli practice --lab 06
```

All eight public checks must pass, including multiple valid citations and rejection of an empty ID. Add an example for a valid ID from the wrong topic. Your function will accept it if that ID was retrieved; explain which additional layer must enforce relevance.

## Improve an evaluation, not just a score

Author four new cases without changing the current holdout:

1. A supported task with an ordinary expected draft.
2. A request for a guarantee the source does not provide.
3. Two equally plausible articles with conflicting versions.
4. A safe customer quotation containing instruction-like words.

For each, write the expected action and the reason before running a policy. Include at least one required fact and one prohibited claim where appropriate.

Separate metrics:

- **Usefulness:** supported tasks completed correctly.
- **Safety:** unauthorized or unsupported effects avoided.
- **Grounding:** individual claims supported by evidence.
- **Abstention:** escalations on answerable versus unanswerable inputs.

Do not average away a severe permission failure simply because many easy cases pass.

## Stretch

Create a manual review rubric for three claim-level labels: supported, contradicted, and not established. Blind the reviewer to which policy generated each answer. Compare the manual labels with the fixture substring checks. Document at least one false positive and one false negative of the automated checker.

Deliver a short evaluation card containing scope, split discipline, metrics, baseline, observed failures, limitations, and the next data slice you need.

[Hints](hints/06.md) · [Solution discussion](solutions/README.md#lab-06) · [Next lab](07-traces-and-diagnosis.md)

## Connect it to the complete harness

This lab teaches one component contract. After completing Labs 01–08, follow [Lab 11](11-complete-student-harness.md) to use this function in real runs with component evidence, crash recovery, and an integrated acceptance gate. The ordinary reference evaluation does not call this student helper.
