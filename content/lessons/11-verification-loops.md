# 11 · Use verification loops that catch real defects

Stage 4 · 90 minutes · Practitioner

Drive a coding change with independent checks and learn why an agent saying its work is correct is not evidence.

## What you will be able to do

- Write behavioral tests that can fail for the right reason.
- Use failures to guide one bounded repair at a time.
- Distinguish assertions about behavior from implementation mirroring.

## The idea

A coding agent can generate a patch, run checks and revise it. The value comes from the quality of the feedback loop. If the tests simply repeat the implementation's assumptions, the loop can converge confidently on the wrong behavior. Choose checks that represent the user's requirement independently of how the code is written.

For Signal Desk, “a citation must refer to an available source” is a behavioral rule. A test that calls the validator with an unknown ID and expects rejection directly exercises it. A test that asserts a helper function was invoked exactly once may be useful in a narrow architecture test, but it does not establish that unsupported citations are rejected.

Before repairing a bug, create a case that demonstrates it. Observe the failure, make a focused change, then rerun the case. This is a practical discipline, not a requirement to write exhaustive tests for every cosmetic edit. Spend verification effort where behavior, authority, state or recovery can go wrong. Reversible wording changes can often be inspected directly.

A passing command proves only what it actually checked. Record the command, exit status and relevant result. If a dependency is missing, say the check could not run. If you changed a test to match a new requirement, explain the requirement change. Never turn a failure into success by weakening the assertion without justification.

## Worked example

Suppose the validator accepts any nonempty `evidence_ids` list. A draft containing `KB-DOES-NOT-EXIST` passes. The regression case is:

```python
available = {"KB-EXPORT-2"}
draft = {"evidence_ids": ["KB-DOES-NOT-EXIST"]}
# Expected behavior: reject with an unknown-source error.
```

The repair checks membership in the available source set. Add a valid-source case and an empty-evidence case because these boundaries could regress. Do not test only the helper's internal data structure. Your requirement is about whether the draft crosses the validation boundary.

## Exercise 1 · Guided failure

Write three tests or manual cases for unknown, valid and empty source lists. Run them against a deliberately faulty validator that only checks list length. Confirm which case fails and why. Label every expected result before inspecting the implementation.

**Deliverable:** cases and failing result. **Pass:** the unknown-source case detects the defect; the expected outcome does not depend on the buggy implementation.

## Exercise 2 · Build a repair loop

Implement the smallest repair, then run the three cases and the relevant existing suite. Save a short log with hypothesis, change, result and next decision. Optional agent use: ask the agent to inspect the failure and propose a repair; review the patch before accepting its completion claim. Keep the original failure as a regression case.

**Deliverable:** patch, checks and repair log. **Pass:** the original failure is fixed; valid input still passes; empty input retains the intended behavior; no unrelated test was weakened.

## Exercise 3 · Adversarial test quality

Create a mutant implementation that always returns success. Create another that always returns failure. Run your tests against both. Then create a more subtle mutant that accepts any ID starting with `KB-`. Determine whether your suite detects it. Add one case only if it represents a real missing requirement boundary.

**Deliverable:** mutation table. **Pass:** the suite rejects all three mutants while accepting the correct implementation. Explain any intentionally uncovered behavior.

## Hints and solution outline

A tiny fixture set is sufficient: one available ID, one nonexistent ID and an empty list. The prefix mutant exposes the difference between syntactic validity and source existence. Use descriptive assertion messages so a failure points to behavior. The repair log should not include every internal thought; it should contain reproducible observations and decisions. For the bundled lab, run `python3 -m unittest discover -s tests -p 'test_lab*.py'` after adapting the case to its actual schema.

Do not claim model reliability from these deterministic tests. They establish validator behavior. A separate evaluation checks how often proposed drafts need rejection and whether the final system handles that rejection usefully.

## Reflection

Which test would still be meaningful if the implementation were completely rewritten? Which one is coupled to incidental structure? What important failure could pass your current suite?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Python: unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
