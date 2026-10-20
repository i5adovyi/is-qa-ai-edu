# Assess practical AI engineering skills

The unit of assessment is a reproducible artifact plus an explanation. A good-looking generated answer is not sufficient. Use this rubric to review your own work, or ask a peer to challenge the evidence.

## Common scoring rubric

Score each dimension from 0 to 4. Zero means absent; one means a demonstration with major gaps; two means a happy path works; three means repeatable behavior with relevant failures handled; four means clear tradeoffs, adversarial evidence, and documented limitations.

| Dimension | Evidence to inspect |
| --- | --- |
| Task definition | Input contract, output contract, explicit exclusions, observable acceptance checks |
| Context quality | Relevant sources, provenance, stale-source handling, untrusted-content boundaries |
| Control and tools | Typed arguments, least required capability, budgets, errors, duplicate-call behavior |
| Evaluation | Baseline, representative cases, untouched split, failure analysis, denominator |
| Reproducibility | Exact commands, fixture versions, traces, setup instructions, explanation |

A suggested pass is 15/20, with no dimension below 2. This is this course's pedagogical standard, not an industry certification. Do not average away a serious authorization failure: an unauthorized action is a gate failure even if the total score is high.

## Eight stage gates

1. **Foundations:** submit three task briefs and a baseline log. Another learner should be able to identify success without guessing your intention.
2. **Context:** submit an evidence packet with conflicting sources, a priority rule, and a compressed handoff. Show what information was deliberately excluded.
3. **Tools and skills:** submit a tool contract and a reusable skill with trigger and non-trigger examples. Demonstrate malformed arguments and an unauthorized request being rejected.
4. **Agentic development:** submit a small change request, reviewable patch, targeted tests, and a handoff. Explain a plausible regression the happy-path test would miss.
5. **Harnesses:** submit traces for success, timeout, budget exhaustion, and resumption. Show why retries cannot duplicate a completed mutation.
6. **Evaluation:** submit a baseline comparison on frozen cases. Report numerator and denominator, an error taxonomy, and any observed regressions. If none are observed, state that with the tested denominator and coverage; do not invent a regression.
7. **Delegation:** submit task boundaries, artifact contracts, integration evidence, and a comparison against one worker. Reject delegation if the benefit does not justify its overhead.
8. **Production:** submit one capstone release dossier including operation limits, stop conditions, a rollback procedure, and an incident exercise.

## Integration evidence

For the expanded engineering route, add [labs 09–11](INTEGRATION-LABS.md) to the relevant stage dossiers:

- **Stage 3, MCP:** an actual SDK client/server run with matched request IDs, rejected invalid arguments, an unknown-record result and bounded disconnect/timeout behavior.
- **Stage 3, skills:** installation evidence plus fresh-host discovery/use, a non-trigger request and a missing-reference observation. Keep a package-validator pass separate from a host-behavior pass.
- **Stages 5–6, harness:** the student composition profile, component identity and invocation records, task evaluation, failure/recovery checks, and proof that an incorrect helper changes the outcome. A completed-example pass alone is insufficient for the student's gate.

Use the same scoring dimensions and minimums. If host access is unavailable, record skill behavior as pending; the offline component and protocol work can still be assessed. These additions do not turn self-reported progress into a credential.

## How to review a submission

Start by running the student's command, using their documented input. Then change one condition: omit a field, duplicate a message, introduce conflicting evidence, or cut the allowed budget. Ask the student to predict behavior before executing. Finally inspect one trace and require a short explanation of which layer enforced the constraint.

A trace is evidence of an execution, not a guarantee that all executions behave the same. If a student claims a 95% success rate, ask “95% of which cases, with what definition of success?” If they tuned on the same cases, ask for an untouched evaluation set. If they used an LLM judge, ask for examples of disagreement with human labels and the adjudication rule.

## Capstone scoring

Use the five common dimensions above, plus five project dimensions worth 0-4 each: user usefulness, incident readiness, cost and latency measurement, data handling, and clarity of the final defense. Suggested pass: 30/40 with no dimension below 2 and no unauthorized side effects. Record the actual work reviewed, not just the score.

This is the single capstone standard for lesson 24 and all three project briefs. The 20-point rubric above is for stage submissions. Apply each dimension to the chosen product: research can demonstrate recovery from an interrupted evidence ledger; QA can demonstrate recovery from an interrupted check without claiming it passed; support can demonstrate replay without duplicate writes.

No paid model is required for an offline capstone pass. For cost and latency, report measured local work and elapsed time, label synthetic accounting assumptions, and mark model billing “not applicable.” If model integration was not exercised, it remains unverified; an offline pass must not be reported as a live-model qualification.

## Calibrate your self-assessment

Use these anchors before scoring your own submission:

| Evidence pattern | Appropriate score for the relevant dimension |
| --- | --- |
| A tool contract is described, but there is no run or mechanically reproducible simulation | 1 for control and tools |
| A draft succeeds once with valid input, with no negative case | 2 for control and tools |
| Valid input succeeds; wrong scope, malformed arguments and duplicate operations have reproducible outcomes | 3 for control and tools |
| The previous evidence includes a tested limitation, explicit assumptions and an explained tradeoff | 4 for control and tools |
| A percentage is reported without cases, a denominator or a rubric | At most 1 for evaluation |
| A baseline and candidate are compared on frozen cases, with labels, discordant cases and sample limits | 3 or 4 for evaluation, depending on reproducibility and limitations |

One strong dimension cannot rescue another from its minimum. For example, stage scores `4, 4, 4, 2, 1` total 15/20 but fail because reproducibility is below 2. Capstone scores `4, 4, 4, 4, 4, 4, 3, 3, 3, 1` total 34/40 but fail for the same minimum-dimension rule. Cite the actual artifact for every score; these examples do not substitute for reviewing the work.

## Oral defense prompts

- What is the strongest evidence that your change helped?
- Which observed failures belong to the harness and which to the model?
- What happens if a tool reports a timeout after committing an update?
- What would make you stop a run before it exhausts its budget?
- Which part of your evaluation could be rewarding a shortcut?
- What did you learn from the worst failure, and what test now captures it?

## Reassessment

Keep the original submission. Make a focused revision, rerun the failed cases, and run the untouched cases once. Write a short change note. A pass after a thoughtful failure is as valuable as a first-attempt pass; hiding the failure destroys the evidence of learning.
