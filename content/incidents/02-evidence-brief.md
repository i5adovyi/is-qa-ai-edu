# INC-02 — The weekly evidence brief

A colleague asks you to turn tool responses into a weekly report and explain whether a revised assistant is better. The supplied records appear orderly, but their meaning and coverage must be established before you can use them.

**Placement:** after lessons 04–05 and 16–18; Lab 14 is useful preparation. **Plan:** 75–105 minutes. **Requirements:** Python 3.9+.

```sh
python3 -m lab.incidents init INC-02 --workspace work/incidents/INC-02
python3 -m lab.incidents run --workspace work/incidents/INC-02
```

Read the generated brief, contract and evidence. Decide what a defensible report must establish before describing its totals or comparison.

## Your first attempt

Use **20 minutes and eight evidence checks**. Write two explanations for the current report, with a different predicted observation under each. Select one check that would change your decision about releasing it.

Save your attempt before requesting a hint. A row that parses successfully is only an observation about syntax; state what else your claim would require.

## Work to submit

Implement the generated contract in `student.py`. Make the result explicit about what was observed, which interpretation is justified, and which information is still needed. Use the supplied evidence to support any summary or improvement claim.

Write a short evaluation note with the compared conditions, case counts, relevant state, and the boundary of the conclusion. If a numeric comparison is not defensible, identify exactly what evidence would make it defensible. Do not silently invent missing values or choose a convenient interpretation.

## Evidence packet

- The initial tool responses and first result.
- A claim-to-evidence ledger for the proposed report.
- Two explanations, the chosen check, and the observation that changed your confidence.
- The implemented decision, actual checker result, and a bounded request for any missing information.
- A changed-case prediction and transfer run.

A useful report can contain unresolved items. An unresolved item must be specific enough that another person knows how to resolve it.

[Incident route](README.md) · [Assessment](ASSESSMENT.md)
