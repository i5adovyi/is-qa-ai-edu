# Turn lessons into working practice

The course has three connected routes. **Concept practice** uses diagrams, contracts and manual simulations. **Engineering practice** implements local Python helpers and inspects a deterministic harness. **Model practice** captures actual assistant output and evaluates it through the [model bridge](../lab/model-bridge.md). Complete the model route when you have access to an assistant; keep it marked “not attempted” when you do not. An offline pass does not establish live-model performance.

## Prerequisites and placement

You do not need machine-learning mathematics or a paid API account. For the Python labs, you should be able to:

- Open a terminal at this project's root and run `python3 --version`.
- Read a Python function using lists, dictionaries, conditionals and imports.
- Read and edit JSON without changing its shape accidentally.
- Find a file from a printed path and distinguish a command's output from its exit status.
- Run a supplied `unittest` command and identify which assertion failed.

Check these by running `python3 -m lab.cli demo`, opening its `result.json`, and locating `classify` in `lab/policy.py`. Explain one branch in your own words. If that is difficult, start with the concept route and spend a preparation session on the [official Python tutorial](https://docs.python.org/3/tutorial/). Learn functions, data structures, modules, and reading/writing files before Lab 01. The course does not teach Python from zero.

Git is useful for preserving patches, but it is not required: keep before/after copies until you are comfortable with version control. Never overwrite the only copy of an experiment.

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
| 10 task design, 11 verification, 12 review | [Development sandbox](../content/dev-sandbox/README.md), copied to `work/router-practice/` | One original failure, narrow patch, five passing checks, mutant failures and reviewed diff |
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

## Evidence before completion

Use the [assessment manual](ASSESSMENT.md) for stage gates and the single capstone rubric. A quiz pass checks recall; an executable gate checks its stated contract; a reviewed artifact demonstrates the broader skill. Keep those records distinct.
