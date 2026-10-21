# AI engineering study plan: subjects and learning paths

Start at **Start from zero** in the portal (`#start`). The academy now has 14 independent subject tracks, each ordered from beginner to intermediate to advanced. A subject explains one area in depth. A learning path combines selected topics across subjects for a particular goal. You can always see the complete subject map in the sidebar or at `#tracks`.

The current catalog has 84 topics: 60 new readings plus all 24 retained beginner guides and their original lessons. This is a map to choose from, not a requirement to finish every page. Every topic starts with explanation, a small testing example, a copyable Codex or Claude Code prompt, expected observations, and troubleshooting. Read the [assistant quickstart](ASSISTANT-QUICKSTART.md) if you have only a coding assistant and are unsure where to paste a prompt.

Open the [complete subject and path index](SUBJECT-CATALOG.md) for a direct link to every topic in an offline Markdown reader.

## Choose your route

| Path | Who it helps | What to do |
| --- | --- | --- |
| Start from zero | No prior AI knowledge | Begin with the first topic, then follow Continue this path. Eight topics introduce assistants, tokens, clear tasks, evidence, and uncertainty. |
| AI in everyday SDET work | You understand the first concepts and want help at work | Follow repository context, safe changes, failure investigation, review, skills, and evaluation. |
| Building controlled agents | You want to understand and eventually build an agent | Study tools, permissions, MCP, the harness loop, recovery, retrieval, and delegation. |
| Operate and evaluate AI systems | You need reliable release and incident decisions | Study datasets, graders, adversarial tests, security, multi-agent failures, observability, and operations. |

Open **Learning paths** (`#path`) for each full sequence, prerequisites, outcome, and next direction. **Continue this path** stays within your chosen path even when the next topic belongs to a different subject. Opening a topic directly from a subject instead uses **Next in this subject**. Save my place remembers both the topic and the selected path when applicable.

## Every subject has a separate home

| Subject | Beginner foundations | Deeper questions |
| --- | --- | --- |
| AI foundations | What an assistant does; tokens and context limits | Uncertainty, embeddings, multimodal inputs, model selection |
| Coding assistants | First session; understanding a repository | Safe changes, failing tests, diff review, session handoff |
| Prompting and task design | Clear task contracts and examples | Untrusted input, iteration, structured outputs, regression testing |
| Context engineering | Relevant evidence and project instructions | Context budgets, checkpoints, freshness, conflicting information |
| Retrieval, RAG, and memory | Finding evidence and splitting documents | Semantic/hybrid search, grounded answers, durable memory boundaries |
| Tools, APIs, and function calling | Requests and contracts | Validation, results, side effects, version changes |
| MCP | What connects to what; discovery | Local servers, remote authentication, diagnosis, trust boundaries |
| Skills | What a skill is; package structure | Installation, invocation, testing, distribution |
| Agentic development | Workflows and bounded tasks | Verification, review, CI, replanning |
| Harness engineering | Runtime boundaries and controlled loops | Recovery, observability, cancellation, replay |
| Evaluation and AI testing | Checking outputs and choosing datasets | Grader calibration, retrieval quality, adversarial tests, release comparisons |
| Multi-agent systems | Roles, handoffs, and delegation | Shared state, conflicts, team evaluation, partial failures |
| Security and permissions | Trust boundaries and least privilege | Injection, secrets, supply chain, approvals, audit |
| Production operations | Runtime visibility and service boundaries | Cost, latency, incidents, releases, fallbacks, capstone delivery |

The precise titles, prerequisites, time estimates, materials, and selected sources live in `content/tracks/catalog-*.json`. Path orders live in `content/tracks/paths.json`. The portal renders these sources directly. Topics can be added without renumbering the original course or invalidating previous progress.

## A manageable session

1. Open one topic. Read the plain-language explanation and example before asking your assistant to do anything.
2. If useful, copy its self-contained prompt. Ask about unfamiliar words first. You can follow the example without installing a model SDK or buying API credits.
3. Compare the result with What you should see. Distinguish an explanation, a simulation, and an actually executed check.
4. Use the selected external section only for extra depth. It states what to read and where to stop; you do not need the provider's whole course catalog.
5. Continue, or save your place and stop. Optional practice comes after understanding. No drawing, report, quiz, or implementation gate blocks reading.

Time estimates are planning aids, not deadlines. Advanced means more complex decisions and failure cases, not assumed prior mastery. Use prerequisite links or ask a tutor to explain a missing idea.

## Existing material and learning records

The [original 24-lesson map](ORIGINAL-LESSON-MAP.md) remains accessible at `#legacy`, with all original stage and lesson routes. The 24 lessons are also included in their subject tracks. Their original explanations, 72 exercises, quizzes, and solution gates remain available. All 15 labs, six incidents and capstone incident, eight primers, articles, manuals, templates, books, courses, videos, and capstones are retained.

Use **Find learning materials** to search the whole collection by topic and format. Readings for a subject are also linked on its topic pages. Use the [practice map](PRACTICE-MAP.md) to choose a runnable lab after understanding its prerequisites. The PDF remains the original practice fieldbook; the complete current subject curriculum is in the portal and editable source download.

A saved place is a bookmark, not completion. Existing primer and original-lesson bookmarks remain separate from subject bookmarks; attempts and notes keep their original IDs. Local saves use SQLite and hosted saves use browser storage. [Export/import and backups](LOCAL-DATA.md) move records deliberately; there is no automatic synchronization.

For tutoring, use [the learning prompt](../templates/tutor-prompt.md). Chosen exercises keep the attempt-first, explicit-reveal contract, including incident debriefs. Ordinary explanations never require an attempted assignment.
