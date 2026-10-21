# Review AI changes beyond a green test

## Start here

You can ask for a small change and investigate a failing test. Now learn how to review the result. This is an advanced assistant habit, but it does not require memorising Git commands. Your job is to connect the changed behaviour to the requirement and evidence, then identify what remains unverified.

## The idea in plain language

A **diff** displays changes between two file states. Added lines commonly begin with `+`; removed lines begin with `-`. A **hunk** is one grouped region of change. Context lines help locate that region. A review should inspect the actual changed source, not just the assistant’s summary.

Git distinguishes working files, the **staging area** prepared for the next commit, and committed history. Plain `git diff` normally shows unstaged tracked changes; `git diff --cached` shows staged changes. New untracked files require separate inspection. Therefore, one empty diff does not prove that nothing changed.

Tests offer evidence about the behaviours they exercise. They cannot prove every requirement, and a weak test can confirm the same mistake as the implementation. A review asks whether the tests would fail for a realistic defect and whether the change altered assertions, disabled checks, or expanded its scope unnecessarily.

## A small example

A synthetic patch changes `assert response.status == 201` to `assert response.status < 500`. The author says it “handles more responses.” A test now passes with 403. The patch is small and green, but it weakens the requirement that successful creation returns 201.

Another patch adds a new helper with the correct condition but forgets to call it from the actual request path. Its unit test may pass while production behaviour is unchanged. Reviewing only the helper misses that connection. The useful question is: which executed path now behaves differently, and which check demonstrates that difference?

Also inspect what a test does not show. A synthetic fixture can confirm local branching without proving that an external service accepts the same request. A code review should make that boundary visible rather than inflate the verification claim.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and paste:

```text
Review this synthetic patch conceptually; do not edit or execute anything.
Requirement: creating a ticket succeeds only when the response is 201.
Before: assert response.status == 201
After:  assert response.status < 500
The author says the suite now passes with response 403.
Explain the changed behaviour, one concrete counterexample, and what the
passing test does and does not prove. Then explain how I would inspect
unstaged, staged, and untracked files in a real repository without deleting
or resetting any work. Keep findings tied to this requirement.
```

For real work, ask the assistant to read the actual diff and relevant surrounding code. Provide the requirement and existing test evidence. A second review pass can help, but two assistants agreeing is not independent runtime proof.

## What you should see

The review should identify the weakened success condition and the concrete 403 counterexample. It should avoid turning style preferences into correctness defects. For a real repository, it should report which changes it inspected and distinguish executed checks from recommendations. A finding should explain its trigger and impact clearly enough for you to reproduce or reject it.

## If it goes wrong

If the assistant says “looks good” after reading only a summary, request the actual patch. If a finding is vague, ask for the specific input and resulting behaviour. If it suggests resetting files to obtain a clean tree, stop; unrelated changes may belong to you. If it proposes many extra tests, select those that resolve a concrete uncertainty rather than mirror every line of code.

## Go deeper

Read the description and “Generating patch text with -p” in the [Git diff manual](https://git-scm.com/docs/git-diff). Skip the long options catalog. No GitHub account is needed for the reading. The academy’s [review and operations lab](../../labs/15-review-and-operations.md) adds optional practice with more realistic changes.

## Optional practice

Ask your tutor for a new two-line patch and its requirement. Identify one behaviour change before receiving the review. Request feedback on your reasoning, not a generic checklist. You do not need to publish a pull request to learn this skill.
