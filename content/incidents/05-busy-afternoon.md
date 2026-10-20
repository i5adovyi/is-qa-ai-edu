# INC-05 — The busy afternoon

The workflow is reliable in a small demonstration. This afternoon, several workers process tasks together and the queue stops behaving as expected. Each worker's local account sounds reasonable; the combined outcome still needs explanation.

**Placement:** after lessons 14–15 and 19–21 and Lab 13 Part B. **Plan:** 90–120 minutes. **Requirements:** Python 3.9+. Time, service responses and competing operations are modeled locally.

```sh
python3 -m lab.incidents init INC-05 --workspace work/incidents/INC-05
python3 -m lab.incidents run --workspace work/incidents/INC-05
```

Read the generated contract and inspect the combined trace as well as individual worker observations. Preserve the first run before changing scheduling behavior.

## Your first attempt

Use **20 minutes and eight evidence checks**. State two explanations that predict different behavior when one condition changes. Choose a small comparison that could separate them without increasing the workload indefinitely.

Save the attempt before requesting a hint. Record the budget for the whole investigation and the unit in which it is counted.

## Work to submit

Implement the generated decision contract in `student.py`. Explain how the final outcome relates to all workers and pending operations. Re-run a boundary condition, then show how the system behaves when another result arrives after the state has moved on.

Keep a ledger of total logical work, stops, deferred work and unresolved conflicts. The simulator's logical counts are not provider billing measurements. Do not use the fastest worker alone as the cost of the full workflow.

## Evidence packet

- Initial combined trace and the relevant individual observations.
- Competing explanations and a discriminating check.
- A narrow change with actual check output and global accounting.
- A recovery decision for pending or incompatible work.
- A transfer prediction, changed-case result, and an explanation of the remaining limit.

Use the [common rubric](ASSESSMENT.md). An orderly stop can be a better outcome than an unbounded run; it still needs evidence and a useful handoff.

[Incident route](README.md) · [Attempt record](../../templates/incident-attempt.md)
