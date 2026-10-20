# Debug a seeded budget defect

This is an intentionally broken exercise fixture for lessons 10–12. It is separate from the passing Signal Desk reference harness. The function promises at most `max_steps` successful calls, but the supplied implementation accepts one extra call at the boundary.

## Start from a disposable copy

Run these commands from the academy project directory. If `work/router-practice` already exists, choose a new destination rather than overwriting an earlier attempt.

```sh
mkdir -p work
cp -R content/dev-sandbox work/router-practice
python3 -m unittest discover -s work/router-practice -p 'test_router.py' -v
```

Expected baseline: **five tests, one failure**. The failing case is `test_exhausted_budget`. The command exits nonzero by design. Do not edit the reference lab or weaken the test to make it pass.

## Write the request before using an assistant

Explain the trigger: `take_step(3, 3)` returns `4`, although all three permitted steps are already consumed. Ask for a minimal patch that preserves the public function signature and its validation of negative counts and non-integer inputs. Require the assistant to explain why its change follows from the contract.

## Verify more than the supplied case

After the fix, all five supplied tests should pass. Add a zero-budget test and an already-over-budget test. A zero budget must not permit the first call. Compare the assistant's patch with the intended change, then write a review comment explaining the user-visible effect of the boundary defect.

## Evidence to retain

Save the original failure, your task contract, the patch, the final output, and one short review note in your practice directory. In a version-controlled copy, use a small commit; otherwise save a unified diff. Record any test that you proposed but did not execute as unexecuted.

## Solution guidance

The acceptance comparison must be strict: `used < max_steps`. This permits a call when one or more steps remain and rejects a call when the budget is exhausted. This fixes the supplied defect; it does not add a wall-clock timeout or an operating-system sandbox. Try the exercise before revealing the implementation to an assistant.
