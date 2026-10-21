# Maintain and extend the academy

The editable source is this repository. The portal is generated into `dist/`; do not edit generated content there. The build also refreshes the downloadable source archive, so a newly extracted project can rebuild all portal downloads. Lessons and reference material are ordinary Markdown so the course remains usable without its interface.

## Structure

- `content/tracks/catalog-*.json`: independent subject tracks, levels, topic prerequisites, material links, and selected sources. The current release has 14 tracks and 84 topics. Preserve stable subject/topic IDs when extending it.
- `docs/SUBJECT-CATALOG.md`: generated offline index of every subject, topic, and curated path. The portal build refreshes it through scripts/build_subject_catalog.py; edit catalogs rather than this index.
- `content/tracks/paths.json`: curated cross-subject sequences. `#start` introduces the zero path; `#path` lists paths; `#learn=zero` shows one sequence; `#tracks`, `#track=mcp`, and `#topic=mcp-basics` open the subject catalog, subject, and topic.
- `content/tracks/<subject>/`: 60 new topic articles. Every topic uses the same eight-section teaching contract as the retained beginner guides. Catalog entries with `lesson` reuse the original how-to file and retain the full original lesson, exercises, and notes.
- `portal/tracks.js`: subject navigation and teaching views. Loaded after data.js and before app.js; include it in builds and launcher checks.

- `content/how-to/`: all 24 beginner guides and their map fragments. Build merges the maps into A.course. Every canonical lesson begins with its guide and retains the complete original lesson below it.
- `content/sdet-path.json`, `content/guide/`: eight retained supporting primers, scoped readings, and related links. Do not replace or hide the full course with this shorter route.
- `content/curriculum.json`: stage and lesson metadata.
- `content/learning.json`: exercise/step contracts, progressive hints, applied checks, routes, walkthroughs, and transfer prompts. Tutor packets whitelist prompt fields and exclude hints and solutions.
- `content/onboarding/`, `content/practice/`, `content/assessment/`, `content/walkthroughs/`: preparation, starter fixtures, calibration, transfer, and original walkthroughs.
- `content/lessons/`: original lesson text.
- `content/resources.json`: curated external library.
- `content/articles/`, `content/library/`: supporting reading.
- `content/labs/`, `lab/`, `tests/`: practical assignments, the reference harness, and manual model-response bridge.
- `lab/mcp_lab/`: real SDK client/server exercise with separately installed dependencies.
- `content/skill-practice/`, `lab/skill_lab/`: installable teaching skill, synthetic inputs, and disposable-workspace tooling.
- `lab/composed.py`: integrated student-component runner; preserve the ordinary reference CLI.
- `lab/planner_lab/`: bounded planner, live-model adapters, real MCP use, host integration, and separately labeled execution evidence.
- `lab/practicum/`: isolated coding mission, process/model workers, retrieval comparison, and local review queue.
- `content/incidents/`, `content/incidents.json`, `lab/incidents/`: six incident briefs and one capstone incident, separately stored guidance, disposable simulations, and behavioral checks. Never put an incident debrief into a student brief.
- `content/research/`: synthetic source corpus and scored research examples.
- `content/dev-sandbox/`: intentionally broken development exercise; its one baseline test failure is expected and isolated from reference checks.
- `docs/`, `templates/`, `capstones/`: learner manuals and reusable project artifacts.
- `portal/`: interface source.
- `academy.py`, `academy.json`: shared local/hosted launcher and canonical hosted/GitHub URLs. Both source and portable packages include them; legacy server commands delegate to this launcher.
- `academy_local.py`, `.academy-data/`: local SQLite persistence and the ignored default learner data directory. Never distribute its database, sidecars, or backups.
- `README.md`, `AGENTS.md`, `CLAUDE.md`: project overview, shared tutor/maintainer instructions, and Claude entry point. Keep them in editable downloads and new-account copies.
- `scripts/prepare_new_site.py`: creates a separate publication copy with a fresh hosting manifest and no hosted URL; actual registration happens through Sites in the target account.
- `scripts/`: build, serving, packaging, and content validation.
- `work/`: your private experiment outputs, intentionally excluded from distribution.

