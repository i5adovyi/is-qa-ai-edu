# Learning experience implementation record

Implemented 20 October 2026 against the [learning experience review](LEARNING-EXPERIENCE-REVIEW.md). The course retains 24 lessons and eight stages. The additions make the first attempt easier to start and give later technical work a runnable, inspectable path.

## What changed

| Review workstream | Delivered practice | How it is checked |
| --- | --- | --- |
| Progressive hints and route corrections | Eight component hint pages use independently closed, keyboard-accessible disclosures. Lesson 08 and week 4 submissions now match the real MCP and skill activities. | Renderer unit tests and browser checks on every hint page; content validation |
| Preparation and scaffolding | Three entry checks, an unrelated diagram example, a terminal worksheet, five checkpoints for the first diagram, and four starter fixture packs with separate keys | Fresh-copy terminal commands include intended failures and successful regeneration; exercise metadata and links checked |
| Feedback and mastery | 72 exercise workspaces, 72 applied checks, saved attempts/revisions/feedback, artifact references, evidence labels, spoiler-free tutor packets, calibration specimens, and export/import | Unit and browser checks cover migration, resume, history, conflicting imports, tutor packet exclusions, and keyboard interaction |
| Actual model-directed tools | Lab 12 has a bounded planner loop, incomplete student starter, fault fixtures, provider transports, real MCP lookup, and an optional assistant-host connection | 25 planner tests; actual model → MCP observation → subsequent decision; separate host MCP run |
| Coding and workers | Lab 13 creates a disposable repository, preserves the first failure, supports a scoped repair, review, commit, revert/restore, and fresh-session handoff. Separate worker processes compare one worker with two. | Eight scripted case comparisons, coordination faults, actual coding-agent repair/fresh-session verification, and one actual three-request model-worker smoke test |
| Measured retrieval | Lab 14 supplies a versioned synthetic corpus and lexical/hybrid/filter comparison, with retrieval and claim-label checks reported separately | Deterministic case-level results and regressions; the hybrid uses explicit term expansion, not an embedding model |
| Review and operations | Lab 15 adds a local review queue, exact-revision approval, correction/rejection, restart/replay, release-version checks, rollback, and CI artifact preservation | Stale approval, tampering, duplicate effect, fresh-process replay, mismatched release, and rollback tests |
| Retention and transfer | Eight new-domain transfer tasks, mistake-linked recall history, eight original slide/text walkthroughs with pause points and transcripts, differentiated time estimates and explicit routes | Browser checks for walkthroughs/recall and saved responses; content and route validation |

The portal records learning evidence locally. “Tutor reviewed” and “execution evidence” identify the basis entered by the learner; they do not claim that the portal independently authenticated a tutor or executed a lab.

## What the additional study-plan review found

The bridge from classroom work to a future project needs three explicit habits:

1. **Diagnose the environment and API boundary.** Identify the interpreter, dependency environment, source revision, working directory, and difference between an HTTP observation and a valid result.
2. **Evaluate a model or configuration replacement.** Hold cases and criteria fixed, inspect regressions, record all attempts and usage, and restore the previous configuration.
3. **Maintain evaluation data as reality changes.** Record provenance and label uncertainty, separate related case families, version policy and data together, and protect an untouched final set.

The [future-project readiness guide](FUTURE-PROJECT-READINESS.md) adds these as three short missions at the point of use. The [study plan](STUDY-PLAN.md) shows their placement and budgets extra integration time separately. They are not additional requirements before the first diagram.

## Evidence and limits

See the [verification record](VERIFICATION.md) for exact test results and the [planner evidence](../lab/planner_lab/EVIDENCE.md) for actual model/MCP measurements and earlier failures.

- A real learner trial is still needed to validate pacing and whether the first checkpoint is easy enough. The portal now records observed time and requested hints; authored estimates are provisional.
- Retention and transfer require the learner's delayed attempts. Software tests cannot establish that learning occurred.
- Live Codex model and MCP paths were exercised. The separate Responses API transport has offline contract/failure tests; live API compatibility remains pending an API credential.
- The worker smoke test is one synthetic case with three model requests. It does not establish a general quality or speed advantage for teams.
- The review queue is a local single-writer exercise, not a multi-user service. Its release rehearsal changes version bindings rather than deploying a real knowledge service.
- The CI workflow is included. Local equivalent checks and hosted workflow status are separate evidence.
- The walkthroughs are original interactive slides and text transcripts. They are not newly produced narrated videos.

Full solutions remain available by deliberate choice. Tutor packets exclude hints, hidden solutions, instructor implementations, and previous private feedback by default.
