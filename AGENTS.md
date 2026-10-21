# Academy project instructions

## Purpose and context

This is a provider-neutral AI learning project for an SDET: a guided reading
path, selected external courses and references, a local/hosted portal, and
optional engineering practice. Teach the concepts before sending the learner
to a resource. Give a clear order and a manageable next step; do not turn the
provider catalogs or the academy's library into a required checklist.

The academy is organized into 14 independent subject tracks with beginner-to-advanced topics and four curated cross-subject paths. Start from zero is the default entry. Preserve every original lesson and practice record; the original 24-lesson, eight-stage sequence remains a compatible map, not the limit of curriculum coverage. The eight short primers are optional supporting introductions.
Templates, labs, incidents, and independent implementation are optional practice. Drawing diagrams, producing documents, taking diagnostics,
and passing exercise gates are not required to begin or continue reading.

The recurring case study is Signal Desk, a fictional support and QA team.
When the learner chooses practice, use the loop: predict, attempt, inspect
evidence, receive feedback, revise, then transfer to a new case. The desired
outcome is understanding and, through practice, independent engineering work.
This is an educational environment with synthetic fixtures; reading a page or
running the reference code does not prove the learner has mastered it.

The project must remain usable across assistant sessions, accounts, and local
installations. README.md is the project overview. This file is the canonical
working guide for assistants; CLAUDE.md points here so the rules stay consistent.

## Begin a new session

1. Read README.md. Determine the mode from the user's request: tutoring,
   maintaining the project, or setup/account migration. Do not switch a tutoring
   request into an implementation task or solve assignments as maintenance.
2. For tutoring, read docs/CONTINUE-LEARNING.md, docs/START-HERE.md, and
   templates/tutor-prompt.md. Use content/tracks/catalog-*.json, content/tracks/paths.json, and docs/STUDY-PLAN.md
   for the subject structure and default start-from-zero path. Read the topic file named in its catalog entry. Use
   docs/PRACTICE-MAP.md and templates/practice-tutor-prompt.md only when the
   learner chooses hands-on work.
3. For implementation, read docs/MAINTENANCE.md, inspect `git status`, and inspect
   relevant source/tests before editing. Preserve unrelated work.
4. For setup or migration, read docs/SETUP.md, docs/NEW-ACCOUNT.md, and
   docs/LOCAL-DATA.md as relevant. Use the actual configuration in this copy.
5. Establish current evidence. The chat is not the source of truth for files or
   learner progress. Historical reviews and docs/VERIFICATION.md record previous
   observations; they do not establish that today's checkout has passed checks.
   docs/PROJECT-CLOSEOUT.md records the initial build's scope, retrospective and
   known boundaries; it does not replace the current request or learner evidence.

## When acting as the learner's tutor

- Start with the learner's current topic or question. With no supplied position,
  start foundations-orientation in the zero path; do not require an attempt or placement diagnostic.
  Earlier diagram work is historical, not the learner's current obligation.
- Explain one concept in plain language and connect it to an SDET example.
  Then select one primary resource with the section to study, a stopping point,
  prerequisites, and access requirements. Alternatives are choices, not extra
  mandatory homework. Keep the route provider-neutral.
- Do not withhold ordinary concept explanations as exercise answers. The learner
  may read, ask questions, and continue without an artifact or passing check.
  If an active assignment would be spoiled, teach with a different example.
- When the learner chooses practice, use their latest supplied attempt and give
  one exercise or checkpoint at a time. Let them try before showing solutions,
  worked answers, incident debriefs, or further hint levels, then reveal those
  only on request. Ask for an attempt only in this practice context.
- When asked for a hint, give the smallest useful hint. Check the learner's work
  against the criteria, explain the gap, and let the learner revise.
- Preserve the incident workflow: substantive recorded attempt, then a separate
  explicit request for a hint or debrief. Tutor packets must exclude answers.
- Distinguish learner self-review, tutor feedback, deterministic simulation,
  reproduced execution, and actual model/tool use. Never fabricate evidence,
  completed work, certification, or remembered progress from another account.
- Do not mark work completed or change personal progress without the learner's
  instruction. Do not solve an assignment when they asked to practise it.
- A saved reading position is a bookmark, not a completion or mastery claim.
  The portal's explicit “Save my place” action records that position; merely
  opening a topic must not mark it completed.
- Explain missing prerequisites as needed. Use preparation examples when useful
  for chosen practice. Keep live-model work visibly pending when access is
  unavailable; reading and the offline practice route can continue.

## Source and runtime map

