# Complete subject and learning-path catalog

This index is generated from the same metadata as the portal. Start with [Start from zero](START-HERE.md) or choose a subject below. Every original lesson remains available; the [original map](ORIGINAL-LESSON-MAP.md) preserves its previous order.

## AI foundations

Understand models, tokens, uncertainty, embeddings, images, and model choices.

Helpful first: No previous AI knowledge.

- **Beginner** · [What AI can do for an SDET](../content/how-to/01.md) — Separate model, assistant, workflow, agent, and harness.
- **Beginner** · [Tokens, context windows, and why a chat forgets](../content/tracks/foundations/tokens.md) — Understand capacity limits and preserve useful evidence.
- **Intermediate** · [Why fluent answers can still be wrong](../content/tracks/foundations/uncertainty.md) — Distinguish observations, hypotheses, and invented certainty.
- **Intermediate** · [Embeddings: finding similar meaning with numbers](../content/tracks/foundations/embeddings.md) — Understand vectors and why similarity is not proof.
- **Advanced** · [Images, screenshots, and multimodal evidence](../content/tracks/foundations/multimodal.md) — Choose visual inputs and verify what the assistant actually observed.
- **Advanced** · [Choose prompting, retrieval, or model adaptation](../content/tracks/foundations/model-choice.md) — Make an evidence-based choice without chasing model rankings.

## Codex and Claude Code

Learn to open a project, inspect it, make small changes, test, review, and resume.

Helpful first: AI foundations

- **Beginner** · [Your first useful assistant session](../content/tracks/assistants/first-session.md) — Find the right folder and ask for one understandable result.
- **Beginner** · [Explore a repository without getting lost](../content/tracks/assistants/repository-tour.md) — Find the entry point, test command, and relevant source.
- **Intermediate** · [Make one small change you can explain](../content/tracks/assistants/safe-change.md) — Use a disposable example, inspect the patch, and verify behaviour.
- **Intermediate** · [Investigate a failing test with evidence](../content/tracks/assistants/test-failures.md) — Separate a product defect from environment or test failures.
- **Advanced** · [Review AI changes beyond a green test](../content/tracks/assistants/review-diffs.md) — Read the actual difference and challenge weak verification.
- **Advanced** · [Resume work in a fresh assistant session](../content/tracks/assistants/session-handoff.md) — Reconcile a short handoff with current files and evidence.

## Prompting and task design

Express outcomes, teach with examples, handle untrusted input, and test prompt changes.

Helpful first: AI foundations

- **Beginner** · [Turn a request into a clear task](../content/how-to/02.md) — State the outcome, evidence, constraints, and stopping point.
- **Beginner** · [Teach a task with a few examples](../content/tracks/prompting/examples.md) — Use varied examples without leaking the answer to your evaluation.
- **Intermediate** · [Keep instructions separate from supplied data](../content/tracks/prompting/untrusted-inputs.md) — Recognise injected instructions in logs and retrieved documents.
- **Intermediate** · [Improve a prompt one failure at a time](../content/tracks/prompting/iteration.md) — Diagnose an output failure and change one relevant part.
- **Advanced** · [Ask for structured results and validate meaning](../content/tracks/prompting/structured-results.md) — Separate parseable JSON from a factually correct decision.
- **Advanced** · [Compare prompts without fooling yourself](../content/how-to/03.md) — Use explicit criteria, paired cases, and held-out examples.

## Context engineering

Select evidence, maintain instructions, budget context, resume, and resolve stale or conflicting facts.

Helpful first: AI foundations, Prompting and task design

