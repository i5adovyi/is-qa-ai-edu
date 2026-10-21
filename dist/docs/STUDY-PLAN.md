# The guided SDET study plan

This is the default learning route. Read the local explanations first. Follow the selected external resource only when more detail helps, then return for the next topic. No diagrams, reports, quizzes, or practical assignments are required to move through it.

The route is provider-neutral. It goes from using AI in testing work to testing AI systems, then understanding tools, agents, and harnesses. The primary recommendations are editorial choices for this learner, not vendor rankings. Reading times and external course durations are not completion guarantees; progress at your own pace.

## Where to start

[Open topic 01](../content/guide/01-ai-basics.md). In the portal use Start reading and Next topic. Use Save my place if you want to resume there later; it records a location, not mastery. A tutor can explain an unfamiliar term without asking you to produce an artifact.

## The sequence

### 01. What AI can do for an SDET

[Read the local explanation](../content/guide/01-ai-basics.md). Understand models, assistants, prompts, and context through a failed CI test.

Before this: No AI background or setup.

Selected depth: [Microsoft — Introduction to Generative AI and Large Language Models](https://github.com/microsoft/generative-ai-for-beginners/blob/main/01-introduction-to-genai/README.md#how-do-large-language-models-work). Start at “How do large language models work?” and read the following practical-use discussion. Skip the educational-startup scenario, assignment, and next-lesson links. Return to this portal afterward.

Access: Public reading. No installation or account needed to read.

Move on with this idea: A model's suggestion and verified behavior are different things.

### 02. Give AI enough information to help

[Read the local explanation](../content/guide/02-prompts-and-context.md). Frame a testing request and supply relevant, current evidence.

Before this: Topic 01: model, prompt, and context.

Selected depth: [OpenAI — Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering#message-formatting-with-markdown-and-xml). Read “Message formatting with Markdown and XML”, “Few-shot learning”, and “Include relevant context information”. Stop before “Prompting current models”. Skip API setup and code examples you do not need.

Access: Public documentation. Reading does not require API credits.

Move on with this idea: Useful context reduces missing facts; detailed wording alone cannot supply them.

### 03. Use AI in everyday testing work

[Read the local explanation](../content/guide/03-ai-assisted-testing.md). Generate and review tests without letting code define its own correctness.

Before this: Topic 02 and familiarity with ordinary automated tests.

Selected depth: [GitHub — Writing tests with GitHub Copilot](https://docs.github.com/en/copilot/tutorials/write-tests). Read the unit-test example and its execution/review steps. Treat it as an illustration if you use another assistant. A green example run is not proof of complete coverage.

Access: Public reading. Following the IDE steps requires a Copilot plan, supported IDE, and extension.

Move on with this idea: Generated tests need an independent expectation and an actual relevant test run.

### 04. Test software whose answers can vary

[Read the local explanation](../content/guide/04-evaluating-ai.md). Understand evals, test data, rubrics, graders, and regression decisions.

Before this: Topic 03; basic test and CI concepts.

Selected depth: [OpenAI — Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Read evaluation principles and the eval-process steps. Focus on objectives, datasets, scoring, and comparison; defer provider APIs.

Access: Public documentation. No paid execution required for reading.

Move on with this idea: Check deterministic properties and judged quality separately, using realistic cases.

### 05. Help AI find the right evidence

[Read the local explanation](../content/guide/05-retrieval.md). Understand RAG and separate retrieval mistakes from answer mistakes.

Before this: Topics 02 and 04: context and evaluation.

Selected depth: [Microsoft — Retrieval Augmented Generation and Vector Databases](https://github.com/microsoft/generative-ai-for-beginners/blob/main/15-rag-and-vector-databases/README.md). Read the RAG and vector-search explanation. Stop before implementation and assignment sections unless you choose hands-on work.

Access: Public reading. Build examples have separate environment and provider requirements.

Move on with this idea: The right answer needs the right authorized, current evidence and correct interpretation.

### 06. Tools, MCP, and skills without the jargon pile

[Read the local explanation](../content/guide/06-tools-mcp-skills.md). Distinguish operations, integration protocols, and reusable instructions.

Before this: Topics 02–05. Python/terminal only for optional installation work.

Selected depth: [Hugging Face — The Context Course](https://huggingface.co/learn/context-course/unit0/introduction). Read the overview, then the explanations in Units 1 (skills) and 2 (MCP). Defer plugins, subagents, hooks, and Nano Harness until topics 07–08.

Access: Public course text. Hands-on work assumes Python, CLI, a Hugging Face account, and a configured coding agent; provider access may cost money.

Move on with this idea: A skill, tool, MCP connection, and permission each serve different purposes.

### 07. Understand an agent before building one

[Read the local explanation](../content/guide/07-agents-and-workflows.md). Follow tool selection, observations, stopping, and coordination failures.

Before this: Topic 06: tools and permissions.

Selected depth: [Hugging Face — Agents Course — What is an Agent?](https://huggingface.co/learn/agents-course/unit1/what-are-agents). Read this page and Unit 1's tools and action/observation explanations. Skip the first-agent build and certificate quizzes unless you want practice.

Access: Public reading. Coding sections require basic Python and their own setup.

Move on with this idea: Evaluate the actions and their effects as well as the final answer.

### 08. Make agent work reliable enough to operate

[Read the local explanation](../content/guide/08-harness-and-reliability.md). Understand runtime controls, recovery, security, and evidence for release.

Before this: Topics 04–07: evaluations, retrieval, tools, and agents.

Selected depth: [OWASP — Top 10 for LLMs and Generative AI Applications](https://genai.owasp.org/llm-top-10/). Start with Prompt Injection, Sensitive Information Disclosure, and Excessive Agency. Use the other entries later as a risk reference, not a memorization list.

Access: Public reference; no account or tool setup needed.

Move on with this idea: Reliability comes from observable execution, enforced limits, and tested recovery.

## When an external catalog offers dozens of courses

You do not need a course from every provider. Use the named section for the topic you are studying. Product setup courses are relevant when you choose that product. Cloud deployment, enterprise administration, advanced model training, educator tracks, and certifications can wait unless your job requires them.

The portal's collapsed alternatives include Microsoft's introductory video, Google's deeper LLM material, Anthropic's broader AI-fluency course, and a harness engineering article. Google's module assumes ML foundations; it is not a replacement for the first local explanation. The broader resource library retains the original courses, videos, papers, and books.

Primary pages and their described scope were checked on 21 October 2026. This checks what to read, not enrollment, every video playback region, certificate eligibility, or whether product pricing will stay unchanged. You can always continue with the local text if an external resource is unavailable.

## Turn understanding into practice when you want it

The original material is retained in the [practice schedule](PRACTICE-STUDY-PLAN.md), [practice orientation](PRACTICE-START.md), [practice map](PRACTICE-MAP.md), and [integration labs](INTEGRATION-LABS.md). The portal's practice syllabus lists all 24 original lessons; the labs page lists all 15 numbered labs. The new topic links are selections, not the complete collection.

Choose practical work around your current job: generated-test review, retrieval evaluation, connecting a tool, or recovery from an interrupted agent run. The incident collection introduces ambiguous real-world failures when you are ready. If you ask a tutor for practice, it should give one exercise at a time, inspect your actual attempt, and reveal guidance only deliberately.

Reading gives you orientation and understanding. Independent practical skill requires trying relevant work and checking its results. Neither path should claim automatic mastery or a professional certification.
