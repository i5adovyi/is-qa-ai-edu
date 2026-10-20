# AI Engineering Academy

A practical training project for learning to design, build, test, and operate AI-assisted workflows. The shared case study is **Signal Desk**, a fictional support and QA team. You progress from writing precise requests to constructing an observable agent harness and defending its behavior with evidence.

## Start here

Use the [private OpenAI-hosted academy](https://signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site/), or run this copy locally with:

```sh
python3 academy.py local
```

This builds from source and opens `http://127.0.0.1:8765/`. The same command works in the ready-built portable ZIP. `python3 academy.py hosted` opens the hosted copy instead. See [Run anywhere](docs/RUN-ANYWHERE.md) for Windows, ports, progress transfer, GitHub updates, and OpenAI Sites publishing.

1. Follow [fresh-copy setup](docs/SETUP.md) to get the files, run the demo and checks, and open the local portal.
2. Continue with [START HERE](docs/START-HERE.md), including the first 90-minute session. Keep the portal server running in its terminal and use another terminal for exercises.

Python 3.9+ is supported (tested here with Python 3.9.6). The portal builder and reference lab use the standard library; no package install, model subscription, or API key is needed. The bundled lab policy is deterministic and is explicitly not an LLM. Bring a model of your choice for the optional model experiments.

## What is inside

- Eight stages and 24 lessons, each with teaching material, a worked example, three exercises, hints, solution guidance, and a knowledge check.
- Fifteen lab guides: eight component exercises, real MCP, host-installed skills, a composed student harness, a model-directed tool loop, coding and worker practice, retrieval comparison, and review/rollback operations.
- Six incident exercises and one capstone incident, with disposable local workspaces, conflicting evidence, transfer variants, and hints/debriefs unlocked after a recorded attempt.
- Original articles, learner manuals, reusable engineering templates, and three substantial capstone briefs.
- A curated library of courses, books, documentation, papers, and videos, with practical follow-up tasks.
- A local learning portal with beginner preparation, 72 exercise workspaces, 72 applied checks, progressive hints, attempt/feedback history, tutor packets, recall practice, notes, bookmarks, and JSON progress export/import.
- An original PDF fieldbook and a downloadable source archive.

See the [practice map](docs/PRACTICE-MAP.md) for prerequisites and lesson-to-lab links. To try your current chat model without an API integration, follow the [model response bridge](lab/model-bridge.md).

Follow the [incident route](content/incidents/README.md) at its scheduled points. Preserve evidence, write competing hypotheses, and test a discriminating prediction before changing code. The fixtures simulate service behavior locally; no paid model or real customer system is needed. Portal and terminal attempts are separate learning records. Their answer gates support deliberate practice, not secure examinations.

Begin with the [preparation module](content/onboarding/README.md). It teaches diagram notation on a different scenario, checks the coding prerequisites, and helps you choose the concept, local engineering, or live-model route. The portal saves drafts and attempts locally; use its export feature to preserve your feedback and review history.

Changing OpenAI accounts? Follow the [account migration guide](docs/ACCOUNT-MIGRATION.md) and keep the [tutor handoff](docs/CONTINUE-LEARNING.md). The local course and GitHub repository work independently of the original OpenAI login.

After the component exercises, follow the [integration route](docs/INTEGRATION-LABS.md). It connects protocol behavior, installed skills, and your own harness components to observable results.

The [learning experience implementation record](docs/LEARNING-EXPERIENCE-IMPLEMENTATION.md) maps the latest improvements to their checks. The [future-project readiness guide](docs/FUTURE-PROJECT-READINESS.md) adds API/environment diagnosis, model migration, and evolving evaluation data. The [fresh-clone student audit](docs/STUDENT-AUDIT.md) and [second review report](docs/REVIEW-2026-10-20.md) preserve earlier findings. The [verification record](docs/VERIFICATION.md) states exactly what was run.

## Choose a pace

| Route | Suggested cadence | Outcome |
| --- | --- | --- |
| Foundations | 4 weeks, 4-6 hours/week | Complete stages 1-3 and the first two labs |
| Builder | Twelve-week core scaffold, then extend for the chosen practice | Complete lessons and core labs, then integrations, incidents, and one capstone at your measured pace |
| Intensive | Six-week core scaffold, 12-16 hours/week, plus extensions | Same core work, with two review sessions per week; budget integration and incident work separately |
| Practitioner | Self-paced | Take the diagnostic, attempt stage gates, fill demonstrated gaps |

These are planning estimates, not measured completion times. Use the [study plan](docs/STUDY-PLAN.md) for separate integration, incident, and capstone budgets; the full route is not a guaranteed twelve-week finish.

## Commands

Quick reference for an existing setup. The local server stays running until Ctrl+C; do not start a second server on the same port. Run the lab commands in another terminal.

```sh
python3 academy.py local
python3 -m lab.cli demo
python3 -m lab.cli evaluate --split train
python3 -m lab.composed evaluate --components completed --split all
python3 -m unittest discover -s tests
python3 scripts/check_content.py
```

See [the lab manual](lab/README.md) for the exact harness commands and [maintenance](docs/MAINTENANCE.md) for builds, content conventions, and release checks.

## Learning rules

Save evidence, not just completion ticks. Make a prediction before every experiment. Keep at least one untouched evaluation split. Ask your AI tutor for hints before solutions. Every final claim about quality should point to a trace, a test, a dataset, or a human judgment with a rubric.

Course text and code are original educational material. External books, courses, and videos remain with their respective owners; the library links to authorized sources and does not bundle their content. See [reuse and attribution](docs/REUSE.md). This project does not claim university accreditation, vendor certification, or a validated commercial price.
