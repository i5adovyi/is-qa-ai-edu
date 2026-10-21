# Project instructions that help the next session

## Start here

You know how to select evidence for one task. Now learn how to preserve a small amount of useful working guidance for future tasks. This lesson explains `AGENTS.md` and `CLAUDE.md` without asking you to rewrite the academy’s instructions. You can inspect existing files before authoring anything.

## The idea in plain language

A project instruction file tells an assistant how to work in a repository: its purpose, important boundaries, source locations, and relevant checks. It is durable context, intended to remain useful across sessions. A temporary failure log, personal reading history, or incomplete investigation belongs elsewhere.

**Scope** means where an instruction applies. Some tools combine user-level, repository-level, and directory-level guidance. The exact discovery rules depend on the product and configuration. Do not assume that a familiar filename was automatically read; ask the assistant which applicable files it actually used.

Codex documents `AGENTS.md` guidance. Claude Code documents `CLAUDE.md` and related instruction-loading behaviour. This academy uses `AGENTS.md` as its maintained working guide and points `CLAUDE.md` to it. That is a repository choice; it does not mean all assistants in all configurations interpret every filename identically.

Useful instructions are specific and testable. “Run the relevant tests described in the maintenance guide” points to maintained knowledge. “Always do everything perfectly” supplies little guidance. Avoid copying entire manuals into every instruction file, where duplicate versions can disagree.

## A small example

Signal Desk has generated web files and editable source. A concise instruction says, “Edit source under `portal/`; rebuild generated output.” Another says, “Keep local progress databases out of Git.” These rules prevent recurring mistakes and belong in durable project guidance.

“The timeout test failed on my laptop this morning” is a temporary observation. It needs a timestamp, command, environment, and task context. Treating it as a permanent project rule can make future sessions repeat irrelevant work. “The learner completed lesson five” is personal progress and must not be fabricated or shared as repository context.

An instruction file also is not a secret store. A token written there can be read by collaborators, packaged in downloads, or sent as model context. Store credentials through appropriate private configuration instead.

## Try it with Codex or Claude Code

Open the editable course folder using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Inspect README.md, AGENTS.md, and CLAUDE.md without editing them.
Explain which file is the maintained working guide in this repository and
how the others point to it. Identify one durable rule, one source-map fact,
and one instruction that protects personal learning records. Cite actual text.
Then classify these hypothetical additions: “edit source, rebuild output”;
“my token is SECRET”; “yesterday a local test failed”; “use the documented
test command”. Explain where each belongs without creating files.
```

If file access is unavailable, paste the relevant sections rather than asking the assistant to infer the repository. The learning goal is to recognise useful durable guidance, not to create more documentation for its own sake.

## What you should see

The response should cite current files and avoid asserting that all instruction discovery is universal. It should distinguish durable rules from private or temporary state. A useful summary should help a fresh session choose the correct mode: tutoring, maintenance, or setup. It should not replace your current request with an old historical task.

## If it goes wrong

If the assistant follows an obsolete instruction, compare it with the current user request and source file. If two maintained files disagree, identify the canonical source before editing. If it claims an instruction file was loaded automatically, request evidence or explicitly ask it to read the file. If guidance grows too long, preserve the important rule and link the detailed manual.

## Go deeper

Read “How Codex discovers guidance” in [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), then stop before optional fallback configuration. Claude Code users can compare [its memory and instruction documentation](https://code.claude.com/docs/en/memory). These are public references, not a requirement to install both tools.

## Optional practice

Ask your tutor for five fictional project facts. Decide which two belong in durable instructions and explain why. Try before seeing a sample instruction file. Do not change this academy’s canonical guide as part of that practice.
