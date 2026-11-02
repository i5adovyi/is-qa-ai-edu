# AI for SDET — a guided learning academy

A provider-neutral learning project that gathers scattered AI knowledge into a useful sequence for an SDET. Start with plain explanations and testing examples, follow selected external articles or courses when you need depth, and progress toward context engineering, tools, skills, agents, evaluation, and harnesses.

**[Start from zero](docs/START-HERE.md)** to read on GitHub, or [run the portal locally](#run-locally) to browse lessons and save your place.

## The learning experience

1. Understand the concept in plain language and see a small SDET example.
2. Follow the lesson's concrete how-to in Codex or Claude Code. Check its output and learn how to recover when it goes wrong.
3. Open one selected external reading when you want depth, or continue to the next lesson. Save my place remembers your explicit bookmark without marking completion.
4. Choose practice after understanding. Your tutor gives one exercise at a time and keeps assignment answers hidden until you try and ask.

The [study plan](docs/STUDY-PLAN.md) now has **14 independent subject tracks and 84 topics**, ordered beginner → intermediate → advanced within each subject. AI foundations, coding assistants, prompting, context engineering, retrieval/RAG/memory, tools/APIs, MCP, skills, agentic development, harness engineering, evaluation, multi-agent systems, security, and production each have a separate visible home. The 24 original lessons are retained inside those tracks, alongside 60 new readings.

Four **Learning paths** combine selected topics for a goal: Start from zero, AI in everyday SDET work, Building controlled agents, and Operate and evaluate AI systems. Start from zero is the default; the complete catalog is available without becoming mandatory homework. Every topic defines terms, teaches with an SDET example, gives a concrete assistant prompt, and explains what to check when it goes wrong. [Learn with Codex or Claude Code](docs/ASSISTANT-QUICKSTART.md) helps you get started with the assistant you have.

The sidebar exposes every subject, searches topics, and highlights your location. **All subjects** shows the full catalog; **Find learning materials** indexes all retained content and scoped source selections. **Original lesson sequence** preserves the earlier 24-lesson map and stable URLs. On mobile, the Site map button opens an accessible drawer. Multiple providers contribute selected articles, docs, courses, books, and videos; you do not need every provider's catalog.

All original lessons, 72 exercises, 15 lab guides, six incidents plus a capstone incident, articles, manuals, templates, books, videos, and capstones are retained. The PDF is the original practice fieldbook; the new beginner guides live in the portal, Markdown, and source download.

Use **Theme** at the top of any page to choose **Dark**, **Light**, or **System** (the default follows your device). The choice is saved in this browser for this site, separately from learning progress. It is not included in progress exports or the local database.

## New assistant session

Read [AGENTS.md](AGENTS.md) and identify whether the user wants explanation, practice, maintenance, or setup. [CLAUDE.md](CLAUDE.md) points to the same rules.

- Tutoring: use [the handoff](docs/CONTINUE-LEARNING.md) and [tutor prompt](templates/tutor-prompt.md). Explain one topic first. Do not make diagrams or documents mandatory. Never invent remembered progress.
- Maintenance: read [MAINTENANCE.md](docs/MAINTENANCE.md), inspect Git status, edit source, and run the relevant checks.
- Another account: follow [NEW-ACCOUNT.md](docs/NEW-ACCOUNT.md). A local clone remains usable independently of the original OpenAI login.
- Progress recovery: use [LOCAL-DATA.md](docs/LOCAL-DATA.md). Preserve the actual learner database and browser exports.

## Run locally

From the project folder on Windows:

```powershell
python academy.py local
```

On macOS or Linux:

```sh
python3 academy.py local
```

The launcher builds the source and opens `http://127.0.0.1:8765/`. Python 3.9+ is supported for the core; it uses the standard library. No model key or subscription is needed to read the course or run the reference simulation. Optional model, MCP, and host integrations have separate requirements.

For a fresh clone, Windows commands, ports, and package choices, see [SETUP.md](docs/SETUP.md) and [RUN-ANYWHERE.md](docs/RUN-ANYWHERE.md). The ready-built portable ZIP is a reader; the Git clone or source ZIP is the editable project. `python3 academy.py hosted` opens the configured hosted copy.

## What is saved

| Information | Location | Transfer |
| --- | --- | --- |
| Course, portal, labs, and tests | Git repository | Commit and push source changes |
| Local reading place, notes, and practice records | Ignored `.academy-data/progress.sqlite3` or explicit `--data-dir` | SQLite backup or JSON export/import |
| Hosted reading place, notes, and practice records | Browser storage for the Site's origin/profile | JSON export/import |
| Lab evidence | Ignored `work/`, `.lab-runs/`, or a learner-selected directory | Back up separately |
| Assistant chat history | Its original account | Not included in a Git clone |

Local and hosted records do not synchronize automatically. Saving a reading place does not mean completing a lesson. Keep private data, credentials, and transcripts out of Git, ZIP downloads, and Site uploads. See [local backup and recovery](docs/LOCAL-DATA.md).

## Source map

| Source | Purpose |
| --- | --- |
| `content/tracks/` | Subject catalogs, 60 new readings, and four curated path definitions |
| `content/how-to/` | Beginner teaching guides for all 24 lessons and maps of prerequisites, related materials, and scoped readings |
| `content/sdet-path.json`, `content/guide/` | Retained short primers and scoped source selections |
| `content/curriculum.json`, `content/learning.json`, `content/lessons/` | Retained original 24-lesson sequence, original explanations, exercises, hints, checks, and tutor packets |
| `content/resources.json`, `content/library/` | Broader external resource collection |
| `content/labs/`, `content/incidents/`, `lab/`, `capstones/` | Optional runnable practice and investigations |
| `docs/`, `templates/` | Study guidance, operation, account migration, and optional engineering templates |
| `portal/` | HTML/CSS/JavaScript interface source |
| `academy.py`, `academy_local.py` | Launcher, loopback progress API, and SQLite persistence |
| `scripts/`, `tests/` | Build, packaging, validation, and regression checks |
| `dist/`, `output/pdf/` | Generated site/downloads and original practice fieldbook |
| `academy.json`, `.openai/hosting.json` | Repository/hosted URLs and this Site's publication identity |

Edit source and rebuild with `python3 scripts/build_portal.py`; do not hand-edit dist/. GitHub push and Sites publication are separate operations. Preserve the existing Site and private audience on updates. A new account's separate Site needs the identity-free preparation workflow in [NEW-ACCOUNT.md](docs/NEW-ACCOUNT.md).

## Verification and project history

Run the relevant checks listed in [maintenance](docs/MAINTENANCE.md). Ordinary core checks include:

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 scripts/check_content.py
python3 scripts/build_portal.py
```

The original engineering overview and commands are retained in [the practice-edition overview](docs/PROJECT-OVERVIEW-2026-10-20.md). Its hands-on learning loop remains useful when chosen deliberately. The [practice schedule](docs/PRACTICE-STUDY-PLAN.md) and [practice orientation](docs/PRACTICE-START.md) preserve the earlier diagnostic and extended routes.

The [initial closeout](docs/PROJECT-CLOSEOUT.md) records the original implementation. Learner feedback then exposed a mismatch: too much assignment/navigation before explanation. [The learning-design correction](docs/LEARNING-DESIGN-2026-10-21.md) records the change in direction. Historical test results demonstrate the tested software behavior, not that the learning experience was effective.

Course text and code are original educational material. External content is linked, not copied into the project. Reading, quizzes, or reference-code execution alone do not establish mastery, accreditation, or a commercial value. See [reuse and attribution](docs/REUSE.md).
