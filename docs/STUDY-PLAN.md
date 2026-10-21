# The complete AI engineering study plan

One course, eight stages, 24 lessons. The full topic map is the portal's main learning route. Every lesson starts with a beginner guide: plain-language explanation, SDET relevance, a small worked example, a concrete Codex or Claude Code how-to, expected results, and recovery steps. The original detailed lesson and its exercises remain immediately below it.

Start with [lesson 01](../content/how-to/01.md). If you only have an assistant and do not know how to use it with these files, follow [Learn with Codex or Claude Code](ASSISTANT-QUICKSTART.md). You can learn from self-contained examples without cloning, installing Python, or buying API credits. Local runnable labs have separate prerequisites.

## How to move through a lesson

1. Read the beginner guide. Follow prerequisite links when a term is unfamiliar.
2. Inspect the teaching example. Use the supplied prompt in your assistant if you want a guided explanation or demonstration.
3. Check the response against “What you should see.” An assistant's confident statement is not execution evidence.
4. Open the selected external section only when more depth would help. Each recommendation includes scope, access, and a stopping point. Return here afterward.
5. Continue to the next lesson, read the original explanation, or choose a small practice task. Independent builds come after understanding; no diagram, written report, or quiz gate is required for reading.

Save my place explicitly remembers a reading location. It does not mark a lesson complete. Existing primer bookmarks, lesson notes, exercise attempts, and incident history remain intact. Old lesson time estimates include optional engineering work; they do not measure your ability or prescribe how long you must read.

## The full sequence

### Stage 1 · Foundations & deliberate prompting

Turn vague requests into observable, testable work.

- **01 · Understand what your AI assistant is doing** — Technical topic: Think in systems, then choose the smallest useful agent. [Beginner guide](../content/how-to/01.md) · [Original lesson](../content/lessons/01-systems-before-agents.md).
- **02 · Ask for useful work without expecting mind reading** — Technical topic: Write task contracts that survive ambiguity. [Beginner guide](../content/how-to/02.md) · [Original lesson](../content/lessons/02-task-contracts.md).
- **03 · Tell whether a prompt change actually helped** — Technical topic: Run prompt experiments without fooling yourself. [Beginner guide](../content/how-to/03.md) · [Original lesson](../content/lessons/03-prompt-experiments.md).

### Stage 2 · Context engineering

Select, retrieve, preserve and challenge the information an agent sees.

- **04 · Give the assistant the right evidence** — Technical topic: Design an evidence packet with provenance. [Beginner guide](../content/how-to/04.md) · [Original lesson](../content/lessons/04-evidence-packets.md).
- **05 · Find the right information before answering** — Technical topic: Retrieve evidence before generating answers. [Beginner guide](../content/how-to/05.md) · [Original lesson](../content/lessons/05-retrieval-and-grounding.md).
- **06 · Continue work without trusting a stale summary** — Technical topic: Make memory resumable, inspectable and forgettable. [Beginner guide](../content/how-to/06.md) · [Original lesson](../content/lessons/06-memory-and-handoffs.md).

### Stage 3 · Tools, MCP & skills

Design interfaces that make useful actions explicit and bounded.

- **07 · Understand a tool before letting it act** — Technical topic: Design tools as precise contracts. [Beginner guide](../content/how-to/07.md) · [Original lesson](../content/lessons/07-tool-contracts.md).
- **08 · See what MCP connects and how one request travels** — Technical topic: Understand MCP by tracing one request. [Beginner guide](../content/how-to/08.md) · [Original lesson](../content/lessons/08-mcp-request-lifecycle.md).
- **09 · Reuse a useful procedure with a skill** — Technical topic: Package a skill that improves repeatable work. [Beginner guide](../content/how-to/09.md) · [Original lesson](../content/lessons/09-reusable-skills.md).

### Stage 4 · Agentic development

Use agents to change software through small verifiable increments.

- **10 · Ask an assistant for one understandable code change** — Technical topic: Turn a feature request into a bounded coding task. [Beginner guide](../content/how-to/10.md) · [Original lesson](../content/lessons/10-coding-task-design.md).
- **11 · Check the result instead of trusting “done”** — Technical topic: Use verification loops that catch real defects. [Beginner guide](../content/how-to/11.md) · [Original lesson](../content/lessons/11-verification-loops.md).
- **12 · Review an AI change you can actually understand** — Technical topic: Review AI changes through evidence and failure paths. [Beginner guide](../content/how-to/12.md) · [Original lesson](../content/lessons/12-review-and-delivery.md).

### Stage 5 · Harness engineering

Build the runtime that turns model proposals into controlled work.

- **13 · Understand what controls an agent's next step** — Technical topic: Build the agent loop as an explicit state machine. [Beginner guide](../content/how-to/13.md) · [Original lesson](../content/lessons/13-agent-loop-state-machine.md).
- **14 · Resume interrupted work without doing it twice** — Technical topic: Recover from crashes without duplicating work. [Beginner guide](../content/how-to/14.md) · [Original lesson](../content/lessons/14-checkpointing-and-idempotency.md).
- **15 · See what happened and know when to stop** — Technical topic: Make cost, latency and behavior observable. [Beginner guide](../content/how-to/15.md) · [Original lesson](../content/lessons/15-budgets-and-observability.md).

