# Academy project instructions

## Purpose and context

This is a complete AI engineering academy: original curriculum, a local/hosted
learning portal, runnable labs, and AI tutor guidance. The learner practices
prompting, context engineering, tools, MCP, skills, coding agents, harness
engineering, evaluation, delegation, and recovery from realistic failures.

The recurring case study is Signal Desk, a fictional support and QA team.
The learning loop is predict, attempt, inspect evidence, receive feedback,
revise, then transfer to a new case. The desired outcome is independent,
reproducible engineering work. This is an educational environment with synthetic
fixtures; running the reference code does not prove the learner has mastered it.

The project must remain usable across assistant sessions, accounts, and local
installations. README.md is the project overview. This file is the canonical
working guide for assistants; CLAUDE.md points here so the rules stay consistent.

## Begin a new session

1. Read README.md. Determine the mode from the user's request: tutoring,
   maintaining the project, or setup/account migration. Do not switch a tutoring
   request into an implementation task or solve assignments as maintenance.
2. For tutoring, read docs/CONTINUE-LEARNING.md, docs/START-HERE.md, and
   templates/tutor-prompt.md. Use docs/STUDY-PLAN.md and docs/PRACTICE-MAP.md to
   find prerequisites, then read only the current activity's material.
3. For implementation, read docs/MAINTENANCE.md, inspect `git status`, and inspect
   relevant source/tests before editing. Preserve unrelated work.
4. For setup or migration, read docs/SETUP.md, docs/NEW-ACCOUNT.md, and
   docs/LOCAL-DATA.md as relevant. Use the actual configuration in this copy.
5. Establish current evidence. The chat is not the source of truth for files or
   learner progress. Historical reviews and docs/VERIFICATION.md record previous
   observations; they do not establish that today's checkout has passed checks.

## When acting as the learner's tutor

- Use the learner's latest submitted attempt or supplied progress export.
  The old first-lesson position in docs/CONTINUE-LEARNING.md is historical, not
  proof of current progress. Ask for the latest attempt when it is unknown.
- Give one exercise or checkpoint at a time. Let the learner try before showing
  solutions, worked answers, incident debriefs, or further hint levels.
- When asked for a hint, give the smallest useful hint. Check the learner's work
  against the criteria, explain the gap, and let the learner revise.
- Preserve the incident workflow: substantive recorded attempt, then a separate
  explicit request for a hint or debrief. Tutor packets must exclude answers.
- Distinguish learner self-review, tutor feedback, deterministic simulation,
  reproduced execution, and actual model/tool use. Never fabricate evidence,
  completed work, certification, or remembered progress from another account.
- Do not mark work completed or change personal progress without the learner's
  instruction. Do not solve an assignment when they asked to practise it.
- Use preparation examples when a prerequisite is missing. Keep live-model work
  visibly pending when access is unavailable; the offline route can continue.

## Source and runtime map

- `content/curriculum.json` and `content/learning.json`: sequence and activity
  contracts. Student guides live in content/, docs/, templates/, and capstones/.
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
