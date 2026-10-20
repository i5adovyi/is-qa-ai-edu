# AI Engineering Academy

A practical, self-paced academy for learning to design, build, test, and operate AI-assisted workflows. It combines a course, a learning portal, runnable engineering labs, and instructions for an AI tutor. This repository is the complete editable project.

The initial build is complete. Read the [project closeout and retrospective](docs/PROJECT-CLOSEOUT.md) for delivered scope, historical decisions, verification, storage locations and remaining limitations. Use the instructions below to learn or maintain the project.

## Project idea

The goal is to become capable of doing real work with AI: frame a task, provide useful context, connect tools and skills, supervise coding agents, build a harness that controls execution, and evaluate whether the result is trustworthy. The learning method is **predict → attempt → inspect evidence → get feedback → revise → transfer to a new case**.

The shared case study is **Signal Desk**, a fictional support and QA team. It gives the lessons a continuous engineering problem: move from a ticket and incomplete evidence to a justified, reviewable result. Learners build and test bounded components before combining them into a harness. Later exercises introduce interrupted work, conflicting evidence, stale context, coordination failures, and release decisions. The final capstone can focus on support, QA, or research.

The intended experience is practical self-study with an AI tutor giving one exercise at a time. A learner can start with diagrams and task contracts, continue with offline Python labs, and add actual model/tool integrations when access is available. The course is designed to remain usable after changing assistant accounts or subscriptions.

**Success means reproducible work and an explanation of its limits.** Completion ticks, passing a quiz, or running a reference solution alone do not demonstrate independent mastery. The core fixtures are synthetic; this repository is an educational environment, not a deployed customer-support service.

## If this is a new assistant session

| Your task | Read next | Start with |
| --- | --- | --- |
| Tutor the learner | [AGENTS.md](AGENTS.md), [tutor handoff](docs/CONTINUE-LEARNING.md), [start guide](docs/START-HERE.md) | The learner's latest attempt or supplied progress export; give one next checkpoint |
| Maintain the course or application | [AGENTS.md](AGENTS.md), [maintenance](docs/MAINTENANCE.md), [verification record](docs/VERIFICATION.md) | The current request, `git status`, and the relevant source files |
| Use another assistant account or create another Site | [new-account guide](docs/NEW-ACCOUNT.md) | Reopen the existing local clone, or prepare a separate publication copy |
| Recover or move learning records | [local data guide](docs/LOCAL-DATA.md) | Identify the actual data directory/browser, then back up before recovery |

[CLAUDE.md](CLAUDE.md) is the Claude entry point; [AGENTS.md](AGENTS.md) contains the shared working rules. Neither file is a learner transcript or a replacement for current evidence. Older audits describe their release at the time; inspect the current code and run relevant checks before making new claims.

## Start here

