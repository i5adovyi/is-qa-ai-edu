# Learn with Codex or Claude Code

You can start with the assistant you already have. You do not need both products, a model API key, or a working programming environment to understand the lessons. The [study plan](STUDY-PLAN.md) has 14 independent subjects and four learning paths. Start from zero is the default. Each topic teaches the idea before practice; the original 24 lessons remain inside the relevant subjects.

## First, choose what you want to do

| Your situation | Start this way | What you need |
| --- | --- | --- |
| I want to understand a concept | Read a lesson, then paste its small example and assistant prompt into your existing assistant chat | Access to that assistant; no local project needed |
| I want the assistant to read the actual course files | Open an editable course folder in Codex or start Claude Code in that folder | A Git clone or extracted source ZIP, plus product access |
| I want to run a Python lab | Use the same editable folder and ask the assistant to inspect and explain the documented command before running it | Python and the prerequisites of that particular lab |
| I only want the local learning website | Follow [setup](SETUP.md) and run the launcher | Python 3.9+; no model account or model API key |

A **folder** contains your files. A **repository**, often shortened to repo, is a project folder whose changes Git can track. A **terminal** is the window where you type commands to run programs. An assistant's chat input accepts requests in ordinary language; the terminal accepts commands. Do not paste an entire teaching prompt into a shell.

## Learn immediately without downloading anything

