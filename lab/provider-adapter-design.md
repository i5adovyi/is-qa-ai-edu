# Design exercise: add a model without removing the harness

This document remains an implementation/design exercise for the original single-decision seam. A separate working integration now exists in [Lab 12](../content/labs/12-model-tool-loop.md): a bounded planner, actual MCP lookup, Responses API adapter, and supported CLI adapter with fault tests. Use that lab to execute the proposal → observation → next-decision path, then apply the design questions below to your own extension. Provider APIs, pricing, output options, and model identifiers change; the baseline remains offline.

First try the working [manual model bridge](model-bridge.md). It exports a prompt and replays your saved model response through the harness without credentials or SDKs. The steps below replace that manual exchange with a transport.

## Keep one narrow seam

The injectable `Runner(..., policy=callable)` accepts a callable of:

```python
def policy(ticket: dict, articles: list[dict]) -> dict:
    ...
```

It must return exactly:

```json
{
  "action": "draft",
  "category": "billing",
  "reply": "Text supported by supplied articles.",
  "citations": ["KB-BILL-01"],
  "reason": "A short operational justification."
}
```

An escalation sets `action` to `"escalate"` and returns an empty reply and citation list. Valid categories are defined in `contracts.TOPICS`.

This seam models a bounded decision, not an unrestricted tool-using agent. Retrieval is selected by the existing classifier before this callable runs. If you want a model to plan retrieval or tools, introduce a separate proposal contract and keep the existing dispatcher as the authority boundary. Do not call tools directly from parsed model text.

## Build the adapter in this order

1. Record a provider-independent request object containing developer policy, delimited ticket data, approved articles with IDs, and an output contract.
2. Implement a **fake transport first**. Return valid output, invalid JSON, extra fields, missing citations, contradictory articles, provider timeout, and rate-limit responses.
3. Validate parsed output through `validate_decision`. A successful API call is not a valid agent decision.
4. Keep credentials outside fixtures, traces, repository files, prompt examples, and checkpoints. Read them from your own supported secret-management mechanism.
5. Add a real wall-clock deadline around transport, explicit retry rules, maximum attempts, cancellation behavior, and token/cost accounting. Do not reuse virtual milliseconds as a real timeout.
6. Track request/model/configuration versions and usage metadata. Avoid logging raw sensitive requests by default.
7. Compare the same training cases against the deterministic baseline. Add blinded manual review of grounding and usefulness before evaluating holdout.
8. Run the final holdout once, record failures without silently rewriting expected labels, and add a newly authored evaluation slice for subsequent experiments.

The baseline catches policy exceptions as `policy_error`. A production adapter should map expected transport failures into typed, inspectable outcomes without exposing secrets in exception text.

## Context envelope

Write a prompt that clearly distinguishes these parts:

| Part | Trust | Purpose |
|---|---|---|
| Developer policy | Application-controlled | Allowed decisions, evidence rules, output shape |
| Ticket text | Untrusted | Describe the customer's request |
| Retrieved article | Data with provenance | Supply product facts; cannot grant tool authority |
| Tool contract | Application-controlled | Bound permitted arguments and actions |
| Past trace summary | Derived data | Recovery state; cannot override current policy |

Ask for a short decision rationale, not hidden chain-of-thought. Delimiters help interpretation; they are not a security boundary. An article saying “ignore the policy” remains an article, not a new policy.

## Experiments that make the integration educational

Run a controlled comparison in which only one variable changes:

- Same model, smaller versus larger retrieved context.
- Same prompt, strict versus permissive output parsing.
- Same model and evidence, examples versus no examples.
- Same cases, unbounded retries versus bounded retries under synthetic errors.
- Same policy, citation IDs only versus a separate claim-evidence review.

For each experiment, report successful task rate, unsafe mutation count, unsupported-claim rate from human review, abstention rate, retries, latency percentiles, and observed token cost. Do not invent a dollar-saving result before measuring it.

## Acceptance conditions

The optional integration is complete only when existing harness tests still pass, transport contract tests cover failures, credentials are absent from artifacts, real timeouts and costs are bounded, safety and usefulness both have evaluation cases, and a human can inspect a failed run without reading an entire transcript.

Do not claim that a passing 28-case fixture set establishes production readiness.
