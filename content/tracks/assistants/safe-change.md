# Make one small change you can explain

## Start here

You have toured a repository. The next skill is controlling a small edit and checking what it did. This demonstration uses a disposable synthetic file under ignored `work/`; it must not repair the academy’s deliberately incomplete student code. You can read the example without executing it.

## The idea in plain language

A **patch** is a proposed change to file contents. A **diff** shows the before-and-after difference. A **test** compares observed behaviour with an expectation. These are separate evidence sources: a convincing patch description does not prove the patch was applied, and applied code does not prove it works.

The useful loop is to identify the requirement, inspect the current implementation, reproduce the problem, change only what is relevant, and verify the result. Before editing a real project, inspect existing changes so another person’s work is preserved. A small task does not require a complicated plan, but it does require a clear boundary.

Avoid teaching an assistant that green output is the only goal. Removing a failing assertion or changing the expected answer can make a test pass while leaving the defect. The intended behaviour is the standard against which both code and test are judged.

## A small example

A synthetic function says `return status < 500` to decide whether a ticket request succeeded. The requirement says success means an HTTP status from 200 through 299. **HTTP status** is a number returned by a web service to describe the result.

The current function treats 403 as success, which contradicts the requirement. A useful demonstration includes 199, 200, 299, 300, and 403 so the boundaries are visible. Those cases are teaching data, not answers to an academy lab. The assistant should explain the comparison before changing it and should keep the new example separate from course source.

## Try it with Codex or Claude Code

Use the editable project and [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md). Paste this when you choose execution:

```text
Teach a small edit in a NEW ignored directory under work/. Check the current
folder, instructions, Git status, and Python availability first. Do not touch
course source or any existing work directory. Create a tiny teaching example
is_success(status) initially returning status < 500. The requirement is 200–299.
Show a failing assertion for 403, then explain and apply the smallest correction.
Verify 199, 200, 299, 300, 403. Show actual commands, exit status, and the before/after
change. If Python is unavailable, explain the example without pretending it ran.
```

Before accepting execution, understand that it creates local disposable files and runs Python. It should not need a network connection or API key. On Windows the documented interpreter command may be `py -3`; let the assistant inspect the environment rather than blindly copy a macOS command.

## What you should see

You should see a real failing check before the correction and a passing boundary check afterwards. The requirement should remain unchanged. The assistant should show exactly which teaching file changed and keep unrelated source intact. If it only explains the example, that is a valid conceptual result, but it is not execution evidence.

## If it goes wrong

If it edits `lab/student.py`, stop and inspect the diff before any further change. Do not erase unrelated work to recover. If the failing test never failed, ask whether the setup actually represented the defective behaviour. If tests pass because the expectation changed, return to the original requirement. A large refactor for a one-line boundary error deserves a clear reason.

## Go deeper

Read “Limitations” and the adoption best practices in GitHub’s [Copilot Chat application card](https://docs.github.com/en/copilot/responsible-use/chat). The review-and-test principle applies beyond that product; you need not buy Copilot. See the academy’s [coding and workers lab](../../labs/13-coding-and-workers.md) only when you want more involved optional practice.

## Optional practice

Ask your tutor for a different boundary rule with a small defective example. Predict one failing case before letting the assistant edit. Attempt the reasoning yourself, then request a hint or feedback. Keep the student lab’s original challenge untouched until you deliberately choose it.
