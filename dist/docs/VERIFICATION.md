# Verification record for the October 2026 learning release

Checked 20 October 2026. This record describes the expanded learning experience and its synthetic fixtures. Earlier findings remain in the [student audit](STUDENT-AUDIT.md) and [learning experience review](LEARNING-EXPERIENCE-REVIEW.md); the [implementation record](LEARNING-EXPERIENCE-IMPLEMENTATION.md) maps all eight review workstreams to delivered practice.

## Fresh-copy execution

The [fresh-source execution record](RELEASE-V5-EXECUTION.md) lists fourteen commands run from an isolated distribution copy with inherited Python import paths removed. Imports resolved to that copy, and its source manifest remained unchanged.

- Python 3.9.6 core suite: **165 discovered, 154 passed, 11 optional MCP skips**.
- Python 3.12.14 with pinned `mcp==1.30.0`: **all 165 passed**, no skips.
- Dependency-free portal unit suite: **21 passed**.
- Completed composition: **28/28 cases, 11/11 failure scenarios, three integration probes, all eight component hooks**.
- Actual MCP SDK/server gate: **13/13 checks**.
- Scripted planner and scripted planner with actual MCP: two decisions and one lookup completed.
- Untouched planner student starter: expected exit 1, `student_incomplete`, no tool use. This failure is an assignment, not a broken release.
- Retrieval: three variants on twelve fixed synthetic cases. Scripted workers: all eight comparisons and coordination fault checks. Local review queue: all four release/recovery rehearsal gates.

The beginner terminal worksheet was separately executed in a fresh temporary directory. Ten command checks covered initialization, the intended first assertion, successful correction and regeneration, stale output, malformed JSON, invalid types, and preservation of existing input.

## Actual model and coding-host evidence

[Planner execution evidence](../lab/planner_lab/EVIDENCE.md) records an actual model proposal, validated MCP execution, returned observation, and subsequent model decision. A separate assistant-host run discovered and used the same MCP server, including an argument error and repair. These are distinct from deterministic simulation.

An actual Codex coding session read the disposable repository guidance, reproduced the seeded failure, changed only the implementation, and passed all five unchanged tests. The reviewed repair was committed in that disposable repository. Reverting it on a rehearsal branch restored the original failure; switching back restored five passing tests. A second fresh, read-only coding session verified the handoff commit and reran the tests. The canonical learner defect remains unchanged.

A one-case live worker smoke test made three model requests: single-worker baseline, evidence worker, and completeness worker. The outputs passed the same integration contract as scripted workers. Requested model was `gpt-6-astra`; the CLI did not expose an immutable server revision. Available usage and timings were retained locally. This is an integration observation, not evidence that two agents are generally better or faster.

The separate Responses API adapter passed offline transport/contract/failure tests. **Live Responses API execution remains pending an API credential.** A working Codex login does not prove access to that API. These tests do not deliberately cause real service rate limits or refusals.

## Course and portal

The content validator checks 24 lessons, eight stages, 72 exercise workspaces, 72 applied checks, fifteen numbered lab guides, 43 resource entries, and resolving local file/section links. New practice includes four fixture packs with separate keys, eight transfer tasks, eight original slide/text walkthroughs, calibration examples, and three future-project readiness missions.

The browser interaction suites exercise preparation/routes, independently closed keyboard hints on all eight component pages, attempts and revisions, feedback, one-step resume, tutor packet exclusions, downloads, recall scheduling, walkthrough positions, conflicting progress imports, legacy progress migration, and mobile layout. The exhaustive audit reads every distributed document, follows every internal link, tests all 96 quiz choices and eight stage pages, verifies downloadable bytes, and checks every document at a 390-pixel viewport.

The audit found a review-document link to a repository implementation file that was not a downloadable asset. The document now names that file without creating a broken portal link. Browser testing also found and fixed a reentrant textarea-blur bug that could replace a draft during rerender.

The [existing external-link audit](LINK-AUDIT.md) records the earlier checks of 65 learning/setup destinations. Current provider and new setup references were checked against official documentation during this revision. This release does not claim to have watched every video or completed external courses. Access and interfaces can change.

Progress is browser-local and exportable. It is not an authenticated transcript, certification, or automatic verification of learner execution. The new account-migration route makes this storage boundary explicit.

## Fieldbook and portability

The fieldbook was regenerated from the revised sources. Lesson answer guidance and MCP extension solutions are placed in a deliberate final appendix. PDF inspection checks all pages for empty content and text outside safety bounds, followed by visual inspection of representative new pages. It is a reading PDF, not a tagged accessible-PDF conformance claim; editable Markdown and the HTML portal are included.

The source ZIP excludes learner records, runtime output, Git metadata, credentials, and environment files. The ready-built portable ZIP includes the portal, source ZIP, PDF, a local loopback-only server, account-migration instructions, and a tutor handoff. It does not contain browser progress or chat history; export those learning records separately before changing accounts.

## Reproduce locally

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 scripts/check_content.py
python3 -m lab.composed evaluate --components completed --split all
python3 -m lab.practicum.workers --out work/verify-workers
python3 -m lab.practicum.retrieval --out work/verify-retrieval
python3 -m lab.practicum.review_queue rehearse --out work/verify-review
python3 scripts/build_portal.py
python3 scripts/serve_portal.py
```

Use fresh output directories. With the pinned Lab 09 environment, rerun the complete Python suite and actual MCP gate. Optional browser scripts are `scripts/test_portal.cjs`, `scripts/test_learning_portal.cjs`, and `scripts/audit_portal.cjs`; they need Playwright and a matching browser, or `ACADEMY_BROWSER_PATH`. Set `ACADEMY_TEST_URL` for a nondefault server. PDF authoring needs ReportLab, not the learner core.

The GitHub Actions workflow runs the core checks on Python 3.9/3.12, a separate pinned MCP job, and preserves scripted evaluation artifacts. Hosted workflow status must be checked separately from local equivalent results. No live credentials or publication run in this CI workflow.

Pacing, delayed retention, and independent transfer still need real learner attempts. Estimated study time has not been validated by a learner trial.