### Stage 6 · Evaluation & reliability

Measure outcomes, expose failure modes and make defensible comparisons.

- **16 · Choose examples that reveal whether AI helps** — Technical topic: Build an evaluation set that reflects the job. [Beginner guide](../content/how-to/16.md) · [Original lesson](../content/lessons/16-evaluation-datasets.md).
- **17 · How to check whether an AI answer deserves to pass** — Technical topic: Use graders carefully and report uncertainty. [Beginner guide](../content/how-to/17.md) · [Original lesson](../content/lessons/17-graders-and-statistics.md).
- **18 · How to test the boundaries of an AI feature** — Technical topic: Red-team the whole system and set release gates. [Beginner guide](../content/how-to/18.md) · [Original lesson](../content/lessons/18-red-teaming-and-release-gates.md).

### Stage 7 · Multi-agent systems

Delegate only when coordination produces measurable value.

- **19 · How to decide whether another agent would help** — Technical topic: Decide when delegation is worth its coordination cost. [Beginner guide](../content/how-to/19.md) · [Original lesson](../content/lessons/19-delegation-design.md).
- **20 · How to keep several workers from losing each other's work** — Technical topic: Coordinate workers without losing ownership or state. [Beginner guide](../content/how-to/20.md) · [Original lesson](../content/lessons/20-multi-agent-coordination.md).
- **21 · How to tell whether an agent team is worth the extra work** — Technical topic: Measure whether your agent team is actually better. [Beginner guide](../content/how-to/21.md) · [Original lesson](../content/lessons/21-multi-agent-evaluation.md).

### Stage 8 · Production & capstone

Operate, govern and demonstrate a complete system.

- **22 · How to move from a promising demo to a bounded service** — Technical topic: Design a production boundary and service contract. [Beginner guide](../content/how-to/22.md) · [Original lesson](../content/lessons/22-production-design.md).
- **23 · How to investigate a failure without guessing the cause** — Technical topic: Operate the system and learn from incidents. [Beginner guide](../content/how-to/23.md) · [Original lesson](../content/lessons/23-operations-and-incidents.md).
- **24 · How to build a small project with your assistant, then grow it** — Technical topic: Choose, build and defend your capstone. [Beginner guide](../content/how-to/24.md) · [Original lesson](../content/lessons/24-capstone.md).

## Where the other materials fit

| Material | Use it for | Where to find it |
| --- | --- | --- |
| 24 beginner how-to guides | Learn each concept and use an assistant step by step | Top of every lesson; links above |
| Original 24 lessons and 72 exercises | More explanation and optional independent application | Same lesson page and exercise workspaces |
| Eight short primers | A shorter first look or a recap | [Primer reading selections](PRIMER-READINGS.md), portal Short primers |
| Articles, manuals, and templates | Answer a focused question or reuse an engineering aid | Related materials on each lesson; Find learning materials |
| 15 runnable labs | Observe and change real local behavior | Practice labs; [prerequisite map](PRACTICE-MAP.md) |
| Six incidents plus capstone incident | Investigate ambiguous failures after the relevant foundations | Incident practice; prerequisites in each brief |
| Courses, books, videos, papers, and documentation | Study selected sections or explore deeply | External courses & books; search by format/provider/stage |
| Capstones | Combine learned skills into a substantial project | Lesson 24 and Capstones |
| Original fieldbook PDF | Offline reference for the original practice edition | Reference shelf; current beginner guides are in portal/Markdown/source ZIP |

Use **Find learning materials** to search topics such as MCP, state machine, skills, retrieval, evaluation, retries, or context. It includes every distributed Markdown document and all external library entries. It shows titles rather than exercise answers. Source code and fixtures remain available from their lab manuals and the full source download.

## Choose depth without losing the route

The [original practice schedule](PRACTICE-STUDY-PLAN.md) retains its time budgets, diagnostic, integration work, and extended routes. The [practice orientation](PRACTICE-START.md) remains available for deliberate engineering practice. These are optional schedules, not a second required curriculum. Use [integration labs](INTEGRATION-LABS.md) when you are ready for real MCP, installed skills, and a composed student harness.

The eight [primer reading selections](PRIMER-READINGS.md) preserve the earlier short explanations and scoped external sources. Use one if a full lesson feels too dense, then return to that lesson. Microsoft, OpenAI, Hugging Face, GitHub, Anthropic, Google, OWASP, standards bodies, and research authors are selected by topic. You do not need to complete every provider's catalog.

When practising with a tutor, attempt one task before requesting its next hint or solution. Teaching examples use different inputs from assignments; ordinary explanations remain available immediately. Incident guidance still requires a substantive recorded attempt and a separate explicit reveal. Reading or running reference code alone is not independent engineering mastery.
