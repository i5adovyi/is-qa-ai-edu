# A demo is a hypothesis. An evaluation is a decision tool.

**Stage 6 · Original field guide · 30-minute lesson plus a 60-minute evaluation lab**

Your assistant triages a support ticket correctly. The demo is smooth: it finds a related incident, assigns a sensible category and drafts a clear response. What have you learned? You have evidence that this configuration can succeed on that input under those conditions. You do not yet know whether it can handle missing facts, conflicting policies, repeated tool failures or the normal variety of incoming tickets.

An evaluation should support a specific decision. “Is this good?” is too vague. “Can we allow the assistant to draft recommendations for human review without increasing missed-critical-ticket errors?” suggests a population, a baseline, a failure cost and a deployment boundary.

OpenAI's evaluation guide and Anthropic's agent evaluation article both provide useful foundations for testing model-based systems. Use them as references; the dataset and thresholds below are original teaching examples, not vendor requirements or claims of production readiness. [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [Anthropic agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

## Define success before producing answers

For a triage assistant, separate the dimensions:

| Dimension | Example measure | Why it matters |
| --- | --- | --- |
| Category | Correct category or valid abstention | Basic usefulness |
| Evidence | Every decisive claim references supplied evidence | Auditability |
| Critical handling | Critical cases are escalated | Asymmetric failure cost |
| Tool behavior | No unauthorized or malformed action executes | Runtime reliability |
| Efficiency | Calls, elapsed time, tokens and estimated usage cost | Practical operation |

Do not collapse these into a single score too early. A fast system that misses critical tickets should not compensate for that error by producing pleasant prose. Keep hard constraints separate from average quality metrics.

Write a rubric in observable language. Instead of “good explanation,” use “states the proposed category, cites at least one supporting observation, and distinguishes unresolved facts from confirmed facts.” Two reviewers should usually agree on whether the requirement was met.

## Build cases from failure modes

Start with a deliberately small development set that you can inspect completely. For example, make 20 cases: six routine tickets, four ambiguous tickets, three missing-evidence cases, three conflicting-policy cases, two tool failures and two malicious-content cases. This allocation is for learning; a production set must reflect its actual traffic and risks.

Each case needs an identifier, input, available evidence, allowed actions and an expected outcome. The expected outcome may be a set of acceptable answers. If a case is intentionally ambiguous, requiring one exact diagnosis teaches the wrong behavior. Define when the assistant should abstain or request a specific missing fact.

Keep a separate holdout that is not used for prompt tuning. An assistant that helped write the cases can also help suggest edge conditions, but have a human inspect labels and diversity. Synthetic cases often share wording, assumptions and blind spots with their generator.

Record provenance. A fabricated case, a sanitized historical case and a replay of actual traffic support different conclusions. Do not label a synthetic benchmark as customer validation.

## Choose the cheapest credible grader

Use deterministic checks where the desired property is precise: valid JSON, allowed category, existing evidence IDs, correct arithmetic or absence of an executed forbidden action. Check the result in the environment when possible. A generated paragraph saying “the file exists” is weaker evidence than a successful file inspection.

For semantic quality, use a human rubric first. A model judge can help scale review, but calibrate it against human labels and inspect disagreements. Shuffle answer order for pairwise comparisons, conceal provider identity where practical and test whether the judge is overly impressed by length or confident tone.

A grader is software and can be wrong. Include deliberately bad outputs that should fail and good outputs that should pass. If both pass, the score is meaningless. If the evaluator checks only that an `evidence_ids` array exists, the assistant may pass while citing nonexistent evidence.

## Compare configurations fairly

Freeze the cases and grader, then change one important factor: prompt, model, retrieval policy or tool contract. Save the exact configuration and raw outputs. Repeat runs when the model is stochastic and report variation. Use fresh conversations unless the evaluation explicitly concerns memory.

For a teaching example, suppose configuration A passes 16 of 20 cases and B passes 18. Inspect the changed cases before declaring B better. B might improve two routine classifications while introducing one critical failure. It might also have benefited from a temporary service recovery rather than a better prompt.

Small samples produce uncertain estimates. With zero observed failures in a limited test, the failure rate is not proven to be zero. A useful report says “no unauthorized actions observed in these 40 attempted cases” and describes the coverage. It does not say “the system is safe.”

## Turn failure into an engineering action

Classify failures by their earliest causal boundary. Did retrieval omit the decisive policy? Did the model misread supplied evidence? Did the tool time out? Did the runner mishandle the timeout? Did the grader reject an actually correct answer? These require different fixes.

Write a failure record containing the case ID, observed result, expected result, evidence, suspected cause, proposed fix and a regression test. Avoid immediately adding another instruction for every failure. A missing access control belongs in code. An outdated document belongs in the knowledge source. An unclear success criterion belongs in the specification.

## Submission and review

Submit a dataset card, frozen cases, rubric, baseline results, candidate results and three inspected failure records. Include a claim you can support and one tempting claim you cannot. Pass when a reviewer can reproduce the comparison and understand both the improvement and its limits. That is the difference between an attractive demonstration and evidence that can guide deployment.
