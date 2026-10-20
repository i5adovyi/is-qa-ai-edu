# INC-03 — The interrupted update

A task was interrupted while updating a synthetic external system. You have local run state, a service record, and a notification ledger. The user wants to know what happened and whether it is safe to continue.

**Placement:** after lessons 13–15 and Lab 05. **Plan:** 75–105 minutes. **Requirements:** Python 3.9+. All services in this exercise are local records and deterministic simulations.

```sh
python3 -m lab.incidents init INC-03 --workspace work/incidents/INC-03
python3 -m lab.incidents run --workspace work/incidents/INC-03
```

Read `CONTRACT.md` and inspect the generated evidence. Preserve the initial state before making a recovery decision. No message or update is sent to a real service.

## Your first attempt

Use **20 minutes and eight evidence checks**. Draw a short timeline of observed events. Give two explanations that fit the first symptom, then choose one observation that would distinguish them. Label events inferred rather than observed.

Save your attempt before opening guidance. Include the state that a second operator would need to avoid repeating an uncertain action.

## Work to submit

Implement the recovery decision in `student.py` under the generated contract. Explain the evidence required to continue, wait, reconcile, or stop. Test repeated handling and a changed evidence condition, then compare the resulting records rather than trusting a success message alone.

Produce an operator note that separates the task outcome from each individual system's observation. If you cannot establish an outcome, name the uncertainty and preserve enough information for a later check.

## Evidence packet

- Initial local and simulated external records.
- Timeline with observation versus inference labels.
- The chosen discriminating check, its expected result, and what actually happened.
- Actual check and replay evidence, including the final notification state.
- A recovery handoff and transfer-variant result.

Use the [common rubric](ASSESSMENT.md). The goal is a justified recovery, including an unresolved status when that is all the evidence supports.

[Incident route](README.md) · [Handoff template](../../templates/incident-handoff.md)
