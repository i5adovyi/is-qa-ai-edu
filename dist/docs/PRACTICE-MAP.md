# Turn lessons into working practice

> For the guided SDET reading route, use [Start here](START-HERE.md). This page is for local setup or optional practical work; its exercises and checks are not required before reading.

The course has three connected routes. **Concept practice** uses diagrams, contracts and manual simulations. **Engineering practice** implements local Python helpers and inspects a deterministic harness. **Model practice** captures actual assistant output and evaluates it through the [model bridge](../lab/model-bridge.md). Complete the model route when you have access to an assistant; keep it marked “not attempted” when you do not. An offline pass does not establish live-model performance.

## Prerequisites and placement

Start with the [three independent beginner entry checks](../content/onboarding/README.md). Diagram notation and proposal-versus-outcome reasoning are enough to begin the concept route. The terminal check creates a disposable input, a generated result, and an intentional failed assertion; it includes a catch-up worksheet.

You do not need machine-learning mathematics or a paid API account. For the Python labs, you should be able to:

- Open a terminal at this project's root and run `python3 --version`.
- Read a Python function using lists, dictionaries, conditionals and imports.
- Read and edit JSON without changing its shape accidentally.
- Find a file from a printed path and distinguish a command's output from its exit status.
- Run a supplied `unittest` command and identify which assertion failed.

