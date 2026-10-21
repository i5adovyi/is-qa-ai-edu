# Pack useful context without dumping everything

## Start here

You understand evidence selection and project instructions. Now learn what to do when there is more material than the assistant can use effectively. The goal is a sensible information selection, not maximum compression or a complicated document. You can practise entirely in chat.

## The idea in plain language

A **context budget** is the attention and capacity you allocate to instructions, task evidence, history, tool outputs, and the answer. Token limits are one constraint; irrelevant or contradictory information can also hurt a request that technically fits.

**Progressive retrieval** means reading information when it becomes relevant instead of loading every file at the beginning. **Compaction** shortens accumulated context, often through a summary. Compaction can lose qualifiers, failed experiments, source references, or unresolved questions. A summary is useful only if the next decision still has the evidence it needs.

Think in three groups: essential now, available to retrieve later, and inappropriate to include. The third includes secrets and irrelevant private records, not merely low-priority facts. A pointer to a source is useful only if the assistant can actually access that source when needed; otherwise supply the relevant excerpt.

## A small example

Signal Desk is diagnosing one Firefox test returning 403. Available material includes the access requirement, failing request, nearby log events, 80 unrelated feature documents, a week of passing logs, and a private customer export.

The requirement and exact failure belong in the current context. A documented environment or authentication setup may be retrieved next. Unrelated feature manuals can stay outside the request. The private export has no legitimate role in this synthetic diagnosis. “More context” would not make including it useful.

Suppose you shorten “support users may create tickets only within their own tenant” to “support users may create tickets.” You saved words but deleted the condition that may explain 403. **Tenant** means a separate customer or organisation boundary in a shared system. Qualifiers often carry more diagnostic value than a long general description.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and paste:

```text
Teach context budgeting for a synthetic failure: Firefox create-ticket
expected 201, received 403. Requirement: support users may create tickets
only within their own tenant. Available sources: requirement, request log,
authentication setup, 80 unrelated feature documents, passing logs, and a
private customer export. Do not request or read real private records.
Choose what belongs now, what to retrieve next if needed, and what to omit.
Show one misleading compressed summary and explain what it lost.
Do not invent exact token counts or a confirmed root cause.
```

Then ask which additional observation would change the next retrieval choice. A good answer should follow the investigation, rather than prescribe the same giant context packet for every task. You do not need to write a formal report or implement a retrieval system.

## What you should see

The assistant should preserve the tenant condition, distinguish evidence from background, and avoid including the private export. It should explain why a summary can be misleading even when its individual sentences sound reasonable. A proposed source read should answer a concrete uncertainty, not merely expand the context.

## If it goes wrong

If the assistant asks for the entire repository, narrow the question and ask which file would resolve it. If a tool result is truncated, retrieve the relevant portion instead of summarising unseen text. If compaction loses a decision, restore the original source or state that it is unknown. Do not silently turn a remembered summary into authoritative evidence.

## Go deeper

Read “The anatomy of effective context” and “Context retrieval and agentic search” in Anthropic’s [context engineering article](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents). Stop before long-task techniques. Public reading needs no provider account. The academy’s retained [context budgets article](../../articles/context-budgets.md) and [optional lab](../../labs/02-context-budgets.md) connect this to observable controls.

## Optional practice

Ask your tutor for a new question with six possible sources. Pick the first two and explain which uncertainty each resolves. Submit that selection before asking for a worked packet. An oral explanation is enough; drawing a diagram is unnecessary.
