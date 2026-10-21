# Explore a repository without getting lost

## Start here

You can open the assistant and distinguish teaching from editing. Now learn how to inspect a project without asking for a giant explanation of every file. The result is orientation: where to start, how the relevant behaviour works, and what command would verify it. You may use the academy itself as a read-only example.

## The idea in plain language

A repository contains different kinds of files. **Source** is the editable implementation. **Tests** check selected behaviours. **Generated files** are produced from source and are usually changed by rebuilding. A **dependency** is software the project relies on. An **entry point** is where a user or program starts a particular workflow.

An assistant can describe an architecture without checking that description. Ask for a small set of specific file references and a concrete flow. In this academy, opening the portal is not the same as running a lab, and browser progress is not the same as a source-code commit. A useful tour keeps those responsibilities distinct.

You do not have to read every file before doing useful work. Start with the project overview and applicable instructions, then follow one question into the relevant code and test. This reduces distraction and makes it easier to notice when the assistant is merely guessing from filenames.

## A small example

Suppose you ask, “Where does local learning progress get saved?” A useful tour starts from the documented local launcher, follows the local state API to the SQLite storage, and identifies a relevant persistence test. **SQLite** is a database stored in a local file; it is not a Git commit or an automatic cloud sync.

The assistant should not read private progress records just to explain the implementation. It can inspect public source and tests. It should also not modify `dist/` because generated output happens to look like the visible site. Identifying the source/build boundary is part of understanding the project.

## Try it with Codex or Claude Code

Open the course folder as explained in the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Give me a small read-only tour of this academy. Read its project instructions.
Answer one question: how does local progress get from the portal to storage?
Identify the entry point, at most four relevant source files, and one test.
Define API and SQLite when they first appear. Cite the files you actually read.
Do not open private progress databases, run the server, edit files, or fix
intentional student exercises. End with the documented verification command
and what it would prove, clearly labelled as not yet executed.
```

Open one referenced file in your editor and locate the function or section mentioned. You need not understand every line. Check that the file really serves the claimed role. If you only have the portal, use its source download when you want file inspection; the conceptual lesson remains readable without it.

## What you should see

The tour should be short enough to follow. It should distinguish source from generated assets and private runtime data. A proposed command should remain labelled as proposed. The explanation should connect the files into one flow rather than dump a directory tree without explaining which file matters first.

## If it goes wrong

If you receive fifty files, narrow the question to one observable behaviour. If the assistant cites a nonexistent function, ask it to reopen the file and correct the account. If it proposes running all tests before answering a read-only question, ask whether execution is necessary for the claimed fact. For another repository, do not assume the academy’s file layout or commands apply; read that project’s instructions first.

## Go deeper

Read “Understand new codebases” and “Find relevant code” in Claude Code’s [common workflows](https://code.claude.com/docs/en/common-workflows). Stop before bug-fixing recipes. The wording is useful with either assistant; no second subscription is necessary. The academy’s [maintenance guide](../../../docs/MAINTENANCE.md) documents this repository’s actual source and verification boundaries.

## Optional practice

Choose a different read-only question, such as where topic text becomes portal data. Predict which two files matter before asking the assistant. Compare its evidence with your prediction and ask for feedback on the difference. No architecture diagram is required.
