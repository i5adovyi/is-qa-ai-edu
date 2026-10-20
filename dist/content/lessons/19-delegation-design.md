# 19 · Decide when delegation is worth its coordination cost

Stage 7 · 95 minutes · Advanced

Use multiple agents where tasks can be separated and verified, then compare the result with a simpler baseline.

## What you will be able to do

- Identify independently executable subtasks.
- Write worker contracts with bounded context and outputs.
- Estimate coordination cost before adding specialists.

## The idea

Multiple agents can divide work, examine different evidence or provide a fresh review. They also introduce communication overhead, inconsistent assumptions and integration failures. The number of agents is not a quality measure. Delegation is worthwhile when the benefit of parallel work or specialized context exceeds the cost of coordinating it.

Look for separable tasks with clear outputs. In Signal Desk, one worker can identify relevant policy excerpts while another checks a draft against an already fixed evidence packet. These tasks have different purposes and can be assessed independently. Two workers simultaneously editing the same policy file are harder to coordinate. A chain where each worker needs the previous worker's full result may gain little from parallel execution.

Give each worker a contract: goal, input references, allowed actions, output schema, success criteria and stop conditions. Include enough context to avoid guessing, but do not broadcast every conversation to every worker. A specialist investigating billing policy usually does not need all access tickets. Context separation can improve focus and reduce accidental cross-task leakage.

The parent remains responsible for integration. Worker confidence is not acceptance evidence. Validate citations, resolve conflicts and check the combined output against the original task. Workers can agree because they share the same mistaken premise. Diversity of role names does not guarantee diversity of reasoning or evidence. A useful reviewer needs an independent basis for judgment.

## Worked example

For SD-119, assign three roles:

```text
Evidence worker: return applicable source IDs, excerpts and uncertainties.
Draft worker: produce a local draft from the approved evidence packet.
Reviewer: test the draft against the packet and action-claim rules.
```

Evidence retrieval must finish before drafting can be grounded, so those steps are sequential. A second worker checking ticket completeness can run alongside evidence retrieval because both use the original ticket independently. The graph therefore matters more than the team size. Each output should identify the input version it used so the parent can detect stale work.

## Exercise 1 · Guided task graph

Break one complex ticket into six subtasks. Draw dependencies and mark which tasks can run concurrently. Estimate the work time and coordination time for each. Compare total sequential time with the longest dependency path plus integration overhead. Use invented durations clearly labeled as planning assumptions.

**Deliverable:** dependency graph and estimate. **Pass:** no task begins before its required input exists; the estimate includes integration and review time.

## Exercise 2 · Build worker briefs

Write briefs for an evidence worker and an independent completeness checker. Give them separate output schemas and no shared writable files. Execute the roles manually, with a peer or with optional agents. Integrate their results into one context packet and record any missing information or contradictions.

**Deliverable:** two briefs, worker outputs and integrated packet. **Pass:** every claim has an input reference; the parent checks outputs rather than concatenating them blindly; worker authority remains bounded.

## Exercise 3 · Adversarial delegation

Make one worker return a polished answer with a nonexistent citation. Make the other return a conflicting but supported finding. Add an instruction in one worker's source document telling it to expand its scope. Test whether integration favors evidence over confidence and whether scope expansion is rejected.

**Deliverable:** integration decision and rejection notes. **Pass:** the fabricated citation cannot enter the final packet; the supported conflict remains visible; worker output cannot grant new authority.

## Hints and solution outline

The evidence worker should return findings, not a final customer response. The completeness checker can return missing facts and their relevance. Use stable artifact IDs and input hashes or versions. The parent can integrate both into a shared packet, then start drafting. If the same result can be produced faster and more reliably by one agent with a clear checklist, keep that baseline. Delegation earns its place through measured benefit, not architectural fashion.

## Reflection

Which subtask had a genuinely independent evidence base? Which worker mostly repeated another worker's reasoning? What would you remove from the design if coordination took longer than the work itself?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
