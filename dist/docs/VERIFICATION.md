# Verification record for the October 2026 edition

The local course project was checked on 20 October 2026. These results describe this version and the included synthetic cases; they do not establish production readiness for a live provider or real customer data.

## Executable lab

`python3 -m unittest discover -s tests` passed 54 tests using Python 3.9.6. `python3 -m lab.cli evaluate --split all` passed 28 of 28 synthetic cases and 11 of 11 failure and recovery scenarios. The suite includes malformed inputs, authorization scope, idempotency, checkpoint validation, restored budgets, persistence failure, and the separate reference solutions for the eight student labs.

The unimplemented functions in `lab/student.py` are deliberate learner assignments. Their practice checks fail until you complete them. The reference implementation is complete and passes independently.

## Curriculum and resources

The content validator confirmed 24 unique lessons, eight stages with three lessons each, 72 lesson exercises, valid four-option quizzes, 43 unique external resource records, and resolving local Markdown links. The lesson text totals approximately 19,150 words before adding labs, articles, manuals, templates, and capstones.

External resource pages were checked against primary sources. YouTube titles and video IDs were verified through author or course pages; playback was not inspected. Resource access and provider interfaces may change after this edition.

## Learning portal

Headless Chrome checks passed for navigation, the skip link, lesson completion, quiz feedback, note persistence, resource search, saved resources, the deterministic harness simulator, progress export and import, mobile layout, and PDF/source downloads. Desktop, lesson, and mobile screenshots were visually reviewed.

Progress is stored locally in the browser. It is not an authenticated transcript or certification record. Export it for backup and transfer between local and hosted origins.

## PDF fieldbook

The generated fieldbook has 136 A4 pages and 57 outline entries. Automated inspection found no empty pages or text outside the page safety bounds. Representative cover, contents, prose, table, and code pages were rendered and visually inspected. It is a reading PDF, not a tagged accessible-PDF conformance claim; editable Markdown and the HTML portal are also included.

## Reproduce the checks

```sh
python3 -m unittest discover -s tests
python3 -m lab.cli evaluate --split all
python3 scripts/check_content.py
python3 scripts/build_portal.py
python3 scripts/package_project.py
```

Optional browser checks use Playwright through `scripts/test_portal.cjs` against a running local server. Set `ACADEMY_BROWSER_PATH` if using an installed Chrome executable. Optional PDF generation uses ReportLab through `scripts/build_book.py`; these authoring dependencies are not needed for the core lessons or Python lab.
