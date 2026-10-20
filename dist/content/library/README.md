# The working library

This is a curated route through **43 primary-source resources**: 11 courses, 12 documentation references, 5 engineering articles, 2 research papers, 6 books and 7 YouTube lectures. Every entry has a reason to use it and a concrete follow-up task. The machine-readable catalog is [resources.json](../resources.json); the [complete annotated index](catalog.md) includes every entry.

**Last link/content review: 20 October 2026.** “Verified” means the referenced primary page was opened and its identity and relevant coverage were checked. It does not mean the course was completed, code was run, or video playback was watched. Video entries include the author/course page used to verify the YouTube title and ID. Those distinctions are also recorded per entry.

The library is a reference bench, not a completion checklist. Spend roughly one part reading to two parts building and reviewing. Complete the course's own exercises when useful, but avoid repeatedly watching introductory material instead of producing your own evidence.

## The essential route

Choose one primary resource per stage. Use the companion only when your current artifact raises a question that the primary source does not answer.

| Stage | Primary reading or course | Companion | Artifact to produce |
| --- | --- | --- | --- |
| 1 · Foundations | [AI Fluency](https://academy.claude.com/courses/ai-fluency-framework-foundations) | [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) | A task brief, first baseline and correction log |
| 2 · Context | [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | [Original context-budget article](../articles/context-budgets.md) | Context manifest and three packet variants |
| 3 · Tools, MCP and skills | [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/unit0/introduction) | [Agent Skills specification](https://agentskills.io/specification) | A validated tool contract and a tested skill |
| 4 · Agentic development | [Claude Code 101](https://academy.claude.com/courses/claude-code-101) | [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | A reviewed bug fix with before/after evidence |
| 5 · Harness engineering | [Long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | [Original harness article](../articles/harness-architecture.md) | A bounded runner, event log and crash-resume demonstration |
| 6 · Evaluation | [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | [Original evaluation article](../articles/evaluation-vs-demo.md) | Frozen cases, rubric and a baseline comparison |
| 7 · Multi-agent systems | [Introduction to subagents](https://academy.claude.com/courses/introduction-to-subagents) | [Original delegation article](../articles/agent-delegation.md) | Delegation contracts and an integration report |
| 8 · Production | [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices) | [LLMOps lecture](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llmops/) | A runbook, release evidence and rollback exercise |

You can follow the learning objectives with different vendors. Translate configuration syntax using the selected tool's current official documentation. A `SKILL.md`, project instruction file, system prompt, MCP server and hook solve different problems; do not assume they are interchangeable simply because they all influence an agent.

## Claude / Anthropic route

The current official academy is [Claude Academy](https://academy.claude.com/). Its [developer collection](https://academy.claude.com/collections/build-with-claude) links the courses below. Follow this order if Claude Code is your main working environment:

1. [Claude Code 101](https://academy.claude.com/courses/claude-code-101): practice one small change and preserve your review evidence.
2. [Introduction to agent skills](https://academy.claude.com/courses/introduction-to-agent-skills): package a workflow you have already performed successfully.
3. [Claude Code in action](https://academy.claude.com/courses/claude-code-in-action): extend to longer tasks with explicit verification.
4. [Introduction to subagents](https://academy.claude.com/courses/introduction-to-subagents): delegate after you understand ownership and integration.
5. [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api): use when building your own application rather than only operating a coding agent.

The academy materials are described as free. Product execution and API usage are separate. In particular, the Code 101 page lists product access or an API key as a practical prerequisite, and the API course requires an API key. A course badge is a completion credential, not evidence that your application is production-ready. This repository does not issue vendor certification.

## Hugging Face route

Use the [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) to strengthen tokenization and model fundamentals, the [Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction) to compare agent implementations, and the [MCP Course](https://huggingface.co/learn/mcp-course/unit0/introduction) to build interoperable tools. The MCP course identifies Anthropic as a partner and explains its theory and hands-on structure.

Read only the units that unblock your current stage. A learner building a tool server need not first train a transformer. Conversely, if attention or tokenization is confusing, use the optional model-internals material before treating those terms as magic.

Public reading is free. Hosted projects, certificate activities and services used in exercises have their own account and compute requirements. The provider page is the authority for current enrollment and completion conditions.

## Books: choose for a problem, not for shelf size

| Book | Use it when… | Focus for this program | Legal access |
| --- | --- | --- | --- |
| [AI Engineering — Chip Huyen](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) | You need a broad application-design reference | Evaluation, RAG/agents, architecture and feedback | Publisher purchase or subscription |
| [Designing Machine Learning Systems — Chip Huyen](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) | You are designing an ongoing operating process | Data quality, deployment, monitoring and ownership | Publisher purchase or subscription |
| [Build a Large Language Model (From Scratch) — Sebastian Raschka](https://www.manning.com/books/build-a-large-language-model-from-scratch) | You want implementation depth beneath the API | Tokenization and attention; optional extension track | Publisher purchase; official sample/code access varies |
| [Hands-On Large Language Models — Jay Alammar and Maarten Grootendorst](https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/) | Visual explanations help you understand representations and retrieval | Embeddings, retrieval and practical model use | Publisher purchase or subscription |
| [Deep Learning — Ian Goodfellow, Yoshua Bengio and Aaron Courville](https://www.deeplearningbook.org/) | You need mathematical foundations | Probability and practical methodology; optional | Authorized online HTML edition is free; print paid |
| [Dive into Deep Learning — Aston Zhang, Zachary C. Lipton, Mu Li and Alexander J. Smola](https://d2l.ai/) | You learn by running small implementations | Preliminaries and attention; optional | Official online edition is free |

All six are optional. Start with freely accessible resources and buy a book only if you want its depth or format. This project links to authorized sources; it does not include copyrighted book files. The *Deep Learning* authors specifically explain that their site does not distribute a PDF.

## A purposeful video queue

These seven videos are linked from their creators' own sites or the official course pages. Playback was not watched during curation. Use the accompanying pages when you need written summaries or lecture provenance.

1. [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) — Andrej Karpathy. Explain the model lifecycle afterwards without repeating the video.
2. [How I use LLMs](https://www.youtube.com/watch?v=EWvNQjAaOHw) — Andrej Karpathy. Recreate one useful workflow using a task you actually have.
3. [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) — Andrej Karpathy. Measure surprising tokenization cases.
4. [Let's build GPT: from scratch, in code, spelled out.](https://www.youtube.com/watch?v=kCc8FmEb1nY) — Andrej Karpathy. Optional technical depth after Python/tensor prerequisites.
5. [LLMOps](https://www.youtube.com/watch?v=Fquj2u7ay40) — Josh Tobin, Full Stack Deep Learning. Turn the lecture into an experiment register.
6. [UX for Language User Interfaces](https://www.youtube.com/watch?v=l5mG4z343qg) — Sergey Karayev and Charles Frye, Full Stack Deep Learning. Prototype an evidence-and-correction interface.
7. [Augmented Language Models](https://www.youtube.com/watch?v=YdeuQhlHmCA) — Josh Tobin, Full Stack Deep Learning. Compare direct, retrieved and tool-backed answers.

Karpathy's [author page](https://karpathy.ai/) and [technical syllabus](https://karpathy.ai/zero-to-hero.html) establish the first four. The [LLMOps](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llmops/), [UX](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/ux-for-luis/) and [augmentation](https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/augmented-language-models/) pages establish the last three. The Full Stack lectures are from 2023: their model rankings and integration details are historical. Preserve the design questions; update implementations from current docs.

## Research and security reading

Read [ReAct](https://arxiv.org/abs/2210.03629) to understand a historically influential interaction pattern, then reproduce a tiny version with observable actions. Read [Lost in the Middle](https://arxiv.org/abs/2307.03172) to design your own context-position probe. A published result about particular models and tasks should become a hypothesis to test, not a universal assumption about today's model.

For stage 6, inspect [OWASP's LLM application risk taxonomy](https://genai.owasp.org/llm-top-10/) and the [MCP security guide](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices). Convert each relevant risk into a specific fixture, execution boundary and observable outcome. A list of threats alone is not a security test.

## Maintain the library

Before implementing a provider-specific feature, reopen its official page. Record the documentation version, SDK version, date and any assumptions in your experiment. When a link changes, follow a provider-owned redirect and update the catalog. Do not replace a primary source with a search summary simply because it loads faster.

If an exercise now requires an unavailable service, keep the learning objective and use a local fixture or mock. Label the result as a simulation. If a course becomes paid or a certificate changes, update the access note rather than silently promising continued access. No MAX subscription is required to read these local articles or work through offline reasoning exercises.
