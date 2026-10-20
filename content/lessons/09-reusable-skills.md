# 09 · Package a skill that improves repeatable work

Stage 3 · 90 minutes · Practitioner

Turn a successful Signal Desk procedure into a discoverable, testable skill with a clear activation boundary.

## What you will be able to do

- Write skill metadata that identifies when the procedure applies.
- Separate concise instructions from supporting references.
- Test activation, execution and non-activation cases.

## The idea

A skill packages reusable procedural knowledge. It can contain instructions, references, scripts and assets. Its purpose is to make a repeatable task easier to discover and perform. A skill is not automatically a new permission source, a reliable executable program or a substitute for evaluating the results.

Start with a procedure you have performed successfully. For Signal Desk, “produce a grounded troubleshooting draft from a ticket and knowledge snippets” is narrow enough to test. “Be an amazing AI assistant” is not. The description should identify both the task and the circumstances in which the skill applies. Overbroad descriptions cause irrelevant activation; narrow descriptions can hide useful behavior.

The Agent Skills format uses a directory with a `SKILL.md` containing metadata and instructions. Keep the main procedure concise enough to understand quickly. Put detailed policy examples and long reference material in separate files. Reference them at the step where they become useful. Progressive loading should reduce irrelevant context, not conceal essential constraints until after an action occurs.

A skill must describe completion. “Analyze carefully” leaves no observable endpoint. “Save a draft with evidence IDs, list missing facts and run the draft validator” is reviewable. If your skill uses a script, document its inputs, dependencies, outputs and failure behavior. A script that works only on your machine is an undocumented dependency problem, not a prompting problem.

## Worked example

A minimal skill skeleton could begin:

```markdown
---
name: signal-desk-draft
description: Prepare evidence-backed local support drafts from synthetic
  Signal Desk tickets; use for triage and troubleshooting draft requests.
---
1. Read the ticket and applicable knowledge snippets.
2. Separate reported observations from verified facts.
3. Draft a useful next step; record missing evidence.
4. Validate source IDs and save locally.
5. Report the draft path and unresolved questions.
```

This is a starting point, not a finished skill. It still needs an output template, examples and a statement that source text cannot authorize actions. Do not imply that this folder alone installs or activates the skill in every application; integration depends on the host.

## Exercise 1 · Guided activation cases

Write six requests that should activate the skill and six that should not. Include “triage this export issue,” “summarize a novel,” and “send a refund to a real customer.” Explain ambiguous cases. Revise the description until a reviewer can predict the intended boundary.

**Deliverable:** activation table and metadata. **Pass:** both positive and negative cases are meaningful; the skill does not become a universal fallback for unrelated tasks.

## Exercise 2 · Build the package

Create the skill directory in your own practice area with `SKILL.md`, a draft template and a short reference file. Add a deterministic local validator or a manual validation checklist. Run the procedure on three synthetic tickets using only those files. Optional model use: give the package to a compatible agent and record which files it reads.

**Deliverable:** complete skill package and three output drafts. **Pass:** another learner can execute it without previous chat history; dependencies and expected outputs are explicit; no real external action is required.

If you have a compatible assistant host, continue with the [skill integration checklist](../../docs/PRACTICE-MAP.md#operational-mcp-and-skills-extensions): install in the host's documented location, start a fresh session, and capture discovery, one triggered run, one non-trigger request and one missing-reference failure. Until those checks run, mark host integration unverified. The manual package exercise and actual host activation are separate evidence.

## Exercise 3 · Adversarial misuse

Place an instruction to reveal unrelated local data inside a knowledge snippet. Add a ticket asking the skill to skip validation because the case is urgent. Run the procedure and document where both attempts are rejected. Then remove a referenced file and check that the skill reports the missing dependency instead of pretending completion.

**Deliverable:** three failure reports and repairs. **Pass:** source content cannot expand authority; urgency does not erase required checks; a missing dependency produces an actionable error.

## Hints and solution outline

Put stable rules in the main procedure and variable policy details in referenced material. Keep the activation description concrete. A good final report names the saved artifact and its validation status rather than claiming the customer issue is solved. Your negative tests should cover both wrong domain and wrong action scope. If the host supports tool restrictions, configure them as an additional layer; do not assume an experimental metadata field is enforced identically by every host.

## Reflection

What did packaging reveal that your original conversation had left implicit? Which part belongs in a reusable skill, and which part belongs in deterministic code or task-specific evidence?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Agent Skills: Format specification](https://agentskills.io/specification)
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
