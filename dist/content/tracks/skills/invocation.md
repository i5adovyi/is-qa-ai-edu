# Invocation, discovery and skill conflicts

## Start here

Finish the installation topic first, or use this page as a conceptual walkthrough without running anything. **Invocation** means selecting a skill for use. You can select one explicitly, or a host may select it from the task description. These are separate behaviors worth testing. Open the disposable workspace from the previous topic using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), not the academy's original skill source folder.

## The idea in plain language

**Discovery** means the host knows a skill exists. **Activation** means the host chooses and loads it for a task. **Execution** is the subsequent behavior, which may include reading references or calling tools. A final answer saying “I used the skill” is weaker evidence than visible reads and an output that follows its contract.

An explicit invocation removes some selection ambiguity. Codex supports mentioning a skill with `$skill-name`; local Claude Code supports `/skill-name`. Automatic selection instead depends on the description and the task. A broad description can trigger for unrelated work; a narrow or unclear one can miss legitimate requests. Host-specific invocation controls and naming rules can also affect selection.

**Name collisions** happen when several installed skills share a name or similar purpose. Different hosts resolve them differently. Do not guess which copy ran. Inspect the resolved path or visible selection and use unambiguous names in your own packages. A personal copy can behave differently from a project copy even if you edited only the latter.

## A small example

Signal Desk installs a synthetic failure-triage skill. “Use this skill to inspect the supplied failure” is an explicit-selection test. “Help me understand this timeout” is an automatic-selection candidate. “Explain what a test fixture is” is a related topic that may not need the workflow at all.

If explicit invocation succeeds but automatic selection fails, the package may be usable while its description needs improvement. Do not erase the failure or declare all activation correct. If the output is wrong after correct selection, investigate procedure or evidence handling rather than changing the name blindly.

## Try it with Codex or Claude Code

```text
I want to inspect skill discovery without solving the academy fixture yet.
In this disposable workspace, identify the installed Signal Desk skill and the
path that this host can discover. Explain how explicit and automatic invocation
differ in this host. If the host does not expose discovery evidence, say so.
Do not claim activation merely because you can read a file. Do not modify the
description, global settings or personal skills. Show me how to start a fresh
session for a later activation test, keeping the fixture answers hidden.
```

For optional behavior practice, follow the retained lab's activation prompts in separate fresh sessions. Start with its ordinary task request before trying an explicit mention. Record each observation separately; the second run is a different test.

## What you should see

You should know which installed copy you are testing, how you selected it, and which evidence supports loading. A claimed output artifact should actually exist where the task requested it. Missing host/model access should be reported as pending execution, not a failure of the package's structure. Reading can continue while that access is unavailable.

## If it goes wrong

If a skill cannot be found, check workspace, scope, exact name, and supported host features before rewriting its procedure. If two copies conflict, inspect their locations and choose a deliberate resolution rather than deleting both. If it activates for every question, narrow the description with positive and negative task boundaries. If it stops after loading, inspect missing references or tools separately from selection.

## Go deeper

Read [Claude Code's skill guide](https://code.claude.com/docs/en/skills), focusing on invocation control and troubleshooting; stop before advanced patterns. For Codex syntax use [the official skill invocation section](https://learn.chatgpt.com/docs/build-skills). These are public references, and only your chosen host's behavior is required. The [installed-skill lab](../../labs/10-installed-skill.md) retains positive, unrelated-task, and missing-dependency cases.

## Optional practice

Predict whether one new synthetic request should activate the skill before running it. Ask your tutor to assess both the prediction and observed selection. Do not confuse a correct final answer with proof that the intended skill was used.
