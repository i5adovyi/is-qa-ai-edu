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

Continue with lesson 10's copy of the [development sandbox](../dev-sandbox/README.md). Write expected results for below-limit, exactly-at-limit and already-over-limit calls to `take_step`. If you repaired the copy in lesson 10, inspect your saved failing result and original diff, then run the checks against the repaired copy; it should already pass. To reproduce the baseline again, copy the untouched fixture to a different, unused path such as `work/router-baseline/` and run the five starter checks there. Keep your repaired `work/router-practice/` copy intact. The exactly-at-limit case exposes the seeded defect only in the original fixture. Do not remove checks from the working reference harness to manufacture a failure. As an alternative exercise, create the deliberately faulty source validator from the worked example and test unknown, valid and empty source lists.

**Deliverable:** cases and failing result. **Pass:** the boundary case detects the chosen defect; the expected outcome does not depend on the buggy implementation.

## Exercise 2 · Build a repair loop

Implement the smallest repair, or review the repair already completed in lesson 10, then run the boundary cases and the relevant existing suite. For the sandbox, rerun `python3 -m unittest discover -s work/router-practice -p 'test_router.py' -v`; all five starter checks should pass, along with any extra boundary tests you added. Save a short log with hypothesis, change, result and next decision. Optional agent use: ask the agent to inspect the failure and propose a repair; review the patch before accepting its completion claim. Keep the original failure as a regression case.

**Deliverable:** patch, checks and repair log. **Pass:** the original failure is fixed; valid input still passes; rejected boundary inputs remain rejected; no unrelated test was weakened.

## Exercise 3 · Adversarial test quality

Create a mutant implementation that always admits a step, another that always rejects, and a subtle one that restores the erroneous inclusive `<=` boundary. Run your checks against each, restoring the repaired version afterward. For the alternative citation exercise, use always-success, always-failure and “accept any ID starting with `KB-`” mutants. Add a case only if it represents a real missing requirement boundary.

**Deliverable:** mutation table. **Pass:** the suite rejects all three mutants while accepting the correct implementation. Explain any intentionally uncovered behavior.

## Hints and solution outline

For the sandbox, the final permitted step starts below the limit; a new step must not start when `used == max_steps`. The three mutants check that your suite detects both excessive rejection and excessive admission. For the citation alternative, a tiny fixture set is sufficient: one available ID, one nonexistent ID and an empty list. The prefix mutant exposes the difference between syntactic validity and source existence. Use descriptive assertions and record reproducible observations and decisions. Running the reference harness suite can check that the academy remains intact, but it does not test your isolated sandbox patch.

Do not claim model reliability from these deterministic tests. They establish validator behavior. A separate evaluation checks how often proposed drafts need rejection and whether the final system handles that rejection usefully.

## Reflection

Which test would still be meaningful if the implementation were completely rewritten? Which one is coupled to incidental structure? What important failure could pass your current suite?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Python: unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Anthropic: Demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
