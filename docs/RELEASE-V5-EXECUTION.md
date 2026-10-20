# Version 5 fresh-source execution audit

Executed on 20 October 2026 on macOS. All expected exits and acceptance checks below passed.

This audit ran a separate copy of the intended downloadable source, selected with the exact `INCLUDE` and `EXCLUDE` rules from `scripts/package_project.py`. It was not a Git clone and did not reinstall the optional MCP environment. The copy contained **207 files** and excluded Git metadata, the original `work/` directory, runtime records, `dist/`, bytecode, and credentials.

## Isolation and provenance

Fresh source directory used:

```text
/var/folders/_f/93k1g0q55s9_cz6cky4sd6v80000gn/T/signal-desk-v5-fresh-20261020-qdp48slz/ai-engineering-academy
```

The source manifest was saved outside that copy, with SHA-256:

```text
8f92340d6283dd5bbcabed443167c706b1b7d061220996b4d81238fb529eb4a4
```

Each command ran with the fresh directory as its working directory and without inherited `PYTHONPATH`. Import checks printed fresh-copy paths for `lab`, the planner runtime, worker implementation, and MCP client. The MCP client's `ROOT` also resolved to the fresh copy, so the server subprocess used copied sources rather than the original checkout. On macOS, `/var` and `/private/var` spellings in those outputs refer to the same resolved location.

At the end of execution, all 207 manifest files remained byte-identical, and the corresponding source files in the original checkout had not changed since the snapshot. Test outputs were written only to fresh temporary/run directories. This report was added afterward; it is not part of that snapshot's 207-file count.

The optional interpreter was the existing `work/mcp-venv/bin/python` in the original checkout: **Python 3.12.14**, **mcp 1.30.0**. Only its installed runtime/dependencies were reused; imported project modules and server code came from the fresh copy.

## Executed checks

Run the following from a fresh source directory. In the table, `MCP_PYTHON` means the actual path to the interpreter from the optional MCP environment; it is not a command installed by this project.

| Check | Command | Observed result |
| --- | --- | --- |
| Core Python suite | `python3 -m unittest discover -s tests -v` | **165 discovered: 154 passed, 11 optional MCP skips**, Python 3.9.6 |
| Content and local links | `python3 scripts/check_content.py` | **24 lessons, 72 exercise workspaces, 15 lab guides**; applied checks, resource metadata, and file/section links passed |
| Portal unit suite | `node --test tests/test_portal.cjs` | **21 passed**, zero failures/skips |
| Complete reference composition | `python3 -m lab.composed evaluate --components completed --split all --out work/audit-composed` | **28/28 cases, 11/11 scenarios, 3/3 probes**; all eight student-hook boundaries exercised |
| Scripted planner | `python3 -m lab.planner_lab --out work/audit-planner` | Drafted; two proposals, one fixture lookup |
| Unimplemented student planner | `python3 -m lab.planner_lab --backend student --out work/audit-planner-student` | Expected exit **1**, `student_incomplete`, zero tool executions |
| Retrieval experiment | `python3 -m lab.practicum.retrieval --out work/audit-retrieval` | Twelve cases across three variants; macro recall **0.9 / 1.0 / 1.0** on the ten answerable cases |
| Scripted worker comparison | `python3 -m lab.practicum.workers --cases 8 --out work/audit-workers` | All **eight** paired comparisons and coordination gates passed |
| Review/recovery rehearsal | `python3 -m lab.practicum.review_queue rehearse --out work/audit-queue` | Stale approval and mismatched release rejected; pending work preserved; exactly one local effect after replay |
| Full optional-environment suite | `"$MCP_PYTHON" -m unittest discover -s tests -v` | **165 passed**, zero skips/failures |
| Actual MCP acceptance | `"$MCP_PYTHON" -m lab.mcp_lab --out work/audit-mcp` | **13/13** real SDK/stdio checks passed |
| Planner over actual MCP | `"$MCP_PYTHON" -m lab.planner_lab --lookup mcp --out work/audit-planner-mcp` | Drafted; two scripted proposals and one actual MCP lookup |

All commands exited zero except the deliberately incomplete student planner, which exited one as required. Its failure is a successful starter-state check, not completion of the student's exercise.

The worker regression suite additionally covers unordered result lists, conflicting duplicates, changed input identity, cancelled/partial/missing work, worker failure, timeout evidence, fabricated citations, and unexpected host-tool use. Queue tests include applying the same approved revision in separate processes and rejecting approval reuse after changes or release transitions.

## Evidence location and limits

The audit directory beside the fresh copy contains `source-manifest.json`, `execution-results.json`, and captured stdout/stderr for each command. These machine-local runtime logs are not bundled into the course. CLI reports remain under the fresh copy's `work/audit-*` directories.

No new paid or authenticated model run was needed for this repeat. Actual model-planner and assistant-host MCP evidence remains separately documented in [the planner evidence record](../lab/planner_lab/EVIDENCE.md). Fresh-copy scripted success must not be relabeled as new live-model evidence. Live Responses API execution remains pending without API credentials.

This audit establishes reproducible source execution with the stated runtimes. It does not establish learner mastery, completion of every open-ended exercise, semantic correctness for arbitrary generated text, a fresh dependency installation, Windows compatibility, or production readiness. Final PDF layout, browser interaction, owner-only hosting, and GitHub publication are separate release checks.
