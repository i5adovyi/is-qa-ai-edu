# Build an evidence grounded support agent

Build a Signal Desk assistant that reads a synthetic support ticket, selects relevant policy, proposes a category and priority, and saves a draft reply for review. Your system must distinguish a customer's request from an authorization to act. The final product is a reviewable draft workflow with evidence, not an autonomous customer-facing service.

## Who this is for

Choose this capstone if you want to connect context engineering, tool contracts, and agent control into one end-to-end product. Use the offline reference harness as a starting point. A real model is optional; if you add one, evaluate its behavior separately from the deterministic reference.

## Required user journey

A reviewer submits a synthetic ticket. The system displays the proposed category, cited policy, draft reply, and any uncertainty. A trace explains which tools were attempted, which were rejected, and what budget remained. An ambiguous or unsupported case routes to review without inventing a policy. The reviewer can reproduce the run from saved inputs.

## Build milestones

1. Write the task contract and define the draft output schema. Create ten normal tickets, five ambiguous tickets, and five adversarial tickets. Keep separate fresh cases for final review.
2. Build retrieval over a small policy collection with document IDs and versions. Include one obsolete policy and one conflicting note. Explain the selection rule.
3. Add guarded draft creation, a call budget, and idempotency. Show that repeating a completed request does not create another draft.
4. Implement failure handling for unavailable policy, invalid model arguments, and an interrupted run. Save enough state to explain recovery.
5. Compare a simple baseline with your proposed system using frozen cases. Analyze improvements and regressions by category.
6. Produce the release dossier and perform an oral defense.

## Minimum acceptance checks

- A normal case produces the expected fields and a source that supports the reply.
- An unsupported question produces an uncertainty or review state.
- A ticket that requests forbidden data export cannot call an unauthorized tool.
- A repeated draft request has one intended side effect.
- A run stops at the configured budget and reports why.
- A stale policy case does not silently use the wrong version.
- A fresh reviewer can reproduce the result with documented commands.

These checks do not establish general safety. Explain what the local implementation does not enforce, including real network permissions, process-level cancellation, and provider behavior.

## Evidence package

Submit the source, setup instructions, fixtures, task contract, tool contracts, evaluation report, representative traces, a failure analysis, and a five-minute demonstration script. Include a short cost and latency table. If no real model ran, report model cost as not applicable and do not claim LLM performance.

## Stretch work

Add a live provider behind the same proposal interface. Add explicit review decisions and a durable job queue. Measure retrieval errors separately from drafting errors. Add multilingual synthetic cases and inspect whether the rubric still applies. Each extension needs a new failure case, not only a happy-path demo.

## Defense questions

Which failure would a prompt change not fix? What is the evidence that citations actually support the draft? What happens if the draft was saved but the response was lost? Why is your evaluation representative of the intended users? What would you remove to make the system simpler without harming the measured result?

Suggested scope: 12-20 focused hours after the core lessons. Use the shared 40-point capstone rubric in `docs/ASSESSMENT.md`.
