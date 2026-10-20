# Defend your chosen capstone through an incident

Complete [INC-CAPSTONE](../content/incidents/07-release-rehearsal.md) after your project has a working baseline. First investigate the supplied unfamiliar fixture; then adapt one of its pressures to **the same product you already chose**. Do not add a second full support project when your capstone is QA or research.

This investigation is planned for 150–210 minutes in addition to the six short incidents. You may absorb it into your existing hardening sessions if those sessions have sufficient time, but record the actual time rather than counting the same hours twice.

## Keep the adaptation small

Choose one existing journey and create a disposable copy or isolated fixture. Save its initial state before introducing a failure. Use fictional records. Do not interrupt real customer operations or test with production credentials.

| Your chosen project | Existing journey to challenge | Evidence to preserve |
| --- | --- | --- |
| Support agent | Continue one authorized update after an interrupted run | Request identity, relevant operation records, pending work, final user-visible state |
| QA copilot | Resume one review after the change or execution environment moves on | Current diff, test inventory, execution provenance, report revision |
| Research workflow | Continue one evidence brief after source or persisted-record changes | Source versions, completeness observations, claim ledger, current output contract |

Choose a persisted record that the journey actually uses. Define two small versions of that record and their compatibility requirements. Rehearse the proposed recovery against existing records and newly written records. Demonstrate what is preserved, what cannot be reconstructed, and which action you would hold pending better evidence. A version label alone is not a migration test.

Do not reuse the supplied incident's exact input as your own final capstone case. Change the domain values and one structural condition, then predict the result before execution. Explain why your new case tests the same principle rather than merely changing names.

## Defense packet

1. **First attempt:** competing explanations, observed evidence, the next discriminating check, and your initial prediction.
2. **Timeline:** observed events with paths and versions; mark inferences and unknowns.
3. **Decision:** release, hold, containment, clarification, or a narrow repair, with the evidence needed to justify it.
4. **Actual verification:** baseline symptom, final relevant result, replay or resumed-state check, and a changed-condition result.
5. **Useful outcome:** which user journey is restored or safely paused, and what the user is told.
6. **Handoff:** pending actions, incompatible late results, remaining uncertainty, and one next check.

Use the [attempt record](../templates/incident-attempt.md) and [handoff template](../templates/incident-handoff.md). Preserve earlier failed attempts and list any hint or debrief use.

## Questions for a reviewer

- Which observation would make your favored explanation wrong?
- Which artifact is tied to the current input and current code?
- What does your final check fail to establish?
- What happens to a result that arrives after your decision?
- Is your proposed recovery compatible with the records already written?
- If a stakeholder rejects the technically correct result, which acceptance condition must be clarified?
- What would you do if the next check cannot establish the outcome within the available budget?

Use the [single common capstone rubric](../docs/ASSESSMENT.md#capstone-scoring): 30/40 suggested minimum, no dimension below 2, and no unauthorized side effects. Apply the incident evidence to the existing dimensions, especially incident readiness, reproducibility, data handling and user usefulness. A simulated pass remains a simulated pass.
