# 21 · Measure whether your agent team is actually better

Stage 7 · 90 minutes · Advanced

Compare a team with a single-agent baseline using outcome quality, coordination failures and total resource use.

## What you will be able to do

- Construct a fair paired comparison of team and baseline.
- Measure coordination overhead and correlated mistakes.
- Choose an architecture based on observed tradeoffs.

## The idea

A multi-agent demonstration can look impressive because it exposes many visible activities. Activity is not value. Evaluate the final outcome, severe failures, latency, cost and operator effort. A team that produces a slightly better draft after five times the work may still be appropriate for difficult cases, but the tradeoff should be explicit.

Use the same tickets, evidence access and acceptance rubric for the baseline and team. Record architecture differences honestly. If the team gets extra documents or a stronger model, its improvement cannot be attributed solely to delegation. You may still prefer the combined design, but the experiment answers a different question. Isolate variables when diagnosing the cause of improvement.

Measure coordination failures separately: stale output accepted, conflicting findings silently merged, duplicate work, missing worker result and unsupported consensus. These can coexist with a good final answer in a small demo. Tracking them helps predict operational burden. Include the parent's integration time and every worker's resource use in the total.

Agreement is not independent confirmation when workers share evidence, prompts or models. Three workers repeating one incorrect policy excerpt can produce unanimous error. Encourage distinct evidence checks where useful, but do not assume role prompts alone create statistical independence. The strongest final decision comes from validating the relevant claim against appropriate evidence.

## Worked example

On ten synthetic tickets, a single agent produces eight acceptable drafts in 40 total work units. A team produces nine in 95 units and accepts one stale policy result. The team improves one outcome and introduces a coordination defect. A sensible next experiment routes only the three complex cases to the team and keeps ordinary cases on the baseline. This is a hypothesis to test, not a guaranteed optimization.

Define a work unit consistently, such as simulated tool calls plus review minutes in separate columns. Do not add dollars, tokens and seconds into one arbitrary total without explaining the weighting. Operational decisions often require viewing several metrics side by side.

## Exercise 1 · Guided comparison plan

Write a plan comparing a single worker with your lesson 20 team on eight tickets. Hold evidence and rubric constant. Include four normal cases and four requiring conflicting-source resolution. Define usefulness, severe failure, total calls, elapsed time and integration effort before running.

Author these eight tickets and their expected outcomes before the comparison; SD-120 is a starting example, not a supplied eight-case dataset. For every conflict case, include both source excerpts and their applicability rule so each system receives the same solvable evidence problem.

**Deliverable:** experiment plan. **Pass:** both systems face the same inputs and policy; the plan identifies any unavoidable confounders.

## Exercise 2 · Build the experiment

Run both systems using scripted roles, humans or optional models. Record paired case results and every coordination event. Compare totals and the difficult-case subset. If using simulations, describe exactly how outputs were authored and avoid presenting the result as evidence of live-model performance.

**Deliverable:** paired table, traces and architecture decision. **Pass:** the decision considers regressions and resource use, and all worker costs or effort are included.

## Exercise 3 · Adversarial consensus

Give all workers the same incorrect but authoritative-looking note. Then give one worker a verified conflicting source. Test whether the team votes by count or investigates source applicability. Create a case where two workers share a copied error and the third is correct. Compare majority vote with evidence-based adjudication.

**Deliverable:** consensus failure analysis. **Pass:** the final decision can reject the majority when its evidence is weaker; copied findings are not counted as independent corroboration.

## Hints and solution outline

Use a case-level table with baseline outcome, team outcome, difference, tool calls, time and coordination notes. Inspect discordant cases before averaging. A selective-routing architecture may be justified if teamwork helps only difficult cases; test the router too, because misrouting can erase the gain. Do not optimize only for cost: an extra review step may be worthwhile when it prevents a severe failure. State the intended workload and consequence model that support your choice.

## Reflection

What evidence would make you remove an agent from the team? Which improvement came from better instructions rather than parallelism? What new failure does your coordination layer create that the single-agent baseline cannot have?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
