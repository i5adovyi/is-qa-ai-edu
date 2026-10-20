# AI Engineering Academy

A practical training project for learning to design, build, test, and operate AI-assisted workflows. The shared case study is **Signal Desk**, a fictional support and QA team. You progress from writing precise requests to constructing an observable agent harness and defending its behavior with evidence.

## Start here

1. Read [START HERE](docs/START-HERE.md), including the first 90-minute session.
2. Run `python3 scripts/build_portal.py` to rebuild the learning portal.
3. Run `python3 scripts/serve.py` and open **http://127.0.0.1:8765**.
4. In another terminal, run `python3 -m lab.cli demo`.
5. Run `python3 -m unittest discover -s tests` to check the reference implementation.

Python 3.9+ is supported (tested here with Python 3.9.6). The portal builder and reference lab use the standard library; no package install, model subscription, or API key is needed. The bundled lab policy is deterministic and is explicitly not an LLM. Bring a model of your choice for the optional model experiments.

## What is inside

- Eight stages and 24 lessons, each with teaching material, a worked example, three exercises, hints, solution guidance, and a knowledge check.
- Eleven lab guides: eight component exercises plus a real MCP integration, host-installed skill practice, and a complete composed student harness.
- Original articles, learner manuals, reusable engineering templates, and three substantial capstone briefs.
- A curated library of courses, books, documentation, papers, and videos, with practical follow-up tasks.
- A local learning portal with search, quizzes, progress, personal notes, bookmarks, and JSON progress export/import.
- An original PDF fieldbook and a downloadable source archive.

See the [practice map](docs/PRACTICE-MAP.md) for prerequisites and lesson-to-lab links. To try your current chat model without an API integration, follow the [model response bridge](lab/model-bridge.md).

After the component exercises, follow the [integration route](docs/INTEGRATION-LABS.md). It connects protocol behavior, installed skills, and your own harness components to observable results.

The [second review report](docs/REVIEW-2026-10-20.md) records the earlier findings and their resolution. The [verification record](docs/VERIFICATION.md) states exactly what was run.

## Choose a pace

| Route | Suggested cadence | Outcome |
| --- | --- | --- |
| Foundations | 4 weeks, 4-6 hours/week | Complete stages 1-3 and the first two labs |
| Builder | 12 weeks, 6-8 hours/week | Complete all lessons, labs, and one capstone |
| Intensive | 6 weeks, 12-16 hours/week | Same work, with two review sessions per week |
| Practitioner | Self-paced | Take the diagnostic, attempt stage gates, fill demonstrated gaps |

These are planning estimates, not measured completion times. Readings and extensions can add substantial time.

## Commands

```sh
python3 scripts/build_portal.py
python3 scripts/serve.py
python3 -m lab.cli demo
python3 -m lab.cli evaluate --split holdout
python3 -m lab.composed evaluate --components completed --split all
python3 -m unittest discover -s tests
python3 scripts/check_content.py
```

See [the lab manual](lab/README.md) for the exact harness commands and [maintenance](docs/MAINTENANCE.md) for builds, content conventions, and release checks.

## Learning rules

Save evidence, not just completion ticks. Make a prediction before every experiment. Keep at least one untouched evaluation split. Ask your AI tutor for hints before solutions. Every final claim about quality should point to a trace, a test, a dataset, or a human judgment with a rubric.

Course text and code are original educational material. External books, courses, and videos remain with their respective owners; the library links to authorized sources and does not bundle their content. See [reuse and attribution](docs/REUSE.md). This project does not claim university accreditation, vendor certification, or a validated commercial price.