- **Beginner** · [Choose the evidence an assistant actually needs](../content/how-to/04.md) — Separate observations, hypotheses, sources, and applicability.
- **Beginner** · [Project instructions that help the next session](../content/tracks/context/project-instructions.md) — Use AGENTS.md and CLAUDE.md as concise working guidance.
- **Intermediate** · [Pack useful context without dumping everything](../content/tracks/context/budget.md) — Choose what to include now, retrieve later, and keep out.
- **Intermediate** · [Carry state across long tasks and new sessions](../content/how-to/06.md) — Retain decisions and recheck facts when work resumes.
- **Advanced** · [Check whether evidence is still true](../content/tracks/context/freshness.md) — Track versions, timestamps, and invalidation triggers.
- **Advanced** · [Resolve conflicting evidence without guessing](../content/tracks/context/conflicts.md) — Separate authority, scope, time, and malicious instructions.

## Retrieval, RAG, and memory

Prepare sources, find relevant evidence, ground answers, and preserve access boundaries.

Helpful first: AI foundations, Context engineering

- **Beginner** · [Find evidence before asking for an answer](../content/how-to/05.md) — Understand retrieval-augmented generation and its failure points.
- **Beginner** · [Split documents without breaking their meaning](../content/tracks/retrieval/chunking.md) — Preserve headings, exceptions, and source metadata.
- **Intermediate** · [Understand semantic search before installing a database](../content/tracks/retrieval/semantic-search.md) — Match questions to meaning and inspect relevance.
- **Intermediate** · [Combine exact and semantic search](../content/tracks/retrieval/hybrid-search.md) — Handle identifiers, paraphrases, filters, and ranking.
- **Advanced** · [Cite evidence and know when to abstain](../content/tracks/retrieval/grounded-answers.md) — Check whether each claim is supported and applicable.
- **Advanced** · [Design memory that respects users and change](../content/tracks/retrieval/memory-boundaries.md) — Separate persistent facts, scope, deletion, and stale preferences.

## Tools, APIs and function calling

Understand how an assistant requests actions and how software decides what may run.

Helpful first: AI foundations, Prompting and task design

- **Beginner** · [What a tool call actually does](../content/tracks/tools/requests.md) — Follow a request from the assistant to an application and back.
- **Beginner** · [Tool contracts and authority](../content/how-to/07.md) — Retained lesson 07: understand the boundary before running a tool.
- **Intermediate** · [Validate inputs before anything happens](../content/tracks/tools/validation.md) — Separate data shape, business rules, and permission checks.
- **Intermediate** · [Read results, errors and incomplete evidence](../content/tracks/tools/results.md) — Recognize empty results, failed calls, pagination, and untrusted output.
- **Advanced** · [Retries without duplicate effects](../content/tracks/tools/side-effects.md) — Understand uncertain outcomes, operation identity, and reconciliation.
- **Advanced** · [Version and test a tool interface](../content/tracks/tools/versioning.md) — Detect breaking changes and keep recorded tool examples useful.

## Model Context Protocol (MCP)

Follow a real integration from discovery to local execution, remote access, and diagnosis.

Helpful first: Tools, APIs and function calling

- **Beginner** · [MCP without the mystery](../content/tracks/mcp/basics.md) — Place MCP beside tools, APIs, and the assistant you already use.
- **Beginner** · [Discover and inspect available capabilities](../content/how-to/08.md) — Retained lesson 08: read schemas and distinguish a connector from authority.
- **Intermediate** · [Follow your first real local MCP connection](../content/tracks/mcp/local-server.md) — Inspect and optionally run the pinned SDK lab one observable step at a time.
- **Intermediate** · [Remote MCP, authentication and authorization](../content/tracks/mcp/remote-auth.md) — Understand endpoints, account identity, scope, and expired access.
- **Advanced** · [Find the layer that broke](../content/tracks/mcp/diagnosis.md) — Use request IDs and controlled failures to distinguish transport, schema, and tool errors.
- **Advanced** · [MCP trust boundaries in real projects](../content/tracks/mcp/trust.md) — Separate server installation, returned content, credentials, and action permission.

## Skills and reusable workflows

Learn what a skill contains, install a disposable copy, test activation, and share changes safely.

Helpful first: Codex and Claude Code, Prompting and task design