## Release checks

These are maintainer checks. Install Node.js 22 or newer for the JavaScript tests; it is not required for the student Python route. Browser checks additionally need Playwright and a compatible browser. The PDF rebuild needs ReportLab; the generated PDF is included for readers.

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 scripts/check_content.py
python3 scripts/build_portal.py
python3 scripts/preview_portal.py --port 8792
```

Open overview, a lesson, a lab, the library, and a manual. Check keyboard navigation, narrow screens, quiz feedback, saved notes, progress export, and import. Use an isolated temporary `--data-dir` for maintainer checks; do not overwrite a learner's profile. Verify local database save/reload, a server restart, and conflict/error handling. Hosted browser storage is local to its origin; local databases and hosted portals do not share progress. Export/import JSON to transfer records, and use the database backup command for local recovery.

The static test server above uses an enlarged connection backlog for concurrent browser checks and deliberately uses browser storage, matching hosted behavior; its visible static-preview notice is expected. With that server running and Playwright available, set `ACADEMY_TEST_URL=http://127.0.0.1:8792`, then run `node scripts/test_portal.cjs` for interactions and `node scripts/audit_portal.cjs` for every document, internal link, quiz answer, downloadable asset, and mobile document layout. `ACADEMY_BROWSER_PATH` selects an installed browser executable. When testing another checkout, set `ACADEMY_TEST_URL` to its server and `ACADEMY_DIST_DIR` to its matching `dist/`; the audit compares download hashes with that exact build.

Run `node scripts/test_subject_tracks.cjs` and `node scripts/test_sidebar.cjs` after navigation changes. The sidebar exposes every subject and its active topic; its separate Original lesson sequence shelf indexes all eight original stages and 24 lessons, searches beginner titles and technical terms, and highlights the lesson for lesson/document/exercise deep links. Test every section link, short desktop scrolling, and mobile drawer focus, Escape, same-route navigation, and viewport resizing. Sidebar search/expansion is temporary interface state; it must not change learning records. On mobile, opening the drawer makes the article inert until closing, and progress import must close the drawer before returning to the refreshed content.

Run `node scripts/test_beginner_journey.cjs` for the first-time reading route. It follows the inline next-reading link, all 24 end-of-guide continuations, eight stage entrances, and detours through setup, materials, and primers on desktop/mobile without writing progress. Normal links to beginner guides must open `#lesson=NN`; original-lesson links target its retained original section. Preserve explicit standalone `#doc=` routes and Markdown downloads, with a route back to the full lesson. Search clears on navigation. The last visited lesson used for a return link is session-only interface context, not a saved position or completion claim.

Run `node scripts/test_local_progress.cjs` separately for actual SQLite browser behavior. It starts its own launcher with a temporary data directory, so the check does not write into a learner's default database. Python discovery includes real HTTP/database tests, backup restoration, new-account preparation, and source-distribution privacy checks.

Also run `node scripts/test_learning_portal.cjs` for the exercise workspace, spoiler protection, v1 progress migration, feedback history, import conflicts, recall, and narrow-screen behavior. The v2 progress schema must preserve original attempts; do not silently overwrite a learner's history on import.

Run `node scripts/test_sdet_path.cjs` for the guided reading route: first-session navigation, topic sequencing, resource scope and access notes, explicit reading-position saves, optional notes, retained practice links, and narrow-screen behavior. Opening or reading a topic must not create exercise attempts, mark a lesson complete, or pass a gate. Confirm that the saved position survives the supported reload/export/import flow without replacing existing practice records. Inspect the actual assertions before claiming coverage of all those behaviors; add the relevant check when changing a behavior.

Run `node scripts/test_incident_portal.cjs` for incident attempt gates, progressive hints, deliberate debrief reveal, reload and import behavior. Incident guidance must stay out of the DOM and tutor packet before explicit disclosure. The source archive contains editable guidance; the static portal is not an examination security system. The PDF includes incident briefs but omits their guidance because it cannot enforce an attempt gate.