1. Open [lesson 01's beginner guide](../content/how-to/01.md), or the topic you came here to understand.
2. Read “The idea in plain language” and “A small example.” You may ask the assistant to explain any term now; these explanations are not withheld as exercise answers.
3. Copy the prompt under “Try it with Codex or Claude Code” into the **assistant chat**, together with the synthetic example it asks for. These examples contain invented data, not your employer's logs.
4. Read the response against “What you should see.” Ask about one discrepancy rather than accepting a confident answer automatically.
5. Continue to the next lesson or choose optional practice. No diagram, written report, installation, or quiz pass is needed to read on.

An assistant cannot necessarily open this private portal. If it cannot read a link, paste the relevant beginner guide or attach its Markdown file. Do not ask it to guess the hidden page. This starter request works in either tool:

```text
I am an SDET learning AI engineering and may be new to programming.
Teach the concept from the beginner guide I provide below.
Define new terms before using them. Use its small example and explain
what is happening one step at a time. Do not create or edit files yet.
Do not solve the optional exercises or reveal incident answers.
After the explanation, help me check the example, then stop for my reply.
```

Add the guide's text below that request. This is a teaching conversation. It is not evidence that code ran or that you completed a practical assignment.

## Open the project in Codex

If you already have this course folder open in Codex, start at step 3.

1. Obtain the **editable source**. In the portal, use Reference shelf → Download full project, extract the ZIP, and locate the folder containing `README.md`, `AGENTS.md`, `academy.py`, and `content/`. Alternatively clone the private GitHub repository using an account that can access it. The portable ZIP is meant for reading, not editing the lab source.
2. In your desktop app, select Codex and open that local folder as the project. Labels can vary by app version. The official [quickstart](https://learn.chatgpt.com/docs/quickstart) explains selecting Codex, choosing where it works, and starting a chat. Read its desktop setup steps; stop before exploring unrelated products. Sign in through the app's normal flow if required.
3. Start a new chat in the course project and paste:

```text
Read README.md and AGENTS.md. Confirm the project folder and whether
content/how-to/01.md exists. I am here to learn, not to maintain the website.
Teach lesson 01 from that beginner guide. Explain unfamiliar terms and use
the teaching example. Do not edit files, run labs, mark progress complete,
or reveal optional exercise answers. Give me one small next step.
```

4. Check that it identifies this academy and the actual file. If it says the file is missing, check the selected folder before continuing. If it starts redesigning the website, stop it and repeat that this is a tutoring session.
5. On later lessons replace `01` with the lesson number. Your actual last saved position or supplied attempt determines where to resume; another account's chat history is not automatically available.

You can also use the installed Codex CLI from the project folder. Follow the [official CLI guide](https://learn.chatgpt.com/docs/codex/cli) for its current installation and authentication steps. The desktop route above does not require installing a second interface.

## Open the project in Claude Code

If Claude Code is already working in this course folder, start at step 3.

1. Use the same editable source folder described above. Open a terminal. If this is unfamiliar, the official [Claude Code terminal guide](https://code.claude.com/docs/en/terminal-guide) explains how to open one. Follow the [Claude Code quickstart](https://code.claude.com/docs/en/quickstart) only if installation or sign-in is needed; choose the instructions for your operating system. Stop after “Ask your first question.” Access to Claude Code is separate from GitHub and this portal.
2. Enter the folder, then start the installed tool. Replace the example path with your actual extracted folder; keep quotes if it contains spaces:

```sh
cd "/path/to/is-qa-ai-edu"
claude
```

3. Type the following in the **Claude Code prompt**, not a new shell:

```text
Read CLAUDE.md, AGENTS.md, and README.md. Confirm the project folder and
whether content/how-to/01.md exists. I am here to learn, not to maintain
this website. Teach lesson 01 using that beginner guide. Explain each
unfamiliar term and the teaching example. Do not edit files, run labs,
mark progress complete, or reveal exercise answers. Stop after one step.
```

4. Check its reported folder and file. Claude Code's session shows the working directory; a wrong folder means it is looking at a different project. If `claude` is not recognized, return to the official quickstart's installation troubleshooting. Installing Python does not install Claude Code.

The commands and product documentation were checked on 21 October 2026. Product access and interfaces can change. These are instructions for your existing assistant; no live authenticated Codex or Claude Code session was executed as part of the course's offline tests. Your product subscription and optional model API billing are separate; do not assume API usage is included.

## When you choose to run an example

The course portal displays instructions; it does not execute Python or install skills. Run examples in your local project with your assistant or terminal. The guides use `python3` for macOS/Linux. On Windows, use `py -3` if needed, as explained in [setup](SETUP.md); optional virtual-environment commands keep the specific interpreter paths documented in their lab.

1. Read the lab's prerequisites. Most core commands use only Python; the real MCP lab needs a separate environment and pinned packages. Live model routes need their own access. Do not install every optional dependency upfront.
2. Ask your assistant to explain what a command reads, writes, and requires before running it. This is a useful request:

```text
I want to inspect the bundled reference demo, not solve a student exercise.
Read lab/README.md. Explain the documented demo command in beginner terms,
including its input, output directory, and whether it calls a real model.
Check Python availability and the current directory. Run the reference demo
only in a new ignored work directory. Do not edit lab/student.py or fixtures.
Show the actual exit status and one trace event, and explain what they prove.
If a prerequisite is missing, explain that one prerequisite and stop.
```

3. A real result has an executed command, an exit status, and an output or changed file you can inspect. An assistant writing “this should pass” is a prediction. A deterministic reference simulation is not a live model test, and a successful reference run is not your independent solution.
4. Keep lab outputs in the ignored `work/` directory. If an output path already exists, choose a fresh name rather than deleting evidence. Local course progress lives in `.academy-data/`; it is unrelated to generated lab traces.

## Get unstuck without receiving the assignment answer

| What happened | Ask for this |
| --- | --- |
| A word is unfamiliar | “Define this word in this example, then show one simpler case.” |
| A command failed | Paste the exact command, error, OS, and working directory. Ask for one check, then retry it. Remove secrets first. |
| The assistant skipped steps | “Stop after the next observable action and tell me what I should see.” |
| It solved an exercise before you tried | “Use a different teaching example. Let me attempt the assigned case myself.” |
| It wants an API key immediately | “Can I learn this with the provided synthetic example or offline reference first?” |
| A course link demands more background | Return to the lesson prerequisite links; ask about the missing term instead of enrolling in an entire catalog. |

Save your reading position explicitly in the portal. Save a progress export before moving accounts or browsers; follow [Continue learning](CONTINUE-LEARNING.md) and [local data](LOCAL-DATA.md) for recovery. The assistant does not know your saved progress unless you supply it or ask it to read an authorized local record.
