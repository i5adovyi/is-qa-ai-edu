# INC-CAPSTONE — The release rehearsal

Your chosen project has a working baseline. During a release rehearsal, an interrupted operation and a changed persisted record complicate the next decision. Several artifacts disagree about what is current. Prepare a defensible recovery without assuming that an earlier checklist fits this case.

**Placement:** during weeks 11–12, after a working baseline for one chosen capstone. **Plan:** 150–210 minutes. **Requirements:** Python 3.9+ and access to your own local capstone evidence.

```sh
python3 -m lab.incidents init INC-CAPSTONE --project support --workspace work/incidents/INC-CAPSTONE
python3 -m lab.incidents run --workspace work/incidents/INC-CAPSTONE
```

In the initialization command, replace `support` with `qa` or `research` if that is your existing capstone. Select one project; do not run three capstones. The fixture's technical contract is shared, while the generated brief names the chosen context.

Begin with the unfamiliar supplied fixture. Read its generated contract, record the initial state, and produce a first attempt without opening earlier incident debriefs.

## Your first attempt

Allow **30 minutes and twelve evidence checks**. State the current user outcome, two competing explanations, what must be preserved, and the cheapest useful next check. Describe the consequence of choosing incorrectly.

Save the attempt before requesting guidance. The first investigation budget is for diagnosis and containment, not a promise that the entire exercise fits in half an hour.

## Recover the fixture

Implement the generated decision contract in `student.py`. Preserve the initial records, show the actual outcome of your checks, and explain what makes a recovery action compatible with the state that now exists. Consider whether the data can be read and written correctly after the proposed change, as well as whether the code can start.

Produce a release or hold decision, a recovery handoff, and a changed-case prediction. Do not certify an external service or real migration from this deterministic fixture alone.

## Adapt it to one project

Use the [capstone incident defense](../../capstones/incident-defense.md). Choose support, QA or research according to your existing capstone; do not build all three. Reproduce an analogous failure in a disposable copy of that product, using a new input and your own evidence.

Keep the product's smallest useful journey. The incident should challenge a real assumption in that journey and add one regression test or reproducible check. It should not become a second unrelated application.

## Submit and defend

Submit the first attempt, evidence timeline, narrow recovery or justified hold, actual checks, transfer run, and one-project adaptation. A reviewer should be able to reproduce the starting symptom, identify what your evidence proves, and challenge one changed condition.

Use the existing 40-point capstone rubric. The [incident rubric](ASSESSMENT.md) helps diagnose weaknesses; it does not replace the common capstone standard or award an additional credential.

[Incident route](README.md) · [Capstone incident defense](../../capstones/incident-defense.md)
