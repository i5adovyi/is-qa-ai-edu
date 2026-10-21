# AI for SDET — a guided learning academy

A provider-neutral learning project that gathers scattered AI knowledge into a useful sequence for an SDET. Start with plain explanations and testing examples, follow selected external articles or courses when you need depth, and progress toward context engineering, tools, skills, agents, evaluation, and harnesses.

**Start with [What AI can do for an SDET](content/guide/01-ai-basics.md)** or open the [private learning portal](https://signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site/#guide=01). No drawing, report, installation, or graded exercise is required to start.

## The learning experience

1. Read one guided topic and its SDET example.
2. Use its selected external reading if you want more detail. The page tells you which sections to read and where to stop.
3. Choose Next topic. Save my place remembers your chosen reading location without marking completion.
4. Open related practice when you want to try the concept. A tutor gives one exercise at a time and keeps solutions hidden until you try.

The [study plan](docs/STUDY-PLAN.md) starts with using AI in testing, continues with testing AI systems and retrieval, then explains tools, MCP, skills, agents, and reliable harnesses. Microsoft, GitHub, OpenAI, Hugging Face, Google, Anthropic, and OWASP contribute different resources. You do not need to complete every provider's catalog.

The original 24 lessons, 15 lab guides, six incidents plus a capstone incident, articles, manuals, templates, books, videos, and capstones are retained as an optional practice and reference collection. The portal links each guided topic to useful existing material. The full collection remains accessible from Optional practice & reference. The PDF is the original practice fieldbook; the new guided route lives in the portal and Markdown files.

## New assistant session

Read [AGENTS.md](AGENTS.md) and identify whether the user wants explanation, practice, maintenance, or setup. [CLAUDE.md](CLAUDE.md) points to the same rules.

- Tutoring: use [the handoff](docs/CONTINUE-LEARNING.md) and [tutor prompt](templates/tutor-prompt.md). Explain one topic first. Do not make diagrams or documents mandatory. Never invent remembered progress.
- Maintenance: read [MAINTENANCE.md](docs/MAINTENANCE.md), inspect Git status, edit source, and run the relevant checks.
- Another account: follow [NEW-ACCOUNT.md](docs/NEW-ACCOUNT.md). A local clone remains usable independently of the original OpenAI login.
- Progress recovery: use [LOCAL-DATA.md](docs/LOCAL-DATA.md). Preserve the actual learner database and browser exports.

## Run locally

```sh
python3 academy.py local
```

The launcher builds the source and opens `http://127.0.0.1:8765/`. Python 3.9+ is supported for the core; it uses the standard library. No model key or subscription is needed to read the course or run the reference simulation. Optional model, MCP, and host integrations have separate requirements.

For a fresh clone, Windows commands, ports, and package choices, see [SETUP.md](docs/SETUP.md) and [RUN-ANYWHERE.md](docs/RUN-ANYWHERE.md). The ready-built portable ZIP is a reader; the Git clone or source ZIP is the editable project. `python3 academy.py hosted` opens the configured hosted copy.

## What is saved

| Information | Location | Transfer |
| --- | --- | --- |
| Course, portal, labs, and tests | Private Git repository | Commit and push source changes |
| Local reading place, notes, and practice records | Ignored `.academy-data/progress.sqlite3` or explicit `--data-dir` | SQLite backup or JSON export/import |
| Hosted reading place, notes, and practice records | Browser storage for the Site's origin/profile | JSON export/import |
| Lab evidence | Ignored `work/`, `.lab-runs/`, or a learner-selected directory | Back up separately |
| Assistant chat history | Its original account | Not included in a Git clone |

Local and hosted records do not synchronize automatically. Saving a reading place does not mean completing a lesson. Keep private data, credentials, and transcripts out of Git, ZIP downloads, and Site uploads. See [local backup and recovery](docs/LOCAL-DATA.md).

## Source map

| Source | Purpose |
| --- | --- |
| `content/sdet-path.json`, `content/guide/` | Default topic sequence, explanations, selected source scopes, access notes, and links to existing material |
| `content/curriculum.json`, `content/learning.json`, `content/lessons/` | Retained practical syllabus, exercises, hints, checks, and tutor packets |
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