Check these by running `python3 -m lab.cli demo`, opening its `result.json`, and locating `classify` in `lab/policy.py`. Explain one branch in your own words. If that is difficult, start with the concept route and spend a preparation session on the [official Python tutorial](https://docs.python.org/3/tutorial/). Learn functions, data structures, modules, and reading/writing files before Lab 01. The course does not teach Python from zero.

Git is useful for preserving patches, but it is not required: keep before/after copies until you are comfortable with version control. Never overwrite the only copy of an experiment.

Before external APIs or the advanced coding practicum, use the [future-project readiness checks](FUTURE-PROJECT-READINESS.md). They cover Git, JSON/API errors, isolated environments, migration comparisons, and learning from new data. They are placed where needed rather than added as prerequisites to lesson 01.

## Follow the lesson-to-practice map

All paths below start at the project root. Save learner artifacts under `work/`; the lab manual's older `my-work/` convention is also valid if used consistently.

| Lessons | Build or inspect | Completion evidence |
| --- | --- | --- |
| 01 systems, 02 contracts | Five-ticket baseline; contrastive task contracts | Inputs, expected decisions, permitted actions and unsupported claims |
| 03 prompt experiments | Paired experiment; [model bridge](../lab/model-bridge.md) when accessible | Separate development/final cases, raw outputs, scores; mark simulation versus live output |
| 04 packets, 05 retrieval | Own eight-note corpus; [Lab 02](../content/labs/02-context-budgets.md) packing helper | Recall calculation, source applicability and compression-loss ledger |
| 06 memory | Handoff and memory ledger; preview [Lab 05](../content/labs/05-idempotency-and-recovery.md) recovery | Resume from artifact evidence; detect stale completion claims |
| 07 tools | [Lab 01](../content/labs/01-data-boundaries.md) data helper and [Lab 03](../content/labs/03-tool-authority.md) permission helper | Invalid and cross-scope arguments rejected; limits of the helper explained |
| 08 MCP | Message fixtures, then [Lab 09](../content/labs/09-real-mcp.md) SDK client/server | Real initialization, capability listing, request/result matching, invalid calls and disconnects |
| 09 skills | Author a skill, then [Lab 10](../content/labs/10-installed-skill.md) installation and fresh-host practice | Separate installation, discovery and execution evidence; trigger/non-trigger and missing-reference behavior |
| 10 task design, 11 verification, 12 review | [Development sandbox](../content/dev-sandbox/README.md), copied to `work/router-practice/`; Lab 13 Part A can follow here | One original failure, narrow patch, five passing checks, mutant failures and reviewed diff |
| 13 loop, 14 recovery | Reference traces, [Lab 04](../content/labs/04-retries-and-budgets.md) schedule helper and [Lab 05](../content/labs/05-idempotency-and-recovery.md) key helper | Success, exhausted budget, interrupted write and one-effect replay |
| 15 observability | Ten scripted traces, cost ledger, [Lab 07](../content/labs/07-traces-and-diagnosis.md) summary helper | Step/time stops, explicit cost reservations, complete event accounting |
| 16 datasets, 17 graders, 18 release | [Lab 06](../content/labs/06-grounding-and-evaluation.md); authored rubric and cases | Frozen split, false acceptance/rejection counts, hard-gate decision |
| 19 delegation, 20 coordination, 21 comparison | Two worker folders and one integration folder | Versions, stale/duplicate result handling, same-case baseline comparison |
| 22 production, 23 incidents | Service contract and local rollback rehearsal | Explicit denominators, preserved pending work, incident regression |
| 24 capstone clinic | Select [support](../capstones/01-support-agent.md), [QA](../capstones/02-qa-copilot.md) or [research](../capstones/03-research-workflow.md); [Lab 08](../content/labs/08-ship-an-evaluated-policy.md) for the support route | Proposal during the clinic; [Lab 11](../content/labs/11-complete-student-harness.md) for full component integration; project evidence and common 40-point defense across weeks 10–12 |

## What the executable labs actually connect

Labs 01–07 first teach isolated helpers in `lab/student.py`. Their `practice` checks execute those functions. The ordinary reference command, `python3 -m lab.cli demo`, continues to use the preserved reference implementations. Lab 08's `evaluate --policy student` injects the decision function only.

[Lab 11](../content/labs/11-complete-student-harness.md) supplies the complete integration route. Its composed runner selects either your student components or a clearly labeled completed example. All eight functions participate in execution, and component evidence records which code ran. The completion gate includes helper contracts, task cases, failure scenarios and targeted integration probes. A blank student profile is supposed to fail; the completed example is for comparison.

The host retains mandatory schema, scope, approval and budget checks. The read-permission exercise does not silently become authority over every tool. Component identity is preserved across checkpoints so changing the selected code cannot masquerade as resuming the same experiment. Read the lab's seam table to distinguish student behavior from host enforcement.

The [model bridge](../lab/model-bridge.md) remains a separate route for replaying a saved model decision. A composed deterministic harness is not a live model or a model-selected tool loop. Combine claims only when you actually ran the corresponding integration.

## Real MCP and installed skills

[Lab 09](../content/labs/09-real-mcp.md) uses a pinned official MCP SDK with a real local client and server. The guide includes its Python requirement, isolated installation, request/result evidence, negative cases and failure handling. It makes no model calls. The earlier conceptual simulator remains useful for understanding message ownership, but it is no longer the only protocol exercise.

[Lab 10](../content/labs/10-installed-skill.md) installs the supplied skill into a disposable repository workspace. It separates deterministic package checks from fresh-host discovery and behavior. Use the documented host procedure to capture triggered use, a non-trigger request and a missing-reference failure. Host access and authentication are required for that behavioral portion; do not award a host-integration pass merely because a folder validator passed.

The [integration route](INTEGRATION-LABS.md) gives the sequence, additional time budget and common evidence packet. This edition's actual SDK and host checks are recorded in [verification](VERIFICATION.md).

## Added practice, without changing the original exercises

Use [starter fixtures](../content/practice/README.md) before authoring new cases for lessons 05, 16, 17, and 21. Keep the supplied practice examples separate from your own final evaluation split. Use [applied checks and calibration](../content/assessment/README.md) after each lesson and one [new-domain transfer](../content/assessment/transfer-and-retention.md) at each stage gate.

| Extension | Prerequisites | Evidence and remaining boundary |
| --- | --- | --- |
| [Lab 12: model/tool loop](../content/labs/12-model-tool-loop.md) | Lessons 07–09 and 13–16; completed lab 11 component gate; lab 09 for actual MCP | Scripted action/observation loop first; optional actual model decision, MCP execution, observation, and subsequent model decision |
| [Lab 13: coding and workers](../content/labs/13-coding-and-workers.md) | Lessons 10–12; lessons 19–21 for the worker comparison; Git | Original failure, scoped patch, commit/revert/resume; isolated worker outputs, stale/duplicate handling, and all parent/worker effort |
| [Lab 14: retrieval comparison](../content/labs/14-retrieval-comparison.md) | Lessons 04–05 and 16–17 | Same-case recall/support comparison; applicability and source-refresh errors separated from generation |
| [Lab 15: review and operations](../content/labs/15-review-and-operations.md) | Lessons 14 and 22–23 | Exact-version human review, stale-approval rejection, persisted pending work, release checks, and rollback |

These extensions add sessions; the [study plan](PRACTICE-STUDY-PLAN.md) budgets them explicitly. A process-based worker run establishes process coordination; a scripted planner run establishes the loop boundary. Neither establishes unexecuted live-model behavior.

## Investigate unfamiliar incidents

After the component exercises, use the [incident route](../content/incidents/README.md). Each case supplies a neutral brief, a disposable workspace, deterministic evidence and a deliberately incomplete decision function. Preserve the initial state and save a hypothesis, observation and next check before requesting hints or a debrief. The portal and CLI keep separate attempt records.

| Incident | Prerequisites | Evidence added to your dossier |
| --- | --- | --- |
| [INC-01](../content/incidents/01-morning-change.md) | Lessons 10–12 and Lab 13 Part A; Git | Working-tree baseline, scoped change, current test evidence, preserved human work |
| [INC-03](../content/incidents/03-interrupted-update.md) | Lessons 13–15 and Lab 05 | Cross-system timeline, recovery proposal, replay observations, explicit unknowns |
| [INC-04](../content/incidents/04-monday-workspace.md) | Lessons 07–09 and 13–15; revisit Lab 10 | Current scope, environment comparison, boundary checks, narrow authorization or compatibility decision |
| [INC-02](../content/incidents/02-evidence-brief.md) | Lessons 04–05 and 16–18 | Claim-to-evidence ledger, completeness and interpretation checks, comparable evaluation conditions |
| [INC-05](../content/incidents/05-busy-afternoon.md) | Lessons 14–15 and 19–21 and Lab 13 Part B | Whole-run accounting, bounded scheduling, state-conflict handling and pending work |
| [INC-06](../content/incidents/06-resumed-delivery.md) | Lessons 06, 12, 20 and 22–23 | Current acceptance brief, precise clarification, artifact-version comparison and usefulness review |
| [INC-CAPSTONE](../content/incidents/07-release-rehearsal.md) | Working baseline for one chosen capstone | Unfamiliar incident defense, persisted-state recovery evidence and a fresh project-specific regression |

The route adds 10.5–14.5 planning hours, including the capstone incident. The [study plan](PRACTICE-STUDY-PLAN.md) explains where it fits and how to avoid double-counting capstone hardening time. Each case has a transfer variant; record a prediction before running it. The [incident rubric](../content/incidents/ASSESSMENT.md) assesses reasoning, evidence and recovery separately from the executable contract. Use the existing 40-point rubric for the single capstone.

## Evidence before completion

Use the [assessment manual](ASSESSMENT.md) for stage gates and the single capstone rubric. A quiz pass checks recall; an executable gate checks its stated contract; a reviewed artifact demonstrates the broader skill. Keep those records distinct.
