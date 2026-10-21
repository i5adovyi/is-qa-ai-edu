# Install a skill where your host can find it

## Start here

Read the package topic first. Installation means putting a complete reviewed skill package where a particular host discovers it. It is different from running the skill. This lesson starts with inspection, then offers a disposable local installation. Open the academy repository in your assistant using the [quickstart](../../../docs/ASSISTANT-QUICKSTART.md). Python 3.9+ is sufficient for the academy installer; actual skill behavior additionally needs an authenticated compatible host.

## The idea in plain language

**Scope** describes where a skill is available. A project-scoped skill belongs to one workspace. A personal skill may affect many projects. For a first experiment, project scope is easier to inspect and remove. The current documented local locations differ: Codex uses `.agents/skills/<name>/SKILL.md`; Claude Code uses `.claude/skills/<name>/SKILL.md` for project skills.

The whole folder matters. Copying only `SKILL.md` can leave references or scripts missing. A structural validator can confirm that expected files and fields exist. It cannot prove that the assistant discovers the package, selects it for the right request, or produces a correct result. Those are later observations.

A download is also a software supply-chain decision. Read a package's procedure and executable helpers before running them. The academy package is available in source for inspection; this lesson does not require installing a random marketplace package or modifying your global configuration.

## A small example

The retained Signal Desk package contains instructions, a review contract, a template, and a deterministic checker. The installer creates a dedicated workspace under ignored `work/`, copies the package and synthetic fixture, and records an inventory. An existing destination is refused so a repeated command cannot silently overwrite an earlier attempt.

Its installation record keeps host behavior marked `not_tested`. That is useful honesty: file presence is one fact, and successful discovery is another. A green copy/validation result should not be relabeled as a successful AI review.

## Try it with Codex or Claude Code

```text
Guide me through a disposable skill installation in this academy repository.
First read content/skill-practice/README.md and inspect its skill package.
Explain the source folder, destination folder, copied dependencies and validator.
Do not invoke the skill or reveal fixture answers. Do not modify global settings.
Help me run the documented installer with --workspace work/skill-learning-01
only if that destination does not exist, then run its documented validation.
Show the resulting inventory and distinguish installed, discovered and executed.
```

If you choose to run the setup yourself, open a terminal in the academy repository root and run these separately:

```sh
python3 -m lab.skill_lab install --workspace work/skill-learning-01
python3 -m lab.skill_lab validate --workspace work/skill-learning-01
```

The first command copies the package; the second checks its required files and metadata. If the first reports an existing destination, choose a fresh name in both commands. Stop and inspect any other error before continuing.

For a local Claude Code session, ask the assistant to copy the complete installed skill folder into `.claude/skills/` inside that same disposable workspace, refusing an existing destination. Open the disposable workspace as your project. For Codex, use the installed `.agents/skills/` layout directly. The host-specific paths are not interchangeable.

## What you should see

Inspect the actual `SKILL.md`, supporting directories, fixture, and inventory. The validation command should report the observed structural result. If installation worked, continue to the invocation topic with the correct workspace open. Do not infer discovery from the academy source folder: hosts scan designated locations, not every folder that happens to contain Markdown.

## If it goes wrong

If the destination exists, choose a new dedicated name rather than deleting evidence. If a reference is missing, compare the whole folder against the original package. If the skill is absent from the host, confirm the working directory and start a fresh session before changing metadata. Cloud or account-synced skill behavior may differ from local project scope; consult the documentation for the actual surface you use.

## Go deeper

Read [OpenAI's local skill locations and invocation guidance](https://learn.chatgpt.com/docs/build-skills), or the corresponding [Claude Code skill locations](https://code.claude.com/docs/en/skills) if that is your host. Choose one host's sections and stop before advanced features. Both are public. The [package manual](../../skill-practice/README.md) keeps the exact academy commands and cleanup boundaries together.

## Optional practice

Inspect one dependency path in the installed copy and predict what would fail if it were missing. Try a missing-file experiment only in a new disposable copy, then ask for feedback. Leave the original course package unchanged.
