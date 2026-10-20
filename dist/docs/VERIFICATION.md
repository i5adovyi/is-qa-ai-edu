# Verification record for the October 2026 academy release

Checked 20 October 2026. The run-anywhere revision below is the latest verification. Earlier incident and learning-release observations are retained afterward for provenance. Earlier findings remain in the [student audit](STUDENT-AUDIT.md) and [learning experience review](LEARNING-EXPERIENCE-REVIEW.md); the [implementation record](LEARNING-EXPERIENCE-IMPLEMENTATION.md) maps the preceding eight review workstreams.

## Run-anywhere revision: executed checks

The [shared launcher and hosting guide](RUN-ANYWHERE.md) provide explicit local and OpenAI-hosted modes. The source and portable archives contain the same launcher and canonical URL configuration. The older server commands remain supported, including the commands printed in the existing fieldbook.

- Python 3.9.6 full suite: **208 discovered, 197 passed, 11 optional MCP skips**. Seven launcher tests cover actual HTTP startup, alternate working directories, legacy commands, port/config/build errors, serving only course assets, and repeated extract/run/download of a portable copy.
- Portal unit suite: **27 passed**, including mode detection and unchanged progress when opening Run anywhere.
- The new browser check passed navigation, hosted/local/GitHub destinations, exact portable download bytes, setup and progress links, and desktop/mobile layout. Representative screenshots were visually reviewed.
- Both final source and portable ZIPs were separately extracted into temporary directories. Their hosted command printed the configured URL without starting a server; their local command served the real course and five essential/download assets. Source rebuilt from its own files; portable ran without a build dependency. Both stopped cleanly on interruption.
- Content and local-link checks passed. The source ZIP retains only the specific hosting manifest needed for existing-Site publication, not credentials. The portable download is regenerated from course assets when an extracted copy lacks a ZIP of itself.

No OpenAI account or package installation is required for local reading and progress. Hosted access and GitHub permission remain separate. Progress does not synchronize automatically; use export/import. Hosted CI execution is checked separately after pushing the release.

## Incident revision: executed checks

The [incident route](../content/incidents/README.md) adds six investigations and one capstone incident, each with a primary and transfer workspace, boundary workloads, an editable starter, and separate guidance. These are local deterministic simulations; they do not exercise real customer services or deliberately cause provider failures.

- Full Python 3.9.6 core suite: **201 discovered, 190 passed, 11 optional MCP skips**.
- Full Python 3.12.14 suite with pinned `mcp==1.30.0`: **201 passed**, no skips.
- New incident regression coverage: **36 tests**, included in both complete suites. Starters fail their acceptance checks as intended; reference repairs pass primary, transfer and boundary cases. Tests also cover preserved evidence, path containment, malformed outputs, negative acceptance cases, guidance gates, and immutable run/check history.
- Portal unit suite: **26 passed**. A fresh-browser import defect was reproduced and repaired: an untouched local draft now adopts imported work; real conflicting drafts remain preserved.
- All three interaction suites passed: original portal, learning workflow, and incidents. The incident suite covers all seven routes, empty/draft/feedback rejection, explicit progressive hints and debrief, reload/navigation/import closure, tutor packet exclusions, attempt history, escaping and mobile layout.
- Exhaustive browser audit: **137 documents and Markdown downloads, 397 internal link occurrences, 167 distinct internal links, all 96 quiz choices, eight stages, 70 downloadable assets, all 137 documents at mobile width, zero page errors**.
- Fresh source-package execution: **234 distributed files, 14 isolated primary/transfer workspaces, 113 commands**. Initial execution, intended starter-check failures, pre-attempt guidance blocking, explicit post-attempt guidance, and rebuilding both downloadable packages all passed. Distributed source hashes remained unchanged; generated learner work stayed out of the rebuilt source archive.
- Fieldbook: **278 pages**, with no empty pages or text outside the inspected safety bounds. Representative study-plan and incident pages were rendered and visually reviewed. Incident debriefs are absent from the student book; the portal and CLI provide deliberate access after an attempt.

The revised study plan budgets the incident route separately, splits Lab 13's coding and worker prerequisites, and retains the required decision helper for the composed harness regardless of the final capstone choice. A full extended route is not promised within twelve weeks.

Run the complete suites and content validator using the commands below. Browser checks additionally include `node scripts/test_learning_portal.cjs` and `node scripts/test_incident_portal.cjs`. The GitHub workflow discovers the new Python tests and runs the portal unit tests; hosted CI status is verified separately after pushing.

The attempt gates are learning safeguards, not examination security. Editable source contains guidance, while the ordinary incident interface and tutor packets conceal it. CLI and portal attempts are separate records. No actual provider/model reliability claim or learner-pilot result is inferred from these checks.

## Earlier learning release: fresh-copy execution

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
