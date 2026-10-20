# Maintain and extend the academy

The editable source is this repository. The portal is generated into `dist/`; do not edit generated content there. The build also refreshes the downloadable source archive, so a newly extracted project can rebuild all portal downloads. Lessons and reference material are ordinary Markdown so the course remains usable without its interface.

## Structure

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
- `scripts/`: build, serving, packaging, and content validation.
- `work/`: your private experiment outputs, intentionally excluded from distribution.

## Release checks

These are maintainer checks. Install Node.js 22 or newer for the JavaScript tests; it is not required for the student Python route. Browser checks additionally need Playwright and a compatible browser. The PDF rebuild needs ReportLab; the generated PDF is included for readers.

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 scripts/check_content.py
python3 scripts/build_portal.py
python3 scripts/serve.py
```

Open overview, a lesson, a lab, the library, and a manual. Check keyboard navigation, narrow screens, quiz feedback, saved notes, progress export, and import. Browser storage is local to its origin; a local preview and hosted portal do not share progress. Export and import JSON to transfer it. Browser data can be erased; keep backups.

With the local server running and Playwright available, run `node scripts/test_portal.cjs` for interactions and `node scripts/audit_portal.cjs` for every document, internal link, quiz answer, downloadable asset, and mobile document layout. `ACADEMY_BROWSER_PATH` selects an installed browser executable. When testing another checkout, set `ACADEMY_TEST_URL` to its server and `ACADEMY_DIST_DIR` to its matching `dist/`; the audit compares download hashes with that exact build.

Also run `node scripts/test_learning_portal.cjs` for the exercise workspace, spoiler protection, v1 progress migration, feedback history, import conflicts, recall, and narrow-screen behavior. The v2 progress schema must preserve original attempts; do not silently overwrite a learner's history on import.

Run `node scripts/test_incident_portal.cjs` for incident attempt gates, progressive hints, deliberate debrief reveal, reload and import behavior. Incident guidance must stay out of the DOM and tutor packet before explicit disclosure. The source archive contains editable guidance; the static portal is not an examination security system. The PDF includes incident briefs but omits their guidance because it cannot enforce an attempt gate.

The GitHub Actions workflow runs core and optional MCP checks with no model credentials. Live Codex/provider calls are deliberately explicit local checks. Record CI execution separately from a locally passing workflow command.

The [Run anywhere guide](RUN-ANYWHERE.md) separates local startup, private GitHub source updates, and OpenAI Sites publication. `python3 academy.py local` rebuilds source copies and serves only `dist/` on loopback; `python3 academy.py hosted` opens the existing hosted copy. A GitHub push does not by itself deploy Sites.

Launcher checks are included in Python discovery (`tests/test_launcher.py`). They cover source/portable startup from a different directory, legacy commands, occupied/invalid ports, missing files, build failures, serving only the built directory, and an extract/run/download round trip. An extracted portable copy regenerates its portable ZIP download in memory from the course assets; it does not package arbitrary files from the learner's directory. Run `node scripts/test_run_anywhere.cjs` for the mode selector, links, portable download, progress navigation and mobile layout.

## Add a lesson

Create a Markdown file and add metadata with a unique two-digit ID, integer stage, title, summary, time estimate in minutes, objectives, quiz, and file path. A lesson needs a useful explanation, an example, three exercises, clear evidence requirements, and solution guidance. The portal uses the metadata rather than guessing titles from filenames.

## Update external resources

Open the primary destination, verify its title and relevance, and record the check date and limitations. Do not silently label a search snippet as a verified page. Replace obsolete provider instructions with current official documentation. Keep the learning objective stable where possible. Resource availability, prices, badges, and interfaces can change; the catalog's access labels are guidance, not purchase guarantees.

## Extend the harness

Keep deterministic tests fast and offline. Add live providers behind an explicit adapter and opt-in command. Treat their outputs as untrusted proposals that must pass the same tool validation. Measure provider token use separately from local runtime steps. A simulated timeout does not test real process isolation; a production deployment needs appropriate cancellation and resource boundaries.

Run the integration commands from labs 09–11 as separate release checks. The MCP SDK environment must be isolated from the dependency-free core. Skill package validation and host behavioral checks are different evidence; report both accurately. Changing component code or its selected profile invalidates a composed run's resume identity.

The portal's asset allowlist is generated from teaching code and data under `content/` and `lab/`, excluding runtime/dependency directories. Keep personal outputs under `work/` or `.lab-runs/`; do not place credentials or learner transcripts in distributed source folders.

## Content rights and commercialization

Read `docs/REUSE.md`. Link to external courses and books; do not copy them into a commercial bundle. Before selling a version, run a real learner pilot, collect consented feedback, verify every exercise, commission a subject-matter review, and define what support and updates are included. A price is a business decision supported by customer evidence, not a property generated by adding pages.
