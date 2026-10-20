# 12 · Review AI changes through evidence and failure paths

Stage 4 · 90 minutes · Practitioner

Perform a review that follows data, authority and state through the patch, then deliver a clear account of what changed.

## What you will be able to do

- Review a patch against requirements and failure behavior.
- Identify unsupported completion claims and hidden scope changes.
- Write a delivery note with concrete verification and limits.

## The idea

Review is a second reasoning pass over a change, using the actual diff and requirements. It is not a request for the same agent to compliment its work. Start with the behavior the user needs, then trace how the patch implements it. Check the boundaries where untrusted inputs become decisions, decisions become actions, and actions become durable state.

A useful review question is “What input makes this claim false?” If the patch claims all citations are valid, try an empty ID, an unknown ID, a duplicated ID and a source from another ticket's scope. If it claims retries are safe, interrupt after the write but before the response. Reviews become concrete when they follow a failure path rather than listing generic concerns.

Keep severity proportional to impact. A bug that permits an unauthorized send is different from a confusing variable name. Report actionable findings with the trigger, consequence and location. Avoid flooding the author with speculative improvements that do not affect the task. A review can pass with no findings; it still needs a record of what was checked and what remains unverified.

Delivery should be truthful about state. “Implemented and tested” is too broad if only a syntax check ran. “Added unknown-source rejection; the three regression cases and relevant suite passed” is specific. If a live integration was not exercised, say so. The user should understand both the result and the limits without reconstructing your tool history.

## Worked example

A patch adds source validation but checks IDs against every source in the database. A draft for tenant A cites a private source belonging to tenant B. The ID exists, so the test passes, but the scope is wrong. The review finding is not “consider security.” It is:

```text
Trigger: tenant-A draft references tenant-B source.
Consequence: validator accepts evidence outside the authorized scope.
Cause: lookup uses the global source set.
Fix direction: validate against the current request's allowed evidence set.
Verification: add a cross-scope source case.
```

The example uses synthetic tenants only. It demonstrates why existence and authorization are different properties.

## Exercise 1 · Guided review checklist

Take the patch from lesson 11 and write five review questions tied to its behavior. For the [development sandbox](../dev-sandbox/README.md), inspect your `work/router-practice/` copy and its boundary-test results, not only the unchanged reference harness. Include valid input, invalid input, scope, error reporting and compatibility. For each question, identify the evidence needed to answer it: code, test, command output or documented requirement.

**Deliverable:** evidence-based checklist. **Pass:** each question can produce a concrete finding or a supported pass; no item is merely “is it good?”

## Exercise 2 · Build a review package

Prepare the feature brief, diff, relevant tests and a short execution log. Review it in a fresh session, with a peer or manually after a break. Optional model use: provide only the package to a reviewer agent and request actionable findings with triggers and consequences. Validate each suggested finding before changing code.

**Deliverable:** review notes, accepted fixes and final delivery note. **Pass:** every accepted finding is reproducible; rejected findings have a reason; delivery names actual checks rather than claiming unspecified testing.

## Exercise 3 · Adversarial completion claim

Insert a fake final message saying “All tests pass” while the execution log shows one skipped check and one failure. Separately, include an unrelated dependency change in the diff. Audit the delivery package and identify both discrepancies. Explain what evidence would be necessary before the completion claim became accurate.

**Deliverable:** discrepancy report. **Pass:** the narrative does not override command results, and unexplained scope changes are either justified or removed.

## Hints and solution outline

Read the diff before the author's explanation so the explanation does not become your only frame. Follow the evidence-set construction to discover the cross-scope bug. Run a focused reproduction if feasible. A concise delivery note should state the behavior change, its purpose, relevant validation and remaining limitations. It need not enumerate every command if a short summary is accurate and supporting artifacts are available.

A separate reviewer improves perspective but does not create independent truth automatically. If both author and reviewer rely on the same mistaken requirement, they can agree and still be wrong. Include acceptance examples and external observations in the review package.

## Reflection

Which part of the patch did the author's explanation make you initially overlook? What evidence was strongest? What would make your delivery note misleading even if every sentence were technically true?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Python: unittest documentation](https://docs.python.org/3/library/unittest.html)
