# Verification record for the October 2026 edition

The local course project was checked on 20 October 2026. These results describe this version and the included synthetic cases; they do not establish production readiness for a live provider or real customer data.

## Executable lab

`python3 -m unittest discover -s tests` passed 100 tests using Python 3.9.6 and explicitly skipped ten optional MCP tests. Running the complete suite with the pinned MCP environment on Python 3.12.14 passed **all 110 tests, with no skips**. `pip check` reported no broken requirements.

`python3 -m lab.cli evaluate --split all` passed 28 of 28 synthetic cases and 11 of 11 failure and recovery scenarios. The suite includes malformed inputs, authorization scope, idempotency, checkpoint validation, restored budgets, persistence failure, trace metadata leakage, the separate reference solutions for the eight component labs, and eight model-bridge tests.

The unimplemented functions in `lab/student.py` are deliberate learner assignments. Their practice checks fail until you complete them. The reference implementation is complete and passes independently.

The new development sandbox was tested in a disposable copy: its five initial checks produce exactly one intended failure; the corrected copy passes all five. It is isolated from the reference implementation.

The manual model bridge was exercised through actual CLI export and replay commands for five training cases, using explicitly labeled deterministic mock responses. Four created one draft each; the injection case escalated without writes. No external model was invoked. These results establish the local replay path, not model performance or provider reliability.

## Complete student harness

The `lab.composed` completed profile passed **28/28 cases, 11/11 failure scenarios, three integration probes, and all eight component gates**, with all eight component hooks observed. The probes cover redaction reaching the policy, context selection changing its evidence, and rejection when packing would hide a conflicting retrieved answer. The untouched student profile fails intentionally and uses no reference fallback.

Twenty-one integration tests verify actual helper effects, retained host boundaries, source/profile/context identity, crash recovery, and budgets. Cross-review reproduced and repaired a conflict-hiding defect before release. These are deterministic workflow results, not measurements of a live agent model.

## Real MCP and installed skill

The official `mcp==1.30.0` SDK client and server passed **13/13 checks over real subprocess stdio**. Ten optional integration tests passed, including deadlines, disconnects, schema errors, stdout contamination, import behavior, and evidence preservation for malformed learner outputs. The tool-extension baseline failed as expected at 13/16; the completed extension passed 16/16. A changed corpus also verified derived topic behavior. Setup and platform scope are in the [MCP manual](../lab/mcp_lab/README.md).

Thirteen deterministic tests check the skill installer and structural contracts. Fresh Codex CLI sessions demonstrated implicit skill discovery/use, an unrelated request without activation, and missing-reference blocking without a review artifact. The final trigger produced a real review matching all three known fixture verdicts and passing the packaged validator. The recorded package/output hashes match the distributed files. See [host evidence](../content/skill-practice/HOST-EVIDENCE.md) for exact software identity, excerpts, and limits; this small host trial is not a general activation benchmark.

## Curriculum and resources

The content validator confirmed 24 unique lessons, eight stages with three lessons each, 72 actual lesson exercise sections, eleven numbered lab guides, valid four-option quizzes, 43 unique external resource records, and resolving local Markdown file and section links. The lesson text totals 20,446 words before adding labs, articles, manuals, templates, and capstones.

The research source pack contains eight synthetic sources, six questions, and twelve labeled claim-source pairs; all referenced source IDs resolve. Its cost calculations use invented assumptions. All 24 quiz answers retain their original semantic meaning, with correct positions now balanced across the four options.

External resource pages were checked against primary sources. YouTube titles and video IDs were verified through author or course pages; playback was not inspected. Resource access and provider interfaces may change after this edition.

## Learning portal

Ten dependency-free Node regression tests pass. They cover solution assets and section targets, unsafe link rejection, malformed routes, long-note round trips, storage-failure export fallback, progress deduplication, conflicting imported notes, and keyboard-operable import.

Headless Chrome checks passed for navigation, the skip link, lesson completion, quiz feedback, note persistence, resource search, saved resources, the deterministic harness simulator, keyboard progress export/import, conflict preservation, solution links and section focus, malformed routes, mobile layout, and PDF/source downloads. The expanded checks verify all eleven lab cards, the three new guides, and downloadable MCP/skill/composition code. Desktop, lesson, integration-guide, and mobile screenshots were visually reviewed.

A clean extracted source archive rebuilt its own portal and downloadable ZIP successfully. Portal builds now refresh the archive automatically.

Progress is stored locally in the browser. It is not an authenticated transcript or certification record. Export it for backup and transfer between local and hosted origins.

## PDF fieldbook

The regenerated fieldbook has 168 A4 pages and 69 outline entries. Automated inspection found no empty pages or text outside the page safety bounds. Representative cover, contents, integration route, new lab instructions, command blocks, MCP manual, solution guidance, and recorded skill evidence were rendered and visually inspected. It is a reading PDF, not a tagged accessible-PDF conformance claim; editable Markdown and the HTML portal are also included.

## Reproduce the checks

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 -m lab.cli evaluate --split all
python3 -m lab.composed evaluate --components completed --split all
python3 scripts/check_content.py
python3 scripts/build_portal.py
```

After the isolated setup from lab 09, run the entire Python suite and the real MCP gate with that environment:

```sh
work/mcp-venv/bin/python -m unittest discover -s tests
work/mcp-venv/bin/python -m lab.mcp_lab --out work/mcp-new-verification
```

Optional browser checks use Playwright through `scripts/test_portal.cjs` against a running local server. Set `ACADEMY_BROWSER_PATH` if using an installed Chrome executable. Optional PDF generation uses ReportLab through `scripts/build_book.py`; these authoring dependencies are not needed for the core lessons or Python lab.