- **Beginner** · [What belongs in a skill](../content/tracks/skills/basics.md) — Choose when repeated instructions deserve a reusable package.
- **Beginner** · [Read a skill package](../content/how-to/09.md) — Retained lesson 09: inspect the instruction file, references, and helper scripts.
- **Intermediate** · [Install a skill where your host can find it](../content/tracks/skills/installation.md) — Use a disposable project and keep the whole package together.
- **Intermediate** · [Invocation, discovery and skill conflicts](../content/tracks/skills/invocation.md) — Distinguish choosing a skill explicitly from the host selecting it automatically.
- **Advanced** · [Test whether a skill actually helps](../content/tracks/skills/testing.md) — Compare selection, output quality, missing inputs, and unrelated requests.
- **Advanced** · [Share, version and retire a skill](../content/tracks/skills/distribution.md) — Package dependencies, review diffs, and provide a practical rollback route.

## Agentic development and workflows

Move from a small controlled coding task to reviewable, bounded workflows.

Helpful first: Codex and Claude Code, Tools, APIs and function calling

- **Beginner** · [From chat to a controlled workflow](../content/tracks/agentic/workflows.md) — Understand steps, branches, and who decides the next action.
- **Beginner** · [Give an agent a small reviewable task](../content/how-to/10.md) — Retained lesson 10: specify expected behavior and the boundary of a change.
- **Intermediate** · [Verify the change with useful evidence](../content/how-to/11.md) — Retained lesson 11: inspect tests and distinguish a passing command from correctness.
- **Intermediate** · [Review and deliver a patch](../content/how-to/12.md) — Retained lesson 12: examine the change, evidence, and remaining risk.
- **Advanced** · [Agent work in CI and pull requests](../content/tracks/agentic/ci.md) — Keep untrusted changes away from privileged automation and check the actual commit.
- **Advanced** · [Know when to stop or change the plan](../content/tracks/agentic/replanning.md) — Use evidence, budgets, and user intent to avoid endless unsuccessful editing.

## Harness engineering

Understand the software that validates, executes, observes, and stops an agent.

Helpful first: Tools, APIs and function calling, Agentic development and workflows

- **Beginner** · [What a harness is responsible for](../content/tracks/harness/boundaries.md) — Separate model proposals from the code that grants and records execution.
- **Beginner** · [Read a bounded execution loop](../content/how-to/13.md) — Retained lesson 13: understand state and transitions with a small example first.
- **Intermediate** · [Save state and recover without duplicate work](../content/how-to/14.md) — Retained lesson 14: checkpoints, operation identities, and uncertain outcomes.
- **Intermediate** · [Follow traces and budgets](../content/how-to/15.md) — Retained lesson 15: inspect operation history, elapsed time, and consumed resources.
- **Advanced** · [Timeouts, cancellation and unfinished work](../content/tracks/harness/cancellation.md) — Distinguish stopping a wait from stopping a process or reversing an effect.
- **Advanced** · [Replay, resume and change identity](../content/tracks/harness/replay.md) — Know what a recording proves and when a checkpoint no longer matches the program.

## Evaluations and testing AI systems

Learn to judge outputs, construct trustworthy cases, localize RAG failures, and make regression decisions.

Helpful first: AI foundations

- **Beginner** · [Test an AI answer before trusting it](../content/tracks/evaluation/evaluating-outputs.md) — Check shape, task compliance, and evidence before trusting an answer.
- **Beginner** · [Choose examples that reveal whether AI helps](../content/how-to/16.md) — Choose representative examples and preserve their expected behavior.
- **Intermediate** · [How to check whether an AI answer deserves to pass](../content/how-to/17.md) — Check whether human, deterministic, and model judges deserve trust.
- **Intermediate** · [Check retrieval, evidence, and the final answer separately](../content/tracks/evaluation/grounded-retrieval.md) — Separate retrieval coverage, supported claims, and applicable sources.
- **Advanced** · [How to test the boundaries of an AI feature](../content/how-to/18.md) — Test boundaries and unacceptable behavior before release.
- **Advanced** · [Decide whether an AI change is actually an improvement](../content/tracks/evaluation/regression-decisions.md) — Use paired cases, slices, and holdouts to evaluate changes honestly.

