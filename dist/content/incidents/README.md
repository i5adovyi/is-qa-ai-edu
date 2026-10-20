# Practice with an incident you have not solved yet

These seven investigations begin with an imperfect workspace and a user who needs a useful outcome. Your job is to establish what happened, choose the next informative check, and make a defensible recovery decision. A plausible explanation alone does not pass.

The six short incidents connect earlier lessons. The final incident adapts to **one** existing capstone. They use fictional data and local deterministic simulations; they do not call paid models, send notifications, or alter a real customer system. Some parts use a real disposable Git repository. You need Python 3.9+; incident 01 also needs Git.

## Choose the next investigation

The identifiers are stable exercise IDs, not a required order. Follow the placement column.

| Incident | When to attempt it | Planning range | Learner brief |
| --- | --- | --- | --- |
| INC-01 | After lessons 10–12 and Lab 13 Part A; around week 5 | 90–120 minutes | [The morning change request](01-morning-change.md) |
| INC-03 | After lessons 13–15 and Lab 05; around week 6 | 75–105 minutes | [The interrupted update](03-interrupted-update.md) |
| INC-04 | After lessons 07–09 and 13–15; revisit Lab 10; around weeks 6–7 | 75–105 minutes | [The Monday workspace](04-monday-workspace.md) |
| INC-02 | After lessons 04–05 and 16–18; around week 7 | 75–105 minutes | [The weekly evidence brief](02-evidence-brief.md) |
| INC-05 | After lessons 14–15 and 19–21 and Lab 13 Part B; around week 8 | 90–120 minutes | [The busy afternoon](05-busy-afternoon.md) |
| INC-06 | After lessons 06, 12, 20 and 22–23; around week 9 | 75–105 minutes | [The resumed delivery](06-resumed-delivery.md) |
| INC-CAPSTONE | During weeks 11–12, after a working baseline for your chosen project | 150–210 minutes | [The release rehearsal](07-release-rehearsal.md) |

The six incidents add roughly **8–11 hours**. The capstone investigation needs another **2.5–3.5 hours**. These are unpiloted planning ranges. Reserve the time explicitly; see the [study plan](../../docs/STUDY-PLAN.md). You can replace repetitive optional case authoring with an incident after meeting that lesson's original gate. Do not replace a missing prerequisite or quietly award its completion.

## Start from the project root

Read the chosen brief, then initialize its own disposable workspace:

```sh
python3 -m lab.incidents init INC-01 --workspace work/incidents/INC-01
python3 -m lab.incidents run --workspace work/incidents/INC-01
```

Substitute the chosen incident ID and path consistently. Read `brief.md`, `CONTRACT.md`, `input.json`, `student.py`, and `evidence/` in the generated workspace. Keep its original baseline and run artifacts. The supplied implementation is intentionally incomplete; an initial failing check is learning evidence, not a broken academy installation.

Do not modify the academy's runtime to make an incident pass. Work on the generated `student.py` and, for incident 01, inspect its disposable repository. Keep human changes intact. Treat `run` as a local simulation and `check` as a test of the stated behavior; neither establishes how a real provider will behave.

## Make an attempt before asking for guidance

Use the portal's incident workspace or [investigation record](../../templates/incident-attempt.md). Record:

1. Two plausible explanations, including what evidence would disprove each.
2. At least one observation with an exact artifact path, field, command, or trace event.
3. One discriminating next check and the result you predict under each explanation.

The CLI can save an attempt against a real workspace evidence file:

```sh
python3 -m lab.incidents attempt --workspace work/incidents/INC-01 --hypothesis "Write your current explanation here" --evidence evidence/YOUR-OBSERVED-FILE --next-check "Write the check that could disprove it"
```

Replace the placeholder strings and file path with your own work. The path must identify an evidence file in your workspace; do not copy the command unchanged and call it an attempt. The CLI and portal keep separate attempt records. Saving one does not automatically import it into the other.

After saving a substantive attempt, request one hint at a time:

```sh
python3 -m lab.incidents hint --workspace work/incidents/INC-01 --level 1
```

Stop reading when you have a useful next action. Record which hint levels you used. The final debrief is a separate deliberate action:

```sh
python3 -m lab.incidents debrief --workspace work/incidents/INC-01
```

Portal hints and debriefs stay out of the normal brief until you save an attempt and request them. The CLI also requires a saved attempt with workspace evidence. The source repository contains guidance for reproducibility, so these are learning safeguards, not access controls. Do not inspect guidance fields or the test implementation before trying. A tutor should withhold guidance even if it can see those files.

## Investigate within a budget

Each brief sets an initial time and check budget. A check means one deliberate evidence-gathering action, such as inspecting a report, running a targeted command, or comparing two identified records. Record its cost and outcome. These investigation budgets are learner rules; the harness does not observe every action you take outside it.

When the budget expires, save a handoff with what you know, what remains uncertain, and the single next useful action. Ask for a hint or a narrowly specified piece of missing information. Unlimited retries, broad rewrites, and invented certainty are not recovery strategies.

Implement a narrow decision or recovery change only after preserving the initial evidence. Check the result:

```sh
python3 -m lab.incidents check --workspace work/incidents/INC-01
```

Keep the original failure and later results. A passing executable check is necessary for the implemented contract, but your report must also satisfy the [incident assessment rubric](ASSESSMENT.md). The fixture deliberately cannot grade the quality of a stakeholder conversation or prove that you understood every outcome.

## Transfer without memorizing the answer

After completing and reviewing the first workspace, create a new one with changed conditions:

```sh
python3 -m lab.incidents init INC-01 --variant transfer --workspace work/incidents/INC-01-transfer
```

Use the matching ID for other incidents. Predict what should remain invariant and what may change before opening the new evidence. Do not copy the previous conclusion. Capture one new discriminating check, then test and explain the result. A transfer variant is a deterministic changed case, not an independently sampled production evaluation.

## Tutor instructions

Ask for one artifact or one next check at a time. Before revealing a hint, require the learner's explanation, observation, and next check. Respond to the evidence they supplied; do not name the hidden fault just because you know it. Give the smallest useful hint, wait for a revised attempt, then increase help only if requested. Never paste the full implementation.

Offer a debrief only after an attempt and an explicit request. During assessment, ask the learner to predict a changed condition before running it. Distinguish a proposed test, an observed test result, a simulation, and actual external integration. Record uncertainty and help level honestly.

[Study plan](../../docs/STUDY-PLAN.md) · [Practice map](../../docs/PRACTICE-MAP.md) · [Capstone defense](../../capstones/incident-defense.md)
