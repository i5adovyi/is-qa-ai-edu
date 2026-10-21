# Your first useful assistant session

## Start here

Start this track if you have Codex or Claude Code but are unsure what to do with it. You do not need both. The first useful result is small: ask the assistant to explain an example, or identify the course folder and one relevant file. You are not expected to build a program before you understand the tools.

## The idea in plain language

A coding assistant combines a language model with tools. Depending on its environment, it may read files, edit them, run commands, or access connected services. Its available tools and permissions matter as much as the request you type. A chat answer about code is different from an actual file change or executed test.

A **project folder** contains related files. A **repository** is a project tracked by Git, which records changes. A **terminal** accepts executable commands. The assistant’s **chat input** accepts ordinary requests. Paste teaching prompts into chat, not into a terminal shell. If the product cannot access a folder, you can still learn by pasting the small synthetic example from a lesson.

Before asking for changes, establish the working location and mode. “Explain this” asks for teaching. “Inspect this folder” asks for reading. “Modify this file” asks for an edit. “Run this test” asks for execution. Making that distinction prevents the assistant from redesigning your project while you are trying to understand it.

## A small example

The academy contains `README.md`, `AGENTS.md`, `academy.py`, and `content/`. If the assistant claims it is in a different project, a request to “fix the course” would be poorly grounded. A better first interaction asks it to identify the directory and confirm those files exist.

Without a local clone, the synthetic example “expected status 201, received 403” is enough for a teaching conversation about evidence. The assistant can explain what those observations mean without claiming that it ran a test or read your machine. Both routes are useful; their evidence is different.

## Try it with Codex or Claude Code

Follow [Learn with Codex or Claude Code](../../../docs/ASSISTANT-QUICKSTART.md) for the interface you already have. Open the editable source folder if available. Paste this into the assistant chat:

```text
I am learning, not maintaining this project. If you can access the current
folder, identify it and read README.md and AGENTS.md. Confirm whether
content/how-to/01.md exists. Do not edit files or run labs.
Explain the difference between a model answer, a file edit, and an executed
test using “expected 201, received 403” as a synthetic example.
If you cannot access files, say so and teach from this prompt alone.
Give one small next step and stop.
```

Read the response before continuing. A grounded answer should identify actual files it read or explicitly describe its lack of access. You do not need to install Python merely to ask about an example. Python becomes relevant when you choose to run the local portal or a Python lab.

## What you should see

You should know where the assistant is working, what information it used, and whether anything changed. It should explain an executed test as an observed command and result, not a prediction. The next step should be manageable, such as opening the next beginner guide; no diagram, report, or diagnostic pass is required.

## If it goes wrong

If it starts editing, stop that task and restate the learning mode. Inspect any changes before proceeding. If a file is missing, check the selected folder or whether you downloaded the portable reader instead of the editable source. If a command is not recognised, identify which tool is missing rather than installing unrelated dependencies. If sign-in is needed, use the product’s normal authentication flow; never paste a password into a teaching prompt.

## Go deeper

Claude Code users can read its [quickstart](https://code.claude.com/docs/en/quickstart) through the first question and stop before making changes. Codex users can follow the parallel official links in the academy quickstart. Reading is public; using either product requires the access available to your account. These instructions do not claim an authenticated session was executed for you.

## Optional practice

Ask the assistant to explain one unfamiliar word from its response using a different synthetic example. Then explain the distinction back in your own words. Request feedback when ready; you need not create a file or mark a lesson completed.