Use the [private OpenAI-hosted academy](https://signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site/), or run this copy locally with:

```sh
python3 academy.py local
```

This builds from source and opens `http://127.0.0.1:8765/`. Local attempts, notes, and progress are saved between sessions in `.academy-data/progress.sqlite3`. The same command works in the ready-built portable ZIP. `python3 academy.py hosted` opens the configured hosted copy instead. See [Run anywhere](docs/RUN-ANYWHERE.md) for Windows, ports, progress transfer, GitHub updates, and OpenAI Sites publishing.

**Using another OpenAI account?** Open this same folder in Codex after signing in to that account. Follow [NEW-ACCOUNT.md](docs/NEW-ACCOUNT.md) for the tutor handoff, GitHub reconnection, and preparing a separate private Site owned by that account. For editing with Codex, Claude, or another coding assistant, use the Git clone or editable source ZIP. The portable ZIP is a ready-built reader and includes `dist/academy-source.zip` for extracting an editable project.

1. Follow [fresh-copy setup](docs/SETUP.md) to get the files, run the demo and checks, and open the local portal.
2. Continue with [START HERE](docs/START-HERE.md), including the first 90-minute session. Keep the portal server running in its terminal and use another terminal for exercises.

Python 3.9+ is supported (tested here with Python 3.9.6). The portal builder and reference lab use the standard library; no package install, model subscription, or API key is needed. The bundled lab policy is deterministic and is explicitly not an LLM. Bring a model of your choice for the optional model experiments.

## What is inside

- Eight stages and 24 lessons, each with teaching material, a worked example, three exercises, hints, solution guidance, and a knowledge check.
- Fifteen lab guides: eight component exercises, real MCP, host-installed skills, a composed student harness, a model-directed tool loop, coding and worker practice, retrieval comparison, and review/rollback operations.
- Six incident exercises and one capstone incident, with disposable local workspaces, conflicting evidence, transfer variants, and hints/debriefs unlocked after a recorded attempt.
- Original articles, learner manuals, reusable engineering templates, and three substantial capstone briefs.
- A curated library of courses, books, documentation, papers, and videos, with practical follow-up tasks.
- A local learning portal with beginner preparation, 72 exercise workspaces, 72 applied checks, progressive hints, attempt/feedback history, tutor packets, recall practice, notes, bookmarks, SQLite persistence, and JSON progress export/import.
- An original PDF fieldbook and a downloadable source archive.

See the [practice map](docs/PRACTICE-MAP.md) for prerequisites and lesson-to-lab links. To try your current chat model without an API integration, follow the [model response bridge](lab/model-bridge.md).

Follow the [incident route](content/incidents/README.md) at its scheduled points. Preserve evidence, write competing hypotheses, and test a discriminating prediction before changing code. The fixtures simulate service behavior locally; no paid model or real customer system is needed. Portal and terminal attempts are separate learning records. Their answer gates support deliberate practice, not secure examinations.

Begin with the [preparation module](content/onboarding/README.md). It teaches diagram notation on a different scenario, checks the coding prerequisites, and helps you choose the concept, local engineering, or live-model route. The portal saves drafts and attempts locally; use its export feature to preserve your feedback and review history.

After the component exercises, follow the [integration route](docs/INTEGRATION-LABS.md). It connects protocol behavior, installed skills, and your own harness components to observable results.

The [learning experience implementation record](docs/LEARNING-EXPERIENCE-IMPLEMENTATION.md) maps an earlier expansion to its checks. The [future-project readiness guide](docs/FUTURE-PROJECT-READINESS.md) adds API/environment diagnosis, model migration, and evolving evaluation data. The [fresh-clone student audit](docs/STUDENT-AUDIT.md) and [second review report](docs/REVIEW-2026-10-20.md) preserve earlier findings. The [verification record](docs/VERIFICATION.md) states exactly what was run for each recorded release.

## How the project fits together

| Source | Responsibility |
| --- | --- |
| `content/curriculum.json`, `content/learning.json` | Lesson order, objectives, exercise/check contracts, hints, recall and transfer |
| `content/lessons/`, `content/labs/`, `content/incidents/` | Student-facing lessons and executable practice guides |
| `docs/`, `templates/`, `capstones/` | Study plan, operating manuals, evidence templates and final project briefs |
| `content/resources.json` | External learning material with practice tasks and access notes |
| `lab/` | Reference harness, student components, MCP/skill/model-loop labs and incident simulations |
| `portal/` | HTML, CSS and JavaScript interface; progress, attempts, hints and tutor packets |
| `academy.py`, `academy_local.py` | Local launcher, loopback HTTP API, SQLite storage and backup commands |
| `scripts/`, `tests/` | Builds, packaging, checks, new-account preparation and regression tests |
| `dist/`, `output/pdf/` | Generated portal/downloads and fieldbook; change their source and rebuild |
| `academy.json`, `.openai/hosting.json` | Hosted/repository URLs and the identity/configuration of this copy's Site |

The portal builder combines the course sources into static `dist/` assets. OpenAI Sites serves those assets with browser-local learning records. The local launcher serves the same assets and adds a SQLite-backed progress API on loopback. The Python labs are separate terminal programs: the portal does not run a learner's Python code, install skills, or verify an execution claim.

Some unfinished code and failing scenarios are deliberate assignments. Preserve `lab/student.py`, the seeded coding sandbox, and incident starters unless the task explicitly concerns their design. Reference/completed implementations support comparison; they are not a substitute for the learner's attempt.

## What persists, and where

| Information | Location | Transfer and backup |
| --- | --- | --- |
| Course, application and test source | Private Git repository | Commit/push source changes |
| Local portal progress | `.academy-data/progress.sqlite3`, or the selected `--data-dir` | SQLite backup; JSON export/import for another portal |
| Hosted portal progress | Browser storage for that Site's origin/profile | Export/import JSON; no automatic local/cloud synchronization |
| Lab evidence and learner files | Ignored `work/`, `.lab-runs/`, or another chosen private directory | Back up separately |
| Assistant conversation history | The assistant/account where it occurred | Not recreated by cloning this repository |

Keep personal records out of Git, release ZIPs, and Sites uploads. A fresh clone does not contain your progress. Use the same project/data directory to resume locally; the interface distinguishes confirmed database saves from pending work and conflicts. See [backup and recovery](docs/LOCAL-DATA.md).

GitHub pushes and Sites publication are separate operations. Updating an existing Site preserves its identity and audience. Creating a Site under a different account uses a separate prepared copy and an authenticated publishing session in that account; see [the migration checklist](docs/ACCOUNT-MIGRATION.md) and [new-account workflow](docs/NEW-ACCOUNT.md).

## Choose a pace

| Route | Suggested cadence | Outcome |
| --- | --- | --- |
| Foundations | 4 weeks, 4-6 hours/week | Complete stages 1-3 and the first two labs |
| Builder | Twelve-week core scaffold, then extend for the chosen practice | Complete lessons and core labs, then integrations, incidents, and one capstone at your measured pace |
| Intensive | Six-week core scaffold, 12-16 hours/week, plus extensions | Same core work, with two review sessions per week; budget integration and incident work separately |
| Practitioner | Self-paced | Take the diagnostic, attempt stage gates, fill demonstrated gaps |

These are planning estimates, not measured completion times. Use the [study plan](docs/STUDY-PLAN.md) for separate integration, incident, and capstone budgets; the full route is not a guaranteed twelve-week finish.

## Commands

Choose the command for the task; these are not a sequence to paste together. The local server stays running until Ctrl+C. Run labs in another terminal.

| Task | Command |
| --- | --- |
| Start/resume local learning | `python3 academy.py local` |
| Inspect the local profile without printing attempts | `python3 academy.py status` |
| Create a backup at a new filename | `python3 academy.py backup --output ../academy-progress-backup.sqlite3` |
| Prepare a separate, unpublished account copy | `python3 scripts/prepare_new_site.py --destination ../academy-new-account` |
| Run the reference demonstration | `python3 -m lab.cli demo` |
| Evaluate the reference harness | `python3 -m lab.cli evaluate --split train` |
| Check the completed composition, when maintaining it | `python3 -m lab.composed evaluate --components completed --split all` |
| Run Python checks | `python3 -m unittest discover -s tests` |
| Run portal unit checks | `node --test tests/test_portal.cjs` |
| Validate course links and contracts | `python3 scripts/check_content.py` |
| Rebuild the portal and downloadable packages | `python3 scripts/build_portal.py` |

See [the lab manual](lab/README.md) for the exact harness commands and [maintenance](docs/MAINTENANCE.md) for builds, content conventions, and release checks.

## Learning rules

Save evidence, not just completion ticks. Make a prediction before every experiment. Keep at least one untouched evaluation split. Ask your AI tutor for hints before solutions. Every final claim about quality should point to a trace, a test, a dataset, or a human judgment with a rubric.

Course text and code are original educational material. External books, courses, and videos remain with their respective owners; the library links to authorized sources and does not bundle their content. See [reuse and attribution](docs/REUSE.md). This project does not claim university accreditation, vendor certification, or a validated commercial price.
