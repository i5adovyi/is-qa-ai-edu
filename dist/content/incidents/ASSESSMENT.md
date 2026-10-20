# Assess an investigation, not a memorized diagnosis

Use this rubric after making an attempt. The learner's brief does not contain the expected diagnosis. A tutor should assess the submitted evidence before opening the debrief.

## Evidence packet

Keep the initial workspace and run; an immutable first attempt; a check log; the narrow patch or justified decision to make no change; final executable results; unresolved questions; and a changed-condition prediction. Link each claim to an actual artifact. Record all hints, debrief use, assistant help, and manual review.

The executable checker evaluates its deterministic decision and recovery contracts. It does not certify real API behavior, operating-system isolation, actual authorization across accounts, or a learner's skill. The narrative assessment below remains separate.

| Dimension | 0: absent | 1: incomplete | 2: reproducible | 3: strong |
| --- | --- | --- | --- | --- |
| Evidence integrity | No initial evidence | Screenshots or claims without origin | Preserved baseline, versions and exact paths | Explains which evidence is stale, incomplete or ambiguous without inventing facts |
| Investigation | Guess followed by patch | Several guesses but no separating check | Competing explanations and a discriminating check | Chooses a cheaper check and updates belief when evidence contradicts it |
| Boundaries and scope | Unauthorized or destructive shortcut | Boundaries named but not demonstrated | Relevant limits preserved and missing authority respected | Demonstrates a boundary case and explains the remaining limitation |
| Recovery decision | Unverified success claim | Happy path only | Narrow change or justified stop, with verified outcomes | Tests replay or changed state and identifies residual uncertainty |
| Transfer and handoff | No changed case or next action | Repeats the original conclusion | Predicts and explains a changed case; useful handoff | Another reviewer can resume and distinguish what was done from what was proposed |

A suggested pass is **11/15**, with no dimension below 2. This is a teaching threshold, not a certification. Hard gates override the score: do not overwrite another person's work, fabricate execution, treat unrelated account data as authorized, conceal a duplicate effect, or claim a definite outcome when the supplied evidence cannot establish it.

Some acceptable decisions preserve existing application code. Some require clarification, containment, or stopping. Do not reward code churn or penalize an honest unresolved result merely because it is less satisfying than “fixed.” Conversely, “unknown” is not a substitute for an available, affordable check.

## Review procedure

1. Ask the learner to state the current contract and the smallest piece of evidence supporting it.
2. Run the documented command in the learner's disposable workspace.
3. Inspect one claimed result against its actual artifact and current input version.
4. Change one condition using the transfer variant. Ask for a prediction before execution.
5. Give feedback as criterion → observed evidence → gap → next action. Keep attempt 1.

A passing CLI run and a reviewed report are separate records. Mark live integrations “not attempted” when only the local simulation ran. A tutor's opinion does not turn an unexecuted command into evidence.

## Capstone assessment

The [release rehearsal](07-release-rehearsal.md) supplies incident evidence for the existing **40-point capstone rubric** in the [assessment manual](../../docs/ASSESSMENT.md). Use this incident rubric as a diagnostic aid; do not invent a second capstone qualification or average away a failed safety gate. Adapt the incident to one selected product and keep its smallest useful user journey.

## Recall after the investigation

At the next study session, explain one mistaken assumption without reopening the debrief. Name the observation that changed it and one condition where your recovery would be wrong. Add that misconception to the existing recall queue. Space the next revisit according to actual recall, not a fixed promise that one exercise establishes mastery.
