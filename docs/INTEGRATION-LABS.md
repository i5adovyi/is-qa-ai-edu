# From components to working integrations

Complete these three labs to connect the course's diagrams and helper functions to real execution. They address three different boundaries: protocol communication, host-discovered procedures, and control flow inside your own program.

| Lab | What actually runs | Prerequisites | Evidence |
| --- | --- | --- | --- |
| [09: Real MCP](../content/labs/09-real-mcp.md) | Separate MCP SDK client and server over local standard input/output | Lesson 08; Python version and isolated dependencies specified by the lab | Negotiated capabilities, request/result IDs, successful lookup and rejected/failing requests |
| [10: Installed skill](../content/labs/10-installed-skill.md) | A skill copied into a disposable project, then used in fresh Codex sessions | Lesson 09; basic Python; host access for behavioral testing | Installation manifest, discovered skill, generated artifact, trigger/non-trigger and missing-reference observations |
| [11: Complete student harness](../content/labs/11-complete-student-harness.md) | Eight student components connected to the checkpointed workflow | Labs 01–08; lessons 13–18 | Component calls, source identity, evaluation, budget stops, crash/resume behavior and one-effect replay |

Then choose the extensions matching the skill you need to demonstrate:

| Lab | When to take it | What to prove |
| --- | --- | --- |
| [12: Model-directed tool loop](../content/labs/12-model-tool-loop.md) | After lessons 08 and 13–15 | Scripted planner controls; optional actual model→MCP→observation→model execution and direct host integration |
| [13: Coding and workers](../content/labs/13-coding-and-workers.md) | Coding mission after lessons 10–12; worker comparison after 19–21 | Reproduced bug, reviewed Git change, fresh-session handoff, single/team comparisons, coordination faults |
| [14: Retrieval comparison](../content/labs/14-retrieval-comparison.md) | After lessons 05 and 16–17 | Version-aware lexical/hybrid retrieval, separate claim support, changed cases and limitations |
| [15: Review and operations](../content/labs/15-review-and-operations.md) | After lessons 14 and 22–23 | Exact-revision review, stale-approval rejection, preserved pending work, CI and rollback |

Reserve another 7–12 hours for these extensions, and use the study plan's longer route rather than squeezing them into the original 72-hour schedule. A scripted process worker is not an AI agent. A fake provider test is not a live call. Every extension names its own evidence boundary.

The MCP lab uses an official SDK in an isolated environment. It requires package installation but no model or provider account. The skill installer and composed harness retain the standard-library Python route. The portal remains a reading and progress interface; run the commands locally after downloading or cloning the project.

## Sequence and time

Take lab 09 after lesson 08 and lab 10 after lesson 09. Use each to challenge the simpler conceptual exercises: which assumptions only became visible when a real process or fresh host was involved?

Start lab 11 after implementing the first eight helpers. Run the supplied completed example to understand the artifacts, then use your own component profile. Keep those reports separate: a successful example is a baseline, not evidence that your unfinished functions work.

Reserve roughly 5–9 additional focused hours across the three labs. These are planning estimates. Extend the study schedule if environment setup or debugging takes longer; do not rush the capstone to fit a page's estimate.

## A shared evidence packet

For each lab, preserve the exact command, software versions, input files, output report, a predicted failure, the observed failure, and your explanation of the enforcing layer. Retain first attempts and repaired attempts separately.

Use this vocabulary precisely:

- **Installed:** files exist in the intended host discovery location.
- **Discovered:** a fresh host exposed or selected the skill.
- **Executed:** the expected procedure ran and produced inspectable artifacts.
- **Protocol verified:** a real MCP client and server exchanged the tested requests.
- **Component integrated:** the selected helper was invoked in the composed run and its result affected behavior.
- **Evaluated:** a declared set of cases and failure scenarios was checked with stated acceptance rules.

A filesystem validator cannot establish host discovery. A correct protocol result does not establish answer quality. A reference run cannot establish that student code was called. A test result is limited to its observed inputs and environment.

## Defense questions

1. Which result would change if the MCP server stopped responding?
2. How did you distinguish a skill being installed from a skill being used?
3. Which component supplied the retry delay, selected evidence, and operation key in your run?
4. What prevents a permissive student helper from expanding the host's write permissions?
5. Why should changing a component between a crash and resume require a fresh run?
6. Which claims still require live-model measurements rather than local deterministic evidence?

Use the [assessment manual](ASSESSMENT.md) for scoring and the [verification record](VERIFICATION.md) for this edition's executed checks.