The GitHub Actions workflow runs core and optional MCP checks with no model credentials. It pins Ubuntu 24.04 because the moving ubuntu-latest label can select a runner without a Python 3.9 distribution. Check the setup-python version manifest before changing the runner or supported Python matrix. Live Codex/provider calls are deliberately explicit local checks. Record CI execution separately from a locally passing workflow command.

The [Run anywhere guide](RUN-ANYWHERE.md) separates local startup, private GitHub source updates, and OpenAI Sites publication. `python3 academy.py local` rebuilds source copies and serves only `dist/` on loopback; `python3 academy.py hosted` opens the existing hosted copy. A GitHub push does not by itself deploy Sites.

The [new-account guide](NEW-ACCOUNT.md) explains fresh publication identities. `scripts/prepare_new_site.py` uses the same source allowlist as source ZIP packaging, excludes the original `.openai` identity, then writes only a new static manifest and sets `hostedUrl` to `null`. Keep nullable URL handling in the launcher and portal: an unpublished copy must not send a learner to the previous account's Site. New-account exports must refuse existing destinations and leave the original source/data unchanged. `tests/test_new_site.py` checks these boundaries and failure paths.

The [local data guide](LOCAL-DATA.md) documents persistence and backup/restore. Database updates use revisions to reject stale overwrites. Do not replace a corrupt database automatically, silently downgrade failed saves to browser-only success, or put local persistence endpoints into the static hosted bundle as if it had a server.

Launcher checks are included in Python discovery (`tests/test_launcher.py`). They cover source/portable startup from a different directory, legacy commands, occupied/invalid ports, missing files, build failures, serving only the built directory, and an extract/run/download round trip. An extracted portable copy regenerates its portable ZIP download in memory from the course assets; it does not package arbitrary files from the learner's directory. Run `node scripts/test_run_anywhere.cjs` for the mode selector, links, portable download, progress navigation and mobile layout.

## Maintain the guided SDET path

The main architecture is subject tracks and learning paths. `#path` lists curated paths, `#tracks` lists subjects, and `#legacy` preserves the original 24-lesson map. Original lesson routes retain IDs such as `#lesson=01` and their sequence stays in `content/curriculum.json`. Beginner teaching lives in `content/how-to/NN.md`, with prerequisites, keywords, material links, and scoped source metadata in `content/how-to/map-*.json`. Short primer bookmarks remain `#guide=01` and use `content/sdet-path.json`. Keep these distinct: progress.reading is a primer ID; progress.lessonReading is a lesson ID; progress.topicReading is a subject topic ID; progress.topicPath preserves a valid selected path; progress.readingKind selects the most recently explicitly saved type (primer, lesson, or topic) without erasing the other bookmarks. Never reinterpret an old saved primer ID as a lesson bookmark. A topic should explain the concept in plain language, show why it matters to an SDET, and use a concrete testing example before directing the reader elsewhere. Avoid unexplained jargon, required artifacts, and links that send a beginner into a whole catalog.

Each topic has one primary resource. Keep its title, provider, URL, exact reading or viewing scope, stopping point, prerequisites, access requirements, and verification date accurate. Distinguish public reading from optional execution that needs an account, paid credits, an IDE, Python, or a configured agent. Alternatives are substitutes or explicitly deeper reading; they must not become another completion checklist. Select across providers by instructional fit rather than filling vendor quotas. When a linked course contains its own assignments, say whether to skip them for this reading route.

Retain useful material in the original lessons, labs, articles, templates, and library, and link to it at the point it helps. Do not delete practice IDs or rewrite learner history to simplify navigation. Keep the original attempt/hint/debrief contract within chosen practice, but do not apply it to basic concept explanations or block the next reading topic. The explicit **Save my place** action records where to resume; neither a page visit nor that bookmark demonstrates understanding or mastery. Notes remain optional.

Keep [the start guide](START-HERE.md), [study plan](STUDY-PLAN.md), [tutor handoff](CONTINUE-LEARNING.md), [learning tutor prompt](../templates/tutor-prompt.md), and assistant entry points consistent with this learning-first route. The [practice tutor prompt](../templates/practice-tutor-prompt.md) retains coaching for selected assignments. Historical closeout and audit records describe their earlier releases; do not silently rewrite them as if they validated the revised learning experience.

