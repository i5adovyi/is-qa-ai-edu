# Project closeout and retrospective

> Historical closeout of the initial build. The project was reopened after learner feedback; the [21 October learning-design correction](LEARNING-DESIGN-2026-10-21.md) and [current start guide](START-HERE.md) supersede its practice-first entry route.

Recorded 20 October 2026. This is the historical handoff for the academy's initial
build. Annotated Git tag `academy-2026-10-20` identifies the delivered tree and
stores the final GitHub Actions and Sites version/deployment receipts. Current
instructions remain in [README](../README.md), [AGENTS](../AGENTS.md), and
[maintenance](MAINTENANCE.md).

## Closeout decision

The initial build is ready to close and move into learning and ordinary
maintenance. The deliverable is a usable personal AI engineering academy with
editable source, executable practice, a private portal, and an independent local
application. Closing the build does not mark learner work complete.

No known release-blocking defect remains in the tested scope. The limitations
below are explicit boundaries and optional follow-up work. There is no need to
keep expanding the curriculum before beginning to learn.

## Delivered scope

| Area | Result |
| --- | --- |
| Course | Eight stages, 24 lessons, 72 exercise workspaces, 72 applied checks, preparation, recall and transfer practice |
| Engineering practice | Fifteen lab guides, reference and student harnesses, real MCP, skill installation, model/tool loops, coding and workers, retrieval and review/rollback |
| Realistic failures | Six incident investigations and one capstone incident, primary/transfer workspaces, boundary cases, recorded attempts and deliberate guidance reveal |
| Projects and library | Three capstone briefs, original articles/manuals/templates, and 43 curated resource entries |
| Learning interface | One-step practice, drafts, attempt/feedback history, progressive hints, tutor packets, notes, bookmarks, quizzes and progress import/export |
| Persistence | Local SQLite, revision conflicts, recovery and consistent backup; hosted browser storage with explicit JSON transfer |
| Portability | Private GitHub source, local launcher, source and portable ZIPs, PDF fieldbook, and a separate-copy workflow for a new account's Site |
| Session continuity | README, shared AGENTS instructions, CLAUDE entry point, tutor handoff and maintenance/runbooks |

Signal Desk is a fictional support/QA case study with synthetic fixtures.
Deterministic simulations, actual protocol execution and actual model calls
are labeled separately. The portal does not execute or automatically grade
terminal work. Student starter failures remain intentional assignments.

## Development history

This sequence summarizes delivered work, not the learner's personal history.

1. Established the course, portal, reference harness, library and fieldbook;
   added private source storage and downloadable copies.
2. Audited lessons and a fresh-clone student route, repaired unclear steps,
   and mapped exercises to prerequisites and evidence. See the
   [student audit](STUDENT-AUDIT.md) and [exercise audit](EXERCISE-AUDIT.md).
3. Added real MCP, installed-skill practice and a composed student harness;
   extended model-directed execution, coding/workers, retrieval and operations.
   See the [integration guide](INTEGRATION-LABS.md) and
   [fresh-copy execution record](RELEASE-V5-EXECUTION.md).
4. Improved onboarding, graduated hints, attempts, feedback, transfer and recall.
   The [implementation record](LEARNING-EXPERIENCE-IMPLEMENTATION.md) maps this
   expansion to its checks.
5. Added incidents and repaired study-plan pacing and prerequisites. Integration,
   incident and capstone hours are separate; the full route has no guaranteed
   twelve-week finish.
6. Added hosted/local launch modes, account migration, SQLite, recovery and
   separate new-Site preparation. Source, personal data, account access and
   publication identity now have explicit boundaries.
7. Added new-session orientation in commit `d4d66bd`, then completed this closeout.

Earlier commits often use the Sites helper's generic `Update Site source`
message. Use dated review/verification documents for narrative context and Git
diffs as the authoritative record of file changes.

## Retrospective

| Observed problem | Contributing assumption | Resolution and lesson |
| --- | --- | --- |
| Beginners could still be unsure how to start | Content quantity did not establish the first action or prerequisites | Added preparation on an unrelated example, explicit evidence criteria and one-step hints. Test the first ten minutes as a beginner. |
| Working reference code could be mistaken for independent agent experience | Simulations and student/model execution looked similar | Added student hooks, real MCP/skill practice and distinct evidence labels. Require observable behavior for each claimed capability. |
| Happy-path exercises omitted operational ambiguity | Reliable fixtures hid retries, conflicting evidence and coordination faults | Added incident, transfer and boundary workloads. Test failure and recovery together. |
| Browser checks exposed draft/import and save-button defects | Blur events and state transitions interacted across imports and rerenders | Preserved conflicting histories and repaired observed transitions with regression checks. Test real interactions as well as state functions. |
| Account changes risked loss of access or progress | Hosting, Git permission, browser state and local files were treated as one thing | Separated boundaries; added SQLite/export/backup and clean Site copies. Test transfer from a fresh copy. |
| Old checks or chats could become unsupported current claims | Historical evidence was easy to reuse without checking the revision | Added current-session orientation and exact release checks. Keep history distinct from current verification. |

