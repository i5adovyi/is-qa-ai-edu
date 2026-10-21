# What belongs in a skill

## Start here

You have probably repeated an instruction such as “review this test failure, cite the evidence, and do not invent a root cause.” A skill can package that reusable procedure. You do not need to install one yet. Open Codex or Claude Code using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then follow the small example. Knowing that a folder can contain text files is enough to begin.

## The idea in plain language

A **skill** is a reusable package of task instructions and, optionally, supporting files. The Agent Skills format uses a `SKILL.md` file with descriptive metadata and a procedure. **Metadata** is information about the skill, such as its name and when it should be used. Supporting files can provide reference rules, templates, or scripts.

A skill is different from a tool. “Inspect the evidence before suggesting a fix” is guidance; `read_file` is an operation that can obtain evidence. A skill might tell the assistant how to combine several tools, but it does not automatically provide those tools or their credentials. A project instruction file, such as `AGENTS.md`, describes continuing project expectations; a skill is useful for a more focused workflow selected when relevant.

The benefit is consistency and discoverability. The cost is another maintained dependency. A vague procedure can spread the same mistake to many sessions. Start with a recurring, bounded task whose inputs and useful output you understand; do not turn every single prompt into a skill.

## A small example

Signal Desk repeatedly receives synthetic test-failure summaries. A candidate skill could request the failed assertion and relevant log excerpt, separate observed facts from hypotheses, and propose one diagnostic check. It should say what to do when evidence is missing. “Be an expert SDET” does not define that behavior.

The skill should not silently expand into changing production settings or submitting incidents. Those actions require separate task authority and tools. Nor should it always run whenever someone mentions tests. A general question about the meaning of an assertion may need a short explanation rather than the whole failure-triage procedure.

## Try it with Codex or Claude Code

```text
Help me understand when a skill is useful. Do not create or install files yet.
Repeated task: review a synthetic test-failure excerpt, distinguish observations
from hypotheses, and suggest one next diagnostic check. Missing evidence should
lead to a focused question. No repository edits or external messages are allowed.
Explain what would belong in the description, procedure and supporting reference.
Compare this with a one-off prompt, AGENTS.md guidance and a tool.
Give a small demonstration using an invented timeout log, not an academy exercise.
```

Ask for the example in ordinary language before looking at file syntax. Once the purpose makes sense, the retained package lesson shows how the folder is organized.

## What you should see

The explanation should identify when the procedure applies, what evidence it needs, what it produces, and where it stops. It should distinguish a useful hypothesis from a proven root cause. No installation or execution has occurred in this walkthrough. A convincing skill description is a design proposal; you still need to test whether a host selects it and follows it appropriately.

## If it goes wrong

If the assistant proposes a giant “do all QA” skill, narrow it to one repeated workflow. If it adds a helper script, ask what deterministic calculation needs code; a simple procedure may need none. If it embeds secrets or personal logs as examples, replace them with synthetic fixtures. If it claims a skill bypasses normal permissions, return to the Tools and Security tracks' authority boundaries.

## Go deeper

Read the [Agent Skills specification](https://agentskills.io/specification), beginning with Directory structure and SKILL.md format, then Progressive disclosure. Stop before validation tooling. This public reading requires no host account. Next read [the retained package lesson](../../how-to/09.md). The [installed-skill lab](../../labs/10-installed-skill.md) is optional practice once installation and invocation make sense.

## Optional practice

Choose one repeated synthetic SDET task and tell your tutor why a skill might help. State one situation where it should not activate. Try that boundary definition before asking the tutor to improve it; no Markdown file is required.
