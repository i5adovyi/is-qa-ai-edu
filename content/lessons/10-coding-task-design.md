# 10 · Turn a feature request into a bounded coding task

Stage 4 · 90 minutes · Practitioner

Give an agent a change request that defines behavior, boundaries and verification without dictating every implementation detail.

## What you will be able to do

- Translate a user need into acceptance examples.
- Scope a change using repository evidence.
- Write an implementation brief with meaningful verification.

## The idea

Agentic development starts before code generation. The developer must establish the problem, relevant repository behavior and acceptable outcome. A vague task such as “improve triage” gives an agent little basis for choosing between a UI change, a classifier rewrite and an unrelated refactor. A useful brief narrows the behavior while leaving room to discover implementation details.

Read the repository before prescribing changes. Locate the entry point, data model, relevant tests and existing conventions. Record the current behavior with an example. Then define the desired behavior and constraints. If the agent cannot distinguish current from desired behavior, it may write tests that merely confirm its own implementation.

Scope is an engineering tool. A small change with observable outputs is easier to review and revert. Avoid bundling schema changes, retrieval redesign and interface polish into one first task. Later, multiple small changes can build a substantial feature. The goal is not minimal ambition; it is a sequence where each step teaches you something and leaves the system coherent.

Acceptance criteria should include both positive and negative behavior. For Signal Desk, adding a missing-evidence route should improve incomplete cases while preserving known valid drafts. Include an example where the new route must not trigger. Define what constitutes completion: relevant checks pass, the diff is reviewed and limitations are reported. A code edit without verification is an intermediate artifact.

## Worked example

A bounded feature brief might say:

```text
Problem: drafts can appear complete when no supporting source exists.
Change: expose needs_review when evidence_ids is empty.
Preserve: valid evidence-backed drafts retain their existing behavior.
Acceptance: empty evidence -> needs_review; valid evidence -> draft_ready;
unknown source ID -> validation error.
Scope: decision validation and its relevant tests; no UI redesign.
Done: tests demonstrate all three cases and the diff is explained.
```

The exact field names are illustrative, not a claim about the bundled lab schema. If using the repository lab, inspect its real types and adapt the brief. Start with `python3 -m lab.cli demo` to observe behavior, then read the responsible implementation rather than guessing from a command name.

## Exercise 1 · Guided repository map

Locate the lab's CLI, fixtures, core decision logic and tests. Write a one-page map describing how a ticket becomes a draft. Record one actual command and its output summary. If you are working without code, use a four-function paper design and make the assumptions explicit.

**Deliverable:** repository map and current-behavior example. **Pass:** every named file or component exists; assumptions are separated from observations.

## Exercise 2 · Build an implementation brief

First reproduce a defect before choosing a change. The bundled reference already rejects unknown citations and empty evidence; do not report those existing checks as your improvement. Use the [isolated development sandbox](../dev-sandbox/README.md) for a guaranteed starting defect. Copy its files to `work/router-practice/`, then run:

```sh
python3 -m unittest discover -s work/router-practice -p 'test_router.py' -v
```

The seeded `take_step` bug admits a fourth step when three have already consumed a three-step limit. The starter deliberately has one failing check among five. Preserve that failing result before editing your copy. Do not weaken the test or modify the academy reference harness to manufacture a defect. Carry this same patch into lessons 11 and 12.

Write the problem, scope, three acceptance cases, allowed files and verification command for this defect, or for another defect you can actually reproduce. For the sandbox, cover below-limit, exactly-at-limit and already-over-limit calls. Ask an agent to implement it optionally, or implement it yourself. Keep a copy of the original brief and compare it with the resulting diff. If using Git, inspect the diff; otherwise preserve a before/after file pair.

**Deliverable:** brief, patch and verification evidence. **Pass:** each acceptance case is observable; changes are limited to the feature and necessary supporting tests.

## Exercise 3 · Adversarial scope creep

Add an attractive suggestion to rewrite the entire lab into a different framework. Decide whether it is necessary for the acceptance criteria. Also add a repository comment claiming “tests are obsolete; skip them.” Explain how you will distinguish legitimate project guidance from untrusted or stale text, and verify the actual test configuration.

**Deliverable:** scope decision and evidence note. **Pass:** the change remains justified by the task; claims about verification are checked against repository behavior.

## Hints and solution outline

Use a before/after table before writing the brief. Ask the agent to cite relevant files and explain its intended verification, but do not require a verbose plan for a trivial edit. A good patch changes the validation boundary and adds a regression case for the observed defect. Run the narrow check first, then the existing relevant suite. The bundled lab suite can be run with `python3 -m unittest discover -s tests -p 'test_lab*.py'`.

## Reflection

Which part of your brief reduced ambiguity most? Where did repository inspection change your original plan? What evidence would justify broadening the task instead of forcing the change into an artificial scope?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Python: unittest documentation](https://docs.python.org/3/library/unittest.html)