This records development findings, not a production outage or customer-data
incident. During closeout, the bundled Playwright version initially expected an
unavailable browser cache. Selecting an installed executable using the documented
`ACADEMY_BROWSER_PATH` resolved that test-environment issue.
The first concurrent browser batch timed out; the same interaction checks passed
sequentially with server logs redirected and no application changes. The exact
cause was not isolated, so this is recorded as test-run instability rather than
a claimed application repair. Run the documented browser scripts sequentially.

## Closeout verification

- Git integrity passed. All distributable source was tracked, with no required
  source left only in ignored directories. Authenticated GitHub inspection
  confirmed private visibility and matching `main` at the start of closeout.
- Python 3.9 core: **226 discovered, 215 passed, 11 optional MCP skips**.
- Python 3.12 with pinned MCP dependency: **226 passed**, no skips.
- Portal unit checks: **42 passed**.
- Completed harness: **28/28 cases, 11/11 failure scenarios, 3/3 integration
  probes**, with all eight component hooks exercised.
- Course metadata and internal file/section links passed validation.
- Isolated SQLite browser checks passed drafts/history/notes/completion,
  a fresh browser context, concurrent revisions and explicit merge, failed-write
  recovery, a server restart on another port, static fallback and mobile layout.

- Portal, learning-workflow, incident and run-anywhere browser suites passed,
  including spoiler gates, keyboard hints, imports and mobile layouts.
- All **251 distributed source files**, **143 portal documents**, and **67
  teaching assets** matched their source bytes. The portable ZIP's embedded
  source ZIP matched the standalone archive. Both PDF copies were identical;
  the fieldbook itself was not regenerated during closeout.
- Fresh source and portable extractions each started from a different working
  directory and served nine checked HTTP paths, including their downloads and
  local database endpoint. A newly prepared account copy retained all session
  guides and this closeout, reset the old Site identity/URL, and contained no
  learner database. Those temporary servers were stopped.

- Exhaustive browser audit: **143 documents and Markdown downloads, 462 internal
  link occurrences, 174 distinct internal links, 96 quiz choices, eight stages,
  70 downloadable assets and 143 mobile document layouts**; zero page errors.

The release tag records the exact final commit, successful GitHub CI run, and
matching published Site version. GitHub and Sites are separate destinations;
their successful receipts are checked independently. Historical PDF/live-host
observations remain in [VERIFICATION](VERIFICATION.md) and are not counted as
reruns here. No course or application behavior changed during closeout.

## Storage and recovery handoff

| Material | Location | Resume or recover |
| --- | --- | --- |
| Editable project and history | [Private GitHub repository](https://github.com/i5adovyi/is-qa-ai-edu) and the local clone | Clone/reopen; use the closeout tag for this release |
| Website and downloads | Tracked `dist/`, rebuilt from source; existing private Site | Run `python3 academy.py local` or open the [hosted portal](https://signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site/) |
| Course PDF | `output/pdf/ai-engineering-fieldbook.pdf`, copied to `dist/fieldbook.pdf` | Read the fieldbook; operational closeout records live in Markdown/HTML |
| Local learning records | Ignored `.academy-data/progress.sqlite3` or selected `--data-dir` | Use the same directory and the [backup/restore guide](LOCAL-DATA.md) |
| Hosted learning records | Browser storage for the Site origin/profile | Export JSON before clearing storage, moving browsers or changing Site origin |
| Lab outputs and QA artifacts | Ignored `work/`, `.lab-runs/`, `tmp/` | Back up useful private evidence separately; these are not release source |

This checkout had no default learner database at closeout. That does not prove
there is no hosted progress or no database in a separately selected directory.
No personal browser progress was inspected, exported, modified or committed.
GitHub and course downloads are not personal-progress backups. Caches and
disposable test artifacts are intentionally excluded from the release.

The existing Site retains its private custom audience: the original owner and
the previously invited external viewer. It is not a public Site or an ownership
transfer. A separate Site in the next account still needs that account's
authenticated session; see [NEW-ACCOUNT](NEW-ACCOUNT.md).

## Remaining boundaries

- **Learner validation:** real attempts, delayed retention, transfer and measured
  study time still need learner evidence. Build completion is not course
  completion, certification or validation of a commercial price.
- **Optional live API:** the Responses API adapter has offline contract tests;
  live execution still needs an API credential. Historical model-host/MCP
  observations do not establish every provider path.
- **Platforms and accounts:** local macOS and Linux CI were exercised. Windows
  execution and Site creation while signed in to the destination account were
  not performed; separate-copy mechanics were tested.
- **External material:** availability and vendor interfaces change. The
  [link audit](LINK-AUDIT.md) records earlier observations; closeout does not
  claim every external page, course or video was revalidated.
- **Deployment model:** hosted progress and SQLite do not synchronize
  automatically. The loopback server is personal, not a public multi-user
  service. Answer gates support learning, not secure examinations.
- **Accessibility and sales:** no tagged accessible-PDF conformance is claimed.
  A commercial offering still needs a learner pilot, rights review and defined
  support/updates; see [reuse guidance](REUSE.md).

Reopen implementation for a reproducible bug, changed dependency/link, or a gap
demonstrated by an actual attempt. Otherwise, resume through
[START HERE](START-HERE.md), preserve private progress, and follow tutor rules.
The build chat can be closed without deleting or archiving the GitHub repository.
