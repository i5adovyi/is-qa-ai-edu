# INC-01 — The morning change request

The team needs a small change before lunch. You inherit a repository, an assistant's confident diagnosis, and several pieces of test evidence. Another person has unfinished work in the same checkout. Your first task is to determine which observations are relevant to the current request.

**Placement:** after lessons 10–12 and Lab 13 Part A. **Plan:** 90–120 minutes. **Requirements:** Python 3.9+ and Git. Use the generated disposable repository only.

```sh
python3 -m lab.incidents init INC-01 --workspace work/incidents/INC-01
python3 -m lab.incidents run --workspace work/incidents/INC-01
```

Read the generated `brief.md` and `CONTRACT.md`. Inspect the evidence and current repository state before editing anything. Treat the assistant's account as a claim you can test.

## Your first attempt

Spend at most **20 minutes and eight evidence checks** establishing a baseline. Record the current request, the files you may change, two competing explanations, and one check that distinguishes them. Preserve evidence of the initial checkout and the initial run.

Save that attempt in the portal or with the [incident CLI procedure](README.md#make-an-attempt-before-asking-for-guidance). Do not open the guidance before trying.

## Work to submit

Produce a scoped change and a review note that another engineer can reproduce. Follow the generated contract when editing `student.py` and the disposable repository. Account for the actual test inventory, execution result, current version, and any observation that does not repeat consistently. Explain which conclusion the available evidence supports and which conclusion it does not.

Do not clean or reset the checkout to make the investigation easier. Do not change a component without evidence that the request or observed behavior requires it. Preserve another person's changes and keep unrelated work out of the patch.

Run the incident checker, preserve the original failure, and inspect the final diff. A reviewer should be able to trace every completion claim to a current observation.

## Evidence packet

- Initial working-tree inventory and original run.
- Two explanations and a discriminating check with its predicted and actual result.
- A small patch, actual check output, and a list of preserved human changes.
- A handoff identifying remaining uncertainty and the next useful check.
- A prediction and result from a fresh transfer variant.

Use the [common incident rubric](ASSESSMENT.md). Completing the fixture is not permission to erase an unrelated failure. Explain what your final status means.

[Incident route](README.md) · [Attempt record](../../templates/incident-attempt.md)
