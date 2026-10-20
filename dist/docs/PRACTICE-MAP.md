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
| 08 MCP | Three message fixtures and responsibility diagram | Request/result matching and unresolved outcomes; explicitly a simulator |
| 09 skills | Complete `SKILL.md`, reference and template in `work/skills/` | Three drafts, trigger/non-trigger table and missing-dependency behavior |
| 10 task design, 11 verification, 12 review | [Development sandbox](../content/dev-sandbox/README.md), copied to `work/router-practice/` | One original failure, narrow patch, five passing checks, mutant failures and reviewed diff |
| 13 loop, 14 recovery | Reference traces, [Lab 04](../content/labs/04-retries-and-budgets.md) schedule helper and [Lab 05](../content/labs/05-idempotency-and-recovery.md) key helper | Success, exhausted budget, interrupted write and one-effect replay |
| 15 observability | Ten scripted traces, cost ledger, [Lab 07](../content/labs/07-traces-and-diagnosis.md) summary helper | Step/time stops, explicit cost reservations, complete event accounting |
| 16 datasets, 17 graders, 18 release | [Lab 06](../content/labs/06-grounding-and-evaluation.md); authored rubric and cases | Frozen split, false acceptance/rejection counts, hard-gate decision |
| 19 delegation, 20 coordination, 21 comparison | Two worker folders and one integration folder | Versions, stale/duplicate result handling, same-case baseline comparison |
| 22 production, 23 incidents | Service contract and local rollback rehearsal | Explicit denominators, preserved pending work, incident regression |
| 24 capstone clinic | Select [support](../capstones/01-support-agent.md), [QA](../capstones/02-qa-copilot.md) or [research](../capstones/03-research-workflow.md); [Lab 08](../content/labs/08-ship-an-evaluated-policy.md) for the support route | Proposal during the clinic; project evidence and common 40-point defense across weeks 10–12 |

## What the executable labs actually connect

Labs 01–07 are isolated helper exercises in `lab/student.py`. Their `practice` checks execute those functions, but editing them does **not** change the reference harness's context packing, permissions, backoff, storage or traces. Lab 08 connects only `build_decision` through `evaluate --policy student`. The reference harness has its own implementations of its controls.

Use two separate evidence claims: “my helper meets this contract” and “the reference run demonstrates this control.” Do not claim your helper caused a reference-run improvement. Integration is additional engineering work: add an explicit injection point, prove that the selected helper was called, compare its behavior with the original, then check the same failure scenarios. Preserve the reference path and declare which candidate was evaluated.

The [model bridge](../lab/model-bridge.md) addresses a different boundary: supplying captured or generated model decisions to the harness. It does not automatically integrate every helper or create a model-controlled tool-planning loop.

## Operational MCP and skills extensions

The course currently supplies an MCP-shaped simulation, not an installed MCP server. It supplies a skill-authoring exercise, not a verified installation for every assistant host. These are recommended next practical extensions after stage 3:

**MCP extension:** use the [official architecture guide](https://modelcontextprotocol.io/docs/learn/architecture) to choose a current SDK and supported local transport. Pin the SDK version; implement one read-only synthetic knowledge lookup; start a client and server; save initialization/capability, tool-list and tool-call evidence. Verify unknown-tool, malformed-argument, no-result and server-disconnect behavior. Pass only when another learner can run your documented command and match each accepted request to its result. No paid model is needed to test that protocol boundary. Keep the existing teaching simulator labeled accurately.

**Skill extension:** choose one host you actually use and consult its current official skill-installation documentation. Install only your synthetic draft skill in the host's documented project or user location. Start a fresh session with no prior solution context. Capture one triggered run, one non-trigger request, and one missing-reference failure; record host version, discovered skill name, files used and saved artifact. A manually read folder proves procedural clarity; successful discovery and execution in a host proves that particular integration.

If either extension cannot run, preserve its design and mark operational verification pending. Do not award an integration pass from a diagram or the existence of a folder.

## Evidence before completion

Use the [assessment manual](ASSESSMENT.md) for stage gates and the single capstone rubric. A quiz pass checks recall; an executable gate checks its stated contract; a reviewed artifact demonstrates the broader skill. Keep those records distinct.
