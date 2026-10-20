# Start learning AI engineering

You will build a small system that reads a synthetic support ticket, retrieves relevant policy, proposes an action, and records enough evidence for someone else to review it. By the end, you should be able to explain why an agent succeeded, why it failed, and which change would improve it. That ability is more durable than memorizing a particular model's interface.

Start with the [beginner preparation module](../content/onboarding/README.md). Its independent entry checks teach diagram notation, distinguish model proposals from observed outcomes, and offer a runnable Python/terminal worksheet for the coding route. You can begin lesson 01 on paper without installing anything. Then use the [prerequisites and practice map](PRACTICE-MAP.md) to choose concept, local engineering, or live-model practice. Keep manual, scripted, replayed, and actual model results labeled separately.

After the foundations, the [integration route](INTEGRATION-LABS.md) adds a real local MCP exchange, skill installation and fresh-host testing, and a complete student harness. It explains which setup and evidence each requires.

If you have just cloned or downloaded the project, complete [fresh-copy setup](SETUP.md) first. It explains the working directory, Python versions, expected failures, local server, and progress backups.

## Your first session: one small artifact

Complete entry check A, then begin [lesson 01's first checkpoint](../content/lessons/01-systems-before-agents.md#exercise-1--guided-map). Draw only one relationship. Explain it, get feedback, and add its data label. Save that attempt before expanding the diagram. The [blank worksheet](../templates/first-diagram.md) gives you a starting shape without the target solution.

Use the portal exercise workspace or [attempt record](../templates/exercise-attempt.md) to keep your original attempt, requested hint level, feedback, and revision. A tutor packet contains the exercise, criteria, current checkpoint, and your work; instructor solutions are excluded. Ask for one small hint when needed. There is no required period of struggling before asking.

The lesson's timing separates reading, guided practice, independent work, and optional extensions. These are provisional planning estimates. Record actual time and help in the [pacing log](../templates/pacing-log.md); adjust your next session based on what happened.

## A 90-minute engineering orientation

This optional session assumes the terminal entry check is already comfortable. It is not required before the first diagram.

**Minutes 0-15: get something running.** From this project directory, run `python3 -m lab.cli demo`. Read the output, locate its trace, and identify a decision, a tool call, and a result. If Python is missing, you can still read the entire curriculum in the portal or Markdown files; install Python before the executable labs.

**Minutes 15-30: establish your baseline.** Without an AI assistant, explain the difference between a prompt, context, tool, skill, workflow, agent, and harness. Use the glossary if you get stuck, but mark which explanations required help. Save your baseline in `work/baseline.md` after creating the `work/` directory.

**Minutes 30-55: take lesson 01.** Do its guided exercise before reading the solution. Write your predicted answer, your actual result, and one difference. A beautiful answer that you cannot verify is not a passing result.

**Minutes 55-75: create your learning log.** Create `work/experiments/`, then copy `templates/experiment-log.md` into `work/experiments/first-run.md`. Record the input, instructions, tool choices, and result. If using a model, also record the provider, model identifier as shown by the product, date, and relevant settings. Never record a key or token.

**Minutes 75-90: explain the result.** Give yourself a two-minute oral explanation. Could a teammate reproduce your experiment from the log? If not, fix the log before moving on.

## Use your final subscription day well

Spend available access on preparing reusable learning assets and practicing high-feedback tasks. Try one lesson, ask for a critique of your attempted solution, and save both your work and the critique locally. Try one context-compression experiment and one adversarial tool-use exercise. End by writing a personal study plan and exporting your portal progress. Do not spend the entire day collecting hundreds of prompts that you have never tested.

A chat subscription and API billing may have separate terms. This curriculum makes no promise that a subscription includes API credits. The core labs run offline. Optional live-model work is something you enable separately, with your own limits.

## The study loop

1. **Predict:** write what should happen and why.
2. **Attempt:** produce the smallest useful artifact before requesting a solution. Ask for a targeted hint whenever you need one.
3. **Observe:** capture an output, trace, or failed assertion.
4. **Diagnose:** name the layer responsible: task, context, model decision, tool, harness, or evaluator.
5. **Change one thing:** preserve the previous version for comparison.
6. **Explain:** summarize the evidence and remaining uncertainty.

An AI tutor can support each step. It should not erase the effort that teaches you. Use [the tutor prompt](../templates/tutor-prompt.md) to keep it in coaching mode.

## Diagnostic and placement

Attempt these six tasks with a 45-minute total timebox. Score each 0 for no usable artifact, 1 for a plausible artifact with gaps, and 2 for an artifact supported by a reproducible check.

- Turn “make our support better” into a task with inputs, outputs, constraints, and acceptance tests.
- Identify an instruction embedded in retrieved customer text and explain why it cannot authorize an action.
- Design a tool schema for creating a draft reply, including one rejected input.
- Describe what happens when a tool times out after its side effect already succeeded.
- Build five evaluation cases that distinguish a useful agent from a keyword shortcut.
- Compare single-agent and multi-agent execution using quality, latency, and cost evidence.

Score 0-4: begin at stage 1. Score 5-8: read stages 1-2 quickly but attempt their gates. Score 9-12: start with the lab and stage gates; return to lessons whenever you cannot defend an answer. This is a placement aid, not a validated psychometric test.

## When a stage is complete

A completion tick records your judgment. Passing a quiz checks a small concept; it does not prove practical mastery. Pass a stage only when the stage artifact can be reproduced, its required checks pass, and you can discuss at least one failure case without an assistant. Use the assessment manual for the detailed rubric.

## If you feel overwhelmed

Follow one path: lesson 01, lesson 02, lesson 03, lab 01. Keep a single experiment log. Defer optional readings. Spend 25 minutes making one small result more trustworthy. The curriculum is a library of practice opportunities; you do not need to consume every resource before building.
