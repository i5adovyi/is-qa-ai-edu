# Verification record for the October 2026 edition

The local course project was checked on 20 October 2026. These results describe this version and the included synthetic cases; they do not establish production readiness for a live provider or real customer data.

## Executable lab

`python3 -m unittest discover -s tests` passed 66 tests using Python 3.9.6. `python3 -m lab.cli evaluate --split all` passed 28 of 28 synthetic cases and 11 of 11 failure and recovery scenarios. The suite includes malformed inputs, authorization scope, idempotency, checkpoint validation, restored budgets, persistence failure, trace metadata leakage, the separate reference solutions for the eight student labs, and eight model-bridge tests.

The unimplemented functions in `lab/student.py` are deliberate learner assignments. Their practice checks fail until you complete them. The reference implementation is complete and passes independently.

The new development sandbox was tested in a disposable copy: its five initial checks produce exactly one intended failure; the corrected copy passes all five. It is isolated from the reference implementation.

The manual model bridge was exercised through actual CLI export and replay commands for five training cases, using explicitly labeled deterministic mock responses. Four created one draft each; the injection case escalated without writes. No external model was invoked. These results establish the local replay path, not model performance or provider reliability.

## Curriculum and resources

The content validator confirmed 24 unique lessons, eight stages with three lessons each, 72 actual exercise sections, valid four-option quizzes, 43 unique external resource records, and resolving local Markdown file and section links. The lesson text totals 20,073 words before adding labs, articles, manuals, templates, and capstones.

The research source pack contains eight synthetic sources, six questions, and twelve labeled claim-source pairs; all referenced source IDs resolve. Its cost calculations use invented assumptions. All 24 quiz answers retain their original semantic meaning, with correct positions now balanced across the four options.

External resource pages were checked against primary sources. YouTube titles and video IDs were verified through author or course pages; playback was not inspected. Resource access and provider interfaces may change after this edition.

## Learning portal

Ten dependency-free Node regression tests pass. They cover solution assets and section targets, unsafe link rejection, malformed routes, long-note round trips, storage-failure export fallback, progress deduplication, conflicting imported notes, and keyboard-operable import.

Headless Chrome checks passed for navigation, the skip link, lesson completion, quiz feedback, note persistence, resource search, saved resources, the deterministic harness simulator, keyboard progress export/import, conflict preservation, solution links and section focus, malformed routes, mobile layout, and PDF/source downloads. Desktop, lesson, and mobile screenshots were visually reviewed.

A clean extracted source archive rebuilt its own portal and downloadable ZIP successfully. Portal builds now refresh the archive automatically.

Progress is stored locally in the browser. It is not an authenticated transcript or certification record. Export it for backup and transfer between local and hosted origins.

## PDF fieldbook

The regenerated fieldbook has 150 A4 pages and 62 outline entries. Automated inspection found no empty pages or text outside the page safety bounds. Representative cover, contents, practice-map table, model-bridge code, development fixture, research memo, and budget-lesson pages were rendered and visually inspected. It is a reading PDF, not a tagged accessible-PDF conformance claim; editable Markdown and the HTML portal are also included.

## Reproduce the checks

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 -m lab.cli evaluate --split all
python3 scripts/check_content.py
python3 scripts/build_portal.py
```

Optional browser checks use Playwright through `scripts/test_portal.cjs` against a running local server. Set `ACADEMY_BROWSER_PATH` if using an installed Chrome executable. Optional PDF generation uses ReportLab through `scripts/build_book.py`; these authoring dependencies are not needed for the core lessons or Python lab.
