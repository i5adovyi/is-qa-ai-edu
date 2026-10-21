# Combine worker results without losing or inventing work

## Start here

Read roles, delegation, and shared state first. **Shared state** means information multiple workers can read or update. This lesson explains how simultaneous work can conflict even when every worker is trying to help. You need only an assistant conversation and the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), not Git expertise or a running agent framework.

Your goal is to recognize when combining results requires a decision. “Merge everything” is not a meaningful correctness rule.

## The idea in plain language

Two workers can start from the same version and produce incompatible edits. This is a **concurrent update**: work happens before either worker has seen the other's result. A **stale result** was produced against an older version of the relevant inputs. It may still be useful, but it must not silently replace current information.

A **merge policy** states how results are combined. Appending independent observations may be appropriate. Adding numbers may be appropriate for independent counts. Selecting a final decision usually needs an owner and evidence. Applying one policy to every field creates subtle errors: concatenating two incompatible conclusions does not resolve them.

Use narrow ownership when possible. One worker can inspect tests while another inspects documentation, with the coordinator owning the final patch. Separate branches or worktrees isolate file edits, but they do not guarantee semantic compatibility. A clean Git merge can still combine a new API with a test expecting the old behavior.

## A small example

Signal Desk's baseline requirement revision R4 says that a blank filter means “show all.” Worker A proposes rejecting blanks to fix an apparent validation gap. Worker B adds a test asserting that blanks show all, citing R4. Their changes may touch different files and merge without a textual conflict, but they disagree about intended behavior.

The coordinator checks the actual requirement before deciding. It does not pick the newer message or the more confident worker. If revision R5 now says blanks are invalid, both workers need that revision and their relevant checks must be rerun. The coordinator should preserve useful investigation evidence even when an edit is rejected.

## Try it with Codex or Claude Code

```text
Explain a semantic conflict without changing any files.
Synthetic requirement R4: a blank search filter means show all records.
Worker A, based on R4, proposes rejecting blank filters.
Worker B, based on R4, adds a test expecting all records for a blank filter.
Both edits apply cleanly to different files.
Explain why a clean merge is insufficient. Identify the decision owner,
the evidence to consult, and which checks matter after choosing behavior.
Then explain what changes if an authorized requirement R5 makes blanks
invalid. Keep the R4 and R5 cases separate; do not invent a real R5 file.
```

Check that the assistant preserves the scenario's version distinction. If it switches to R5 halfway through without saying so, it is demonstrating the same context problem you are studying.

## What you should see

The result should distinguish a text merge from agreement about behavior. It should identify R4 as the supplied source of truth in the first case and treat R5 as a separate hypothetical. It should require relevant verification against the combined result, not reuse tests from an earlier independent worker checkout as proof of the final state.

A useful result record includes the input revision, claimed change, tests actually run, limitations, and unresolved conflicts. These fields need not become a formal report for the learner; they are the information a coordinator needs to avoid guessing.

## If it goes wrong

If workers repeatedly edit the same file, narrow ownership or serialize those edits. If a task depends on another worker's result, wait for that dependency or explicitly use a stable interface. Parallelizing a dependency does not remove it.

If a result is stale, compare the changed inputs before deciding whether to reuse it. If the merge drops observations, keep worker outputs separately and derive the accepted state from them. If the coordinator chooses by vote, ask whether the votes have independent evidence. More agreement does not repair a shared wrong premise.

## Go deeper

Read LangGraph's [Use the graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api), specifically Define and update state and Process state updates with reducers. A **reducer** is a rule for combining updates. Stop before MessagesState; focus on the combining rule, not Python syntax. Public reading needs no account. Executing examples requires framework installation and is optional.

The retained [coding and workers lab](../../labs/13-coding-and-workers.md) offers hands-on work after understanding the idea. The [delegation brief](../../../templates/delegation-brief.md) can help make ownership explicit.

## Optional practice

Ask your tutor for two short worker recommendations based on different revisions. Identify which evidence must be refreshed and who should decide. Try before requesting the tutor's resolution; no repository changes are required.