## Add or maintain a full lesson

Create a Markdown file and add metadata with a unique two-digit ID, integer stage, title, summary, time estimate in minutes, objectives, quiz, and file path. A lesson in the existing practice curriculum needs a useful explanation, an example, three exercises, clear evidence requirements, and solution guidance. This contract applies to practice lessons, not to guided reading topics. The portal uses the metadata rather than guessing titles from filenames.

## Update external resources

Open the primary destination, verify its title and relevance, and record the check date and limitations. Do not silently label a search snippet as a verified page. Replace obsolete provider instructions with current official documentation. Keep the learning objective stable where possible. Resource availability, prices, badges, and interfaces can change; the catalog's access labels are guidance, not purchase guarantees.

## Extend the harness

Keep deterministic tests fast and offline. Add live providers behind an explicit adapter and opt-in command. Treat their outputs as untrusted proposals that must pass the same tool validation. Measure provider token use separately from local runtime steps. A simulated timeout does not test real process isolation; a production deployment needs appropriate cancellation and resource boundaries.

Run the integration commands from labs 09–11 as separate release checks. The MCP SDK environment must be isolated from the dependency-free core. Skill package validation and host behavioral checks are different evidence; report both accurately. Changing component code or its selected profile invalidates a composed run's resume identity.

The portal's asset allowlist is generated from teaching code and data under `content/` and `lab/`, excluding runtime/dependency directories. Keep personal outputs under `work/` or `.lab-runs/`; do not place credentials or learner transcripts in distributed source folders.

## Content rights and commercialization

Read `docs/REUSE.md`. Link to external courses and books; do not copy them into a commercial bundle. Before selling a version, run a real learner pilot, collect consented feedback, verify every exercise, commission a subject-matter review, and define what support and updates are included. A price is a business decision supported by customer evidence, not a property generated by adding pages.

## Whole-course teaching and discovery checks

Every lesson must have the eight beginner headings validated by check_content.py, a self-contained assistant prompt, a small teaching example distinct from assignment answers, concrete expected observations, recovery steps, prerequisites, and a scoped primary reading. A beginner should know what to open, what to paste, and what to check. Do not make producing diagrams/documents the first teaching step. Keep the original lesson body and its three exercises; edit stale notices when needed, but do not delete useful content.

The home and subject catalog must expose every subject. Each subject lists all its beginner-to-advanced topics; all 24 original lessons must also remain available in their subjects and the original map. Find learning materials indexes every distributed Markdown document and external library entry by title, format, and topic keywords. Search results must not reveal answer text. Each lesson and stage must link its related materials. Downloaded Markdown and source ZIP remain editable; the original PDF is explicitly labeled as the earlier practice edition.

Run `node scripts/test_course_approach.cjs` in addition to the existing suites. It checks all 24 teaching pages, visible navigation, material search, answer protection, and explicit lesson bookmarks with import/reload. The original lesson solution outline is absent from the lesson DOM until all three meaningful recorded attempts and an explicit reveal. Per-exercise and incident gates remain independent. No page visit or bookmark marks completion.

## Subject-track release checks

Run `python3 scripts/check_tracks.py` (also included in check_content.py) to validate required subjects, all three levels, prerequisite order/cycles, original-lesson coverage, topic teaching sections, source metadata, material paths, and curated path references. Do not require a new exercise ID just to add a reading topic.

Run `node scripts/test_subject_tracks.cjs` on the static preview for all subject/topic pages, every step of every curated path, mobile widths, current sidebar location, scoped source links, preserved answer gates, context-preserving detours, search, and explicit subject bookmark reload/export/import. The original course and primer suites remain compatibility checks. `node scripts/test_local_progress.cjs` also tests subject bookmark/path/notes across browser and server restarts with an isolated SQLite profile.

Preserve read-only navigation: visiting topics, expanding the site map, following a path, or inspecting a source must not mutate learning records. Reading an old lesson through a subject must share its original note key and practice IDs. Unknown subject/path routes should fail gracefully, and invalid path context should fall back to the subject sequence. Keep all privacy/package tests and build both ZIP downloads before publication.
