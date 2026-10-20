# From components to working integrations

Complete these three labs to connect the course's diagrams and helper functions to real execution. They address three different boundaries: protocol communication, host-discovered procedures, and control flow inside your own program.

| Lab | What actually runs | Prerequisites | Evidence |
| --- | --- | --- | --- |
| [09: Real MCP](../content/labs/09-real-mcp.md) | Separate MCP SDK client and server over local standard input/output | Lesson 08; Python version and isolated dependencies specified by the lab | Negotiated capabilities, request/result IDs, successful lookup and rejected/failing requests |
| [10: Installed skill](../content/labs/10-installed-skill.md) | A skill copied into a disposable project, then used in fresh Codex sessions | Lesson 09; basic Python; host access for behavioral testing | Installation manifest, discovered skill, generated artifact, trigger/non-trigger and missing-reference observations |
| [11: Complete student harness](../content/labs/11-complete-student-harness.md) | Eight student components connected to the checkpointed workflow | Labs 01–08; lessons 13–18 | Component calls, source identity, evaluation, budget stops, crash/resume behavior and one-effect replay |

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
