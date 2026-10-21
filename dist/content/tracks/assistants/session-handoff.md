# Resume work in a fresh assistant session

## Start here

You can inspect and review a change. Now learn how to continue after a chat becomes long, an account changes, or you return another day. The aim is continuity based on files and verified evidence. A short handoff is useful, but a document is not required merely to continue reading the course.

## The idea in plain language

A **handoff** transfers enough information for the next session to act responsibly: objective, current state, relevant files, established evidence, unknowns, and next step. **Reconciliation** means comparing that handoff with current reality before relying on it.

Different kinds of persistence are separate. A Git commit preserves tracked project files. A local database preserves application records. A browser profile may preserve hosted course progress. An assistant account may preserve chat history or product-specific memory. None automatically copies all the others when you log in somewhere else.

Durable project instructions explain how to work in the repository. Temporary investigation state describes a particular unfinished task. Mixing them makes instructions stale and can accidentally distribute private information. Store only appropriate shared rules in project instructions; keep personal progress, credentials, and private logs in their intended private location.

## A small example

A fictional handoff says: “The ticket classifier is ready. All tests pass.” The next session finds uncommitted changes and a newer failing test. The old claim is too broad and no longer establishes today’s state.

A better handoff says which command ran, at which revision, what passed, what was skipped, and which work remained. It may say, “Boundary checks passed on the disposable example; no external service was called.” The next session can inspect the files and rerun the relevant check if the state changed. This is useful evidence, even when its limits are explicit.

For learning, “I last read embeddings; I have not attempted the optional practice” is enough to orient a tutor. It must not transform that statement into certification or silently mark the portal complete. Reading position is a bookmark, not mastery.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste this synthetic handoff:

```text
Teach me how to resume safely from this fictional handoff:
“Yesterday we changed ticket classification. Tests passed. Continue.”
No files or commands are supplied here. Identify what is missing and show
a compact improved handoff with UNKNOWN placeholders rather than invented
facts. Explain what a new session should verify before editing. Distinguish
Git files, local course progress, browser storage, and assistant chat history.
Do not inspect my private data or mark learning complete.
```

When you actually switch sessions, use your latest saved position or supplied attempt. If you want a local assistant to inspect private progress, explicitly select that record and purpose. Do not ask it to infer progress from this repository’s historical verification notes.

## What you should see

The response should preserve unknowns and separate evidence from next steps. It should identify the need to inspect current files and changes, rather than rerun every historical command automatically. It should not claim that changing OpenAI accounts transfers a Claude Code session, browser storage, or a GitHub repository’s access permissions.

## If it goes wrong

If the assistant invents remembered work, ask which supplied evidence supports it. If it proposes committing a progress export, use the academy’s private backup workflow instead. If a saved check is older than relevant code changes, treat it as historical and verify the new state. If two handoffs conflict, inspect the underlying artifacts and ask about unresolved intent rather than silently combining both stories.

## Go deeper

Read the distinction between instruction files and automatic memory in Claude Code’s [project memory documentation](https://code.claude.com/docs/en/memory). Stop before configuration. Product memory behaviour is not an account migration guarantee. Use [Continue learning](../../../docs/CONTINUE-LEARNING.md) for tutoring and [New account](../../../docs/NEW-ACCOUNT.md) for this academy’s actual migration steps.

## Optional practice

Ask your tutor for a different incomplete handoff. Identify the smallest missing evidence needed to continue and one claim that must be rechecked. Try before requesting a worked handoff. A verbal explanation is enough.