## Multi-agent systems

Understand handoffs, delegation, shared state, conflicts, evaluation, and recovery across workers.

Helpful first: Agentic development and workflows

- **Beginner** · [Understand what one agent hands to another](../content/tracks/multiagent/roles-and-handoffs.md) — Understand who owns the next step and what context must cross a handoff.
- **Beginner** · [How to decide whether another agent would help](../content/how-to/19.md) — Choose when another worker can help and when one agent is enough.
- **Intermediate** · [How to keep several workers from losing each other's work](../content/how-to/20.md) — Keep task identities, ownership, and saved information consistent.
- **Intermediate** · [Combine worker results without losing or inventing work](../content/tracks/multiagent/conflict-resolution.md) — Combine worker results without confusing clean merges with correct behavior.
- **Advanced** · [How to tell whether an agent team is worth the extra work](../content/how-to/21.md) — Measure whether a team improves on the simpler baseline.
- **Advanced** · [Recover when only part of an agent team finishes](../content/tracks/multiagent/partial-failure.md) — Distinguish failure, cancellation, and unknown side effects during recovery.

## Security and permissions

Learn trust boundaries, access scopes, injection defenses, secrets, supply-chain review, and enforceable approvals.

Helpful first: Tools, APIs and function calling

- **Beginner** · [Tell instructions, evidence, and permissions apart](../content/tracks/security/trust-boundaries.md) — Tell accurate information, task instructions, and access authority apart.
- **Beginner** · [Give an assistant only the access its task needs](../content/tracks/security/permission-scopes.md) — Connect each capability to a task and its enforcing boundary.
- **Intermediate** · [Keep retrieved instructions from taking over a task](../content/tracks/security/injection-defenses.md) — Contain instructions hidden in retrieved content without discarding useful evidence.
- **Intermediate** · [Debug an AI workflow without leaking its data](../content/tracks/security/secrets-and-logs.md) — Preserve diagnostic evidence while limiting sensitive-data copies.
- **Advanced** · [Inspect what you install before giving it access](../content/tracks/security/supply-chain.md) — Inspect package origins, scripts, dependencies, destinations, and upgrades.
- **Advanced** · [Make approvals match the action that actually runs](../content/tracks/security/approval-audit.md) — Bind approval to the precise action and preserve truthful execution evidence.

## Production operations

Follow requests, define reliable service behavior, budget work, handle incidents, and release recoverably.

Helpful first: Harness engineering, Evaluations and testing AI systems

- **Beginner** · [Follow one request through an AI system](../content/tracks/production/runtime-observability.md) — Follow one request and distinguish transport success from a supported answer.
- **Beginner** · [How to move from a promising demo to a bounded service](../content/how-to/22.md) — Define the bounded service and the outcomes users can depend on.
- **Intermediate** · [Budget time, tokens, retries, and useful outcomes](../content/tracks/production/cost-latency.md) — Measure full workflow cost, time, retries, and budget exhaustion.
- **Intermediate** · [How to investigate a failure without guessing the cause](../content/how-to/23.md) — Contain problems and investigate evidence without guessing the cause.
- **Advanced** · [Release an AI change with a way to stop and recover](../content/tracks/production/releases-fallbacks.md) — Version behavior, observe limited rollouts, and plan safe fallback and rollback.
- **Advanced** · [How to build a small project with your assistant, then grow it](../content/how-to/24.md) — Combine the tracks in a small inspectable project and grow from evidence.

## Curated paths

These paths select topics across subjects. Prerequisites describe the starting point, not a grading gate.

### Start from zero

Understand an assistant, use a small testing example, ask clear questions, and supply useful context before moving into specialist subjects.

**Before this:** No previous AI knowledge. Reading needs only a browser; guided demonstrations use your existing Codex or Claude Code.

1. [What AI can do for an SDET](../content/how-to/01.md)
2. [Tokens, context windows, and why a chat forgets](../content/tracks/foundations/tokens.md)
3. [Your first useful assistant session](../content/tracks/assistants/first-session.md)
4. [Explore a repository without getting lost](../content/tracks/assistants/repository-tour.md)
5. [Turn a request into a clear task](../content/how-to/02.md)
6. [Teach a task with a few examples](../content/tracks/prompting/examples.md)
7. [Choose the evidence an assistant actually needs](../content/how-to/04.md)
8. [Why fluent answers can still be wrong](../content/tracks/foundations/uncertainty.md)

**Afterward:** Choose AI in everyday SDET work for practical use, or Building agents for the engineering route.

### AI in everyday SDET work

Move from a small repository task to meaningful tests, review, reusable skills, and reliable evaluation. Use the tools you already have.

**Before this:** Start from zero, or comfort with prompts, context, and the difference between generated text and execution evidence.

1. [Project instructions that help the next session](../content/tracks/context/project-instructions.md)
2. [Tell instructions, evidence, and permissions apart](../content/tracks/security/trust-boundaries.md)
3. [Give an assistant only the access its task needs](../content/tracks/security/permission-scopes.md)
4. [Make one small change you can explain](../content/tracks/assistants/safe-change.md)
5. [Investigate a failing test with evidence](../content/tracks/assistants/test-failures.md)
6. [From chat to a controlled workflow](../content/tracks/agentic/workflows.md)
7. [Give an agent a small reviewable task](../content/how-to/10.md)
8. [Verify the change with useful evidence](../content/how-to/11.md)
9. [Review AI changes beyond a green test](../content/tracks/assistants/review-diffs.md)
10. [Resume work in a fresh assistant session](../content/tracks/assistants/session-handoff.md)
11. [What belongs in a skill](../content/tracks/skills/basics.md)
12. [Read a skill package](../content/how-to/09.md)
13. [Install a skill where your host can find it](../content/tracks/skills/installation.md)
14. [Invocation, discovery and skill conflicts](../content/tracks/skills/invocation.md)
15. [Test an AI answer before trusting it](../content/tracks/evaluation/evaluating-outputs.md)
16. [Choose examples that reveal whether AI helps](../content/how-to/16.md)
17. [How to check whether an AI answer deserves to pass](../content/how-to/17.md)
18. [Check retrieval, evidence, and the final answer separately](../content/tracks/evaluation/grounded-retrieval.md)
19. [How to test the boundaries of an AI feature](../content/how-to/18.md)
20. [Decide whether an AI change is actually an improvement](../content/tracks/evaluation/regression-decisions.md)

**Afterward:** Deepen skills, MCP, context, or evaluation through their subject tracks. Choose an optional workplace lab when you want independent practice.

### Building controlled agents

Connect tools and MCP, understand a controlled loop, ground answers in evidence, then handle recovery and delegation.

**Before this:** Start from zero. Comfort opening a repository and asking your assistant to explain a small script; optional runnable labs require their listed setup.

1. [From chat to a controlled workflow](../content/tracks/agentic/workflows.md)
2. [Tell instructions, evidence, and permissions apart](../content/tracks/security/trust-boundaries.md)
3. [Give an assistant only the access its task needs](../content/tracks/security/permission-scopes.md)
4. [What a tool call actually does](../content/tracks/tools/requests.md)
5. [Tool contracts and authority](../content/how-to/07.md)
6. [Validate inputs before anything happens](../content/tracks/tools/validation.md)
7. [MCP without the mystery](../content/tracks/mcp/basics.md)
8. [Discover and inspect available capabilities](../content/how-to/08.md)
9. [Follow your first real local MCP connection](../content/tracks/mcp/local-server.md)
10. [Remote MCP, authentication and authorization](../content/tracks/mcp/remote-auth.md)
11. [Find the layer that broke](../content/tracks/mcp/diagnosis.md)
12. [MCP trust boundaries in real projects](../content/tracks/mcp/trust.md)
13. [What a harness is responsible for](../content/tracks/harness/boundaries.md)
14. [Read a bounded execution loop](../content/how-to/13.md)
15. [Save state and recover without duplicate work](../content/how-to/14.md)
16. [Follow traces and budgets](../content/how-to/15.md)
17. [Timeouts, cancellation and unfinished work](../content/tracks/harness/cancellation.md)
18. [Find evidence before asking for an answer](../content/how-to/05.md)
19. [Split documents without breaking their meaning](../content/tracks/retrieval/chunking.md)
20. [Understand semantic search before installing a database](../content/tracks/retrieval/semantic-search.md)
21. [Combine exact and semantic search](../content/tracks/retrieval/hybrid-search.md)
22. [Cite evidence and know when to abstain](../content/tracks/retrieval/grounded-answers.md)
23. [Understand what one agent hands to another](../content/tracks/multiagent/roles-and-handoffs.md)
24. [How to decide whether another agent would help](../content/how-to/19.md)

**Afterward:** Choose the Operate and evaluate path before deploying a real workflow. The complete student harness and MCP labs are available as optional implementation practice.

### Operate and evaluate AI systems

Test behavior and evidence, constrain permissions, investigate failures, and make measured release decisions. Includes the problems that demos rarely show.

**Before this:** Building controlled agents and Start from zero, or equivalent understanding of tool contracts, MCP, bounded loops, retrieval, and delegation. Reading requires no production deployment.

1. [Test an AI answer before trusting it](../content/tracks/evaluation/evaluating-outputs.md)
2. [Choose examples that reveal whether AI helps](../content/how-to/16.md)
3. [How to check whether an AI answer deserves to pass](../content/how-to/17.md)
4. [Check retrieval, evidence, and the final answer separately](../content/tracks/evaluation/grounded-retrieval.md)
5. [How to test the boundaries of an AI feature](../content/how-to/18.md)
6. [Decide whether an AI change is actually an improvement](../content/tracks/evaluation/regression-decisions.md)
7. [Tell instructions, evidence, and permissions apart](../content/tracks/security/trust-boundaries.md)
8. [Give an assistant only the access its task needs](../content/tracks/security/permission-scopes.md)
9. [Keep retrieved instructions from taking over a task](../content/tracks/security/injection-defenses.md)
10. [Debug an AI workflow without leaking its data](../content/tracks/security/secrets-and-logs.md)
11. [Inspect what you install before giving it access](../content/tracks/security/supply-chain.md)
12. [Make approvals match the action that actually runs](../content/tracks/security/approval-audit.md)
13. [How to keep several workers from losing each other's work](../content/how-to/20.md)
14. [Combine worker results without losing or inventing work](../content/tracks/multiagent/conflict-resolution.md)
15. [How to tell whether an agent team is worth the extra work](../content/how-to/21.md)
16. [Recover when only part of an agent team finishes](../content/tracks/multiagent/partial-failure.md)
17. [Follow one request through an AI system](../content/tracks/production/runtime-observability.md)
18. [How to move from a promising demo to a bounded service](../content/how-to/22.md)
19. [Budget time, tokens, retries, and useful outcomes](../content/tracks/production/cost-latency.md)
20. [How to investigate a failure without guessing the cause](../content/how-to/23.md)
21. [Release an AI change with a way to stop and recover](../content/tracks/production/releases-fallbacks.md)
22. [How to build a small project with your assistant, then grow it](../content/how-to/24.md)

**Afterward:** Choose one retained incident exercise, then a capstone when ready. Their answers remain behind recorded attempts and an explicit reveal.

