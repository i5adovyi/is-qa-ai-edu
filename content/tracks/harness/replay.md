# Replay, resume and change identity

## Start here

This topic builds on checkpoints and observed traces. A **checkpoint** saves enough run state to continue later. A **replay** uses recorded information to reproduce or inspect behavior. The words sound similar but can describe very different execution. Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) for the conceptual example; the complete harness lab is a later optional route.

## The idea in plain language

Replaying stored tool results can help diagnose a decision without calling real services again. It tests behavior against that recording, not the current external world. Resuming a live run may perform new operations from a saved point. The harness must know which actions are already complete, which remain uncertain, and which budget has already been consumed.

**Execution identity** describes the code, configuration, fixtures, and relevant dependencies that gave the saved state its meaning. A **fingerprint** is a compact identifier derived from selected information. It can detect a mismatch, but only for the information actually included. A checksum is neither a signature nor a complete security boundary.

Changes can make old state incompatible. If a new policy interprets an old status differently, blindly resuming may skip a required check or repeat a write. **Migration** transforms saved data according to a deliberate compatibility rule. Sometimes the honest choice is to finish with the old code or start a new run rather than pretend every checkpoint can be upgraded automatically.

## A small example

Signal Desk saves a checkpoint after recording an intended draft operation but before confirming its outcome. Later, someone changes the operation-key function. Resuming with the new function could create a different identity for what was originally the same intent. The existing deduplication record may no longer protect against duplication.

A separate replay of the old recorded response might still be useful for inspecting the decision. It does not prove the new function works against the live store. The evidence label should say whether the run used recorded results, deterministic synthetic tools, or actual external calls.

## Try it with Codex or Claude Code

```text
Teach me replay versus resume using a fictional checkpoint. Do not run or edit.
Saved state: draft operation requested; outcome uncertain; one retry budget unit
already consumed. Since then, the operation-key function changed.
Explain why replaying recorded observations differs from resuming live actions.
List which identity and budget facts should be checked before a resume.
Explain fingerprint limitations and a reasonable response to an incompatible
checkpoint. Do not claim that restarting makes earlier effects disappear.
```

If you have the academy source open, you may also ask the assistant to point out the component binding described in the complete harness lab. Source inspection can explain the design without disclosing or completing your unfinished student functions.

## What you should see

The explanation should retain consumed budget and uncertainty across the pause. It should not regenerate an operation identity casually or infer that an old effect vanished. A mismatch should be reported before unsafe continuation. An actual resume test would need the saved state, relevant code identity, resulting trace, and authoritative effect count; a final message alone does not establish correctness.

## If it goes wrong

If the assistant calls recorded output a live integration test, correct the evidence label. If it resets a budget on resume, ask whether repeated restarts can bypass the limit. If it proposes editing the checkpoint by hand until it passes, require a documented compatibility rule first. If a fingerprint changes across runtimes, preserve both observations and inspect what the implementation binds; fingerprints can depend on more than visible source text.

## Go deeper

Read [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), the introduction and Checkpointer vs. store comparison, then stop before troubleshooting. It is one public framework example, not a required dependency. The academy's [complete harness lab](../../labs/11-complete-student-harness.md) documents its actual resume binding and limits; [the recovery guide](../../how-to/14.md) remains available for a simpler explanation.

## Optional practice

Ask your tutor for one proposed change between checkpoint and resume. Decide which evidence is needed before continuing, then request feedback. If you choose the runnable lab, keep its reference example clearly separate from your own student implementation and evidence.
