# Build a research workflow with verifiable handoffs

Build a small research assistant that answers a technical question from a bounded set of primary sources. Its output must connect claims to evidence, expose conflicts, and distinguish source statements from your own inference. Use multiple agents only if a measured comparison justifies them.

## Product scenario

A team needs to decide whether to use a fixed workflow or an agent for a support knowledge task. The assistant receives five to ten primary documents, a decision question, and constraints on cost, latency, permissions, and evidence. It produces a recommendation memo and an auditable evidence table.

Use supplied synthetic documents for offline practice, then optionally repeat with public official sources. Do not scrape or bundle third-party course content. Preserve titles, URLs, dates where available, and access limitations.

## Build milestones

1. Define the decision and required evidence. State what the memo must not claim.
2. Build a single-worker baseline. Record its source choices, unsupported claims, elapsed time, and output quality.
3. Create an evidence ledger with claim ID, source ID, supporting passage location, confidence in relevance, and conflict status.
4. Design optional researcher and reviewer roles with separate ownership and a strict artifact contract. The reviewer must inspect evidence rather than merely approve prose.
5. Add a bounded revision loop. Stop when criteria pass or the budget is exhausted; report unresolved claims honestly.
6. Compare the workflow variants and write the final decision memo.

## Adversarial cases

Include a source containing an instruction to ignore other documents, a plausible but outdated statement, two contradictory sources, a citation that mentions a topic without supporting the claim, and a question that cannot be answered from the available corpus. A useful assistant should sometimes say that the evidence is insufficient.

## Required checks

- Every material factual claim has supporting evidence or is labeled as an inference.
- Citation existence and citation support are evaluated separately.
- Conflicting sources are preserved until resolved by an explicit rule.
- Retrieved instructions cannot change the task or authorize additional actions.
- The workflow produces an honest incomplete result when the evidence is inadequate.
- Delegation handoffs preserve provenance and do not convert guesses into facts.
- The multi-worker variant is compared against the single-worker baseline on the same criteria.

## Evaluation design

Have a reviewer inspect at least 20 claim-source pairs across several questions. Label supported, partially supported, unsupported, and contradicted. Include cases where a citation is real but irrelevant. Record inter-reviewer disagreement on a subset if a second reviewer is available. Report the denominator and avoid generalizing from a tiny sample to all research tasks.

## Evidence package

Submit the corpus manifest, task contract, evidence ledger, worker briefs, final memos, cost and latency accounting, comparison report, and a handoff failure analysis. Record which calls used a real model and which were simulated. Do not imply that a deterministic simulation demonstrates research accuracy.

## Stretch work

Add source refresh and stale-claim detection. Introduce a budget-aware retrieval strategy. Compare full-context reading with selective retrieval. Measure whether a separate critic catches unsupported claims or simply adds confident wording.

## Defense questions

Can a citation be valid but still fail to support the claim? What did delegation improve? Where did a summary lose an important qualification? Which question should the system decline to answer? How would your recommendation change if the cost budget were cut in half?

Suggested scope: 10-18 focused hours. Use the shared capstone assessment rubric and retain failed attempts.
