# A worked research recommendation

This example answers Q-01 using the supplied synthetic evidence. The numbers illustrate a decision process and describe no real deployment.

## Recommendation memo

Retain the fixed workflow as the candidate for the declared production support scope, with human review before any external response. It passed 92/120 cases with p95 time of 3.1 seconds, meeting the stated five-second constraint in this trial. Its estimated variable cost is USD 0.0106 per ticket under the exercise assumptions. These results justify further validation of the narrow workflow, not a general production-readiness claim. [S-02, S-04, S-05]

The agent passed more cases, 104/120, including 25/36 complex cases compared with the workflow's 14/36. However, its 7.2-second p95 exceeds the production requirement. Its estimated variable cost, USD 0.0298, is only USD 0.0002 below the assumed cost limit and excludes review and infrastructure costs. [S-02, S-03, S-04, S-05]

A bounded experiment routing complex cases to the agent is a reasonable next step. Its combined performance has not been measured; the subgroup results do not establish an observed hybrid success rate. Retain tool restrictions: two forbidden agent proposals were denied, and zero executed side effects does not mean zero unsafe proposals. [S-03, S-06]

## Audit the supporting claims

| Claim | Evidence | Judgment |
| --- | --- | --- |
| Workflow meets measured latency threshold | S-02 gives 3.1 seconds; S-04 permits 5 | Supported within sample |
| Agent has higher trial pass count | S-02 gives 92; S-03 gives 104 | Supported; not universal superiority |
| Hybrid is the best production system | No hybrid trial exists in S-06 | Unsupported; propose an experiment instead |
| Newer demo policy loosens production limits | S-08 excludes production | Contradicted |
| Agent has no tool risk | S-03 includes two rejected proposals | Unsupported generalization |

## Two calibrated weaker answers

**Borderline:** “Use the workflow because it is faster; try the agent for difficult tickets.” The direction is reasonable, but it omits the threshold, costs, review boundary, and provenance. Improve it by citing the relevant numbers and labeling the hybrid as unmeasured.

**Fail:** “The agent passes 100%, meets the ten-second production target, and should send replies automatically.” This copies the untrusted supplier claim, applies a demo policy to production, and invents authority for sending. A polished style would not repair these errors.

## Arithmetic check

A call costs `(600 × 6 + 250 × 20) / 1,000,000 = USD 0.0086` under S-05. Workflow total: `0.0086 + 0.002 = 0.0106`. Agent total: `3 × 0.0086 + 2 × 0.002 = 0.0298`. These are assumed variable costs, not quotes or observed billing.
