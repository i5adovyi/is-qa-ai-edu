# Share, version and retire a skill

## Start here

Complete the testing topic before treating a skill as reusable by other people. **Distribution** means delivering the package to another installation. **Versioning** lets you identify which package produced a result. This lesson reviews a hypothetical release; it does not publish anything. Open your assistant through the [quickstart](../../../docs/ASSISTANT-QUICKSTART.md). A local disposable folder is sufficient if you later want to inspect a package.

## The idea in plain language

A reusable skill needs more than a persuasive `SKILL.md`. Its referenced files, scripts, runtime requirements, license, and installation scope must travel with it. A **dependency** is something the package relies on. A **release** is a specific, identified set of files. A **rollback** returns an installation to a known earlier release if a new one causes problems.

A Git commit can identify the source snapshot. An inventory of file hashes can detect changed bytes, but it does not establish that those bytes are safe or educationally correct. Host features may require extra metadata or plugin packaging for distribution. Keep the portable procedure separate from host-specific installation details and test each supported host explicitly.

Upgrades deserve a review. A changed description can alter when a skill activates; a changed script can alter what it executes; a changed reference can alter its decisions. Treat those as behavior changes, not cosmetic text edits. Distribution also has a privacy boundary: fixtures should remain synthetic, and personal outputs or credentials do not belong in the package.

## A small example

Signal Desk's review skill version A asks for one missing piece of evidence. Version B now creates an external ticket when evidence is incomplete. Even if its final answer looks similar, the authority and side effects changed substantially. Existing users should not discover that change through an unexpected ticket.

A smaller update might fix a misspelled reference path. That still needs a package validation and a focused behavior check, but it does not necessarily require repeating every unrelated experiment. The release description should explain the actual change and its tested limits.

## Try it with Codex or Claude Code

```text
Review a hypothetical skill release; do not publish, install or edit anything.
Version A summarizes supplied synthetic failures and asks for missing evidence.
Version B additionally creates external tickets automatically when data is missing.
Explain what changed in authority, dependencies, activation and testing needs.
Then outline a safer local release comparison with explicit version identity,
complete package files, synthetic examples and a rollback option.
Define dependency, release and rollback before using them.
```

If you want to package your own skill afterward, ask the assistant to inspect your chosen host's current official distribution guide first. A plugin can bundle several capabilities; it is not automatically necessary for a single project-local experiment.

## What you should see

The review should identify new external writes as a meaningful behavior change and require the correct task authorization at execution time. It should distinguish a package that can be copied from one proven to work on a particular host. A rollback plan should identify preserved previous files and configuration, not promise that reverting code can undo messages already sent.

## If it goes wrong

If a bundle contains outputs from `work/`, remove them from the distribution selection while preserving them privately. If only the manifest is shared, check every relative reference. If two hosts behave differently, report separate support status instead of claiming universal compatibility. If an old release is retired, give users a migration path and a way to recognize the replacement rather than silently reusing its name for a different purpose.

## Go deeper

Read [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins), focusing on package structure and manifest concepts. Stop before submission. It is one host's public distribution reference; it does not obligate you to publish or to adopt that host. Keep the [academy package manual](../../skill-practice/README.md) nearby for its local inventory and privacy boundaries.

## Optional practice

Inspect a proposed change to one synthetic skill file and predict which earlier test should be rerun. Explain why that test is relevant before asking your tutor for feedback. No public release is needed to learn release discipline.