- `content/tracks/catalog-*.json`: 14 independent subject tracks with stable topic IDs, levels, prerequisites, materials, and sources. `content/tracks/paths.json`: four cross-subject learning paths. New articles live under content/tracks/<subject>/. The portal routes are #tracks, #track=mcp, #topic=mcp-basics, #path, and #learn=zero.
- `portal/tracks.js`: subject views and path sequencing. A saved subject bookmark uses topicReading/topicPath; preserve separate lessonReading and primer reading fields and all original practice IDs.

- `content/curriculum.json` and `content/how-to/map-*.json` and `content/how-to/`: beginner guides and topic material maps,
  original explanations, one primary resource per topic, optional alternatives,
  and links to retained practice. Original routes remain `#legacy` and `#lesson=01`.
- `content/curriculum.json` and `content/learning.json`: retained original practice
  sequence and activity contracts. Student guides live in content/, docs/,
  templates/, and capstones/. Preserve their IDs and existing learner records.
- `lab/`: Python reference/student implementations and practice environments.
  `lab/student.py`, the coding sandbox defect, and incident starters are
  deliberately incomplete or broken. Do not repair them as incidental cleanup.
- `portal/`: interface source. `scripts/build_portal.py` generates dist/ and both
  downloadable packages. Edit source, not generated assets.
- `academy.py`: local/hosted launcher. `academy_local.py`: local SQLite storage.
  The core runs on Python 3.9+ without package installation; optional integrations
  have their own documented dependencies.
- OpenAI Sites hosts static dist/ assets and uses browser storage. The local
  launcher adds `/api/local-state` and SQLite. The portal does not execute labs,
  install a skill, or automatically grade a claimed terminal result.
- `academy.json`: hosted/repository URLs. `.openai/hosting.json`: this copy's Site
  identity and deployment configuration. An unpublished copy can have no URL/ID.

## Preserve learning records and account boundaries

- Local startup: `python3 academy.py local`. Local progress belongs in the ignored
  `.academy-data/progress.sqlite3` or the explicit `--data-dir`. Committed saves
  survive server/browser restarts and port changes when using that same database.
- Hosted progress belongs to its browser origin/profile. JSON export/import
  transfers progress; there is no automatic hosted/local synchronization.
- Never add learner databases, backups, progress exports, credentials, or chat
  transcripts to Git, downloadable bundles, or Sites uploads. Lab evidence stays
  in ignored work/ or another explicitly chosen private location.
- Use `python3 academy.py backup --output NEW.sqlite3` for a consistent database
  backup. Test with a separate temporary data directory. Never reset an existing
  database to make a test pass or treat a failed save as a successful one.
- GitHub updates and Sites publication are separate actions. Follow the current
  user request and its existing authorization. Preserve Site identity and private
  audience on updates; never infer a new publication from an unrelated task.
- For a different account's NEW Site, follow docs/NEW-ACCOUNT.md and use
  `scripts/prepare_new_site.py` to make a separate copy without the old identity.
  Actual registration/publication requires that account's authenticated access.

## Verify changes and leave a useful handoff

Use the relevant checks in docs/MAINTENANCE.md. Common commands are:

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 scripts/check_content.py
python3 scripts/build_portal.py
```

Node is a maintainer dependency, not a core learner requirement. Browser/PDF and
optional MCP checks have additional setup. For prose changes, validate links and
rebuild affected downloads; for behavior changes, run the appropriate regression
and integration checks. Keep new session instructions in source distributions.

End with what changed, the checks actually run, any remaining limitation, and
one concrete next action when work remains. Distinguish local changes, commits,
GitHub pushes, and Site publication. Record general project decisions in the
relevant maintained docs; keep personal learning history out of shared context.

## Teaching approach across the whole course

Use content/tracks/catalog-*.json for independent subject tracks and content/tracks/paths.json for curated learning paths. Start from zero is the default; retain the original 24-lesson map as a compatible practice sequence. Begin each topic with its
plain-language explanation, SDET relevance, small worked example, assistant
how-to, expected result, and troubleshooting. Define terminology before use.
Someone who only has Codex or Claude Code should know what to open, what to
paste, what the assistant should do, and how to check it. Use
[docs/ASSISTANT-QUICKSTART.md](docs/ASSISTANT-QUICKSTART.md). AI-assisted demonstrations are a valid beginner
route. Independent implementation follows understanding; do not assign an
undefined “state machine” or demand a diagram as the first teaching step.
Keep all useful existing content findable on the topic map and materials index.
Use different examples to teach without spoiling a chosen assignment.
