# Investigate a failing test with evidence

## Start here

You have seen a small safe edit. Now consider the messier case: a test fails and nobody knows whether the product, test, environment, or data is responsible. You will learn a narrow investigation loop before asking an assistant to “fix everything.” This lesson uses a fictional transcript, so execution is optional.

## The idea in plain language

A **reproduction** repeats the conditions that produced a failure. A **fixture** is controlled input or setup used by a test. An **exit status** is a process’s numeric outcome; zero conventionally means success, while nonzero means the command reported a failure. An assertion failure is different from a test runner that could not start.

If an assistant sees only the final red line, it may change the wrong thing. Useful evidence includes the command, working directory, runtime version, test name, expected and actual result, and relevant nearby output. Real workplace logs may contain credentials or private data; share a sanitised or synthetic reproduction.

A test can fail because the product violates its requirement, the test expresses the wrong requirement, a service is unavailable, or the environment differs. **Flakiness** means outcomes vary under conditions expected to be equivalent. Retrying until green does not explain the variation or establish that it is harmless.

## A small example

Synthetic transcript A says: `python3 -m unittest tests.test_ticket`, followed by `ModuleNotFoundError: ticket_sdk`. No assertion ran. Transcript B says the test ran, expected 201, and received 403. Both appear red, but their next investigations differ.

For A, inspect the documented environment and dependency configuration. For B, inspect the authentication fixture and the access requirement before changing an expected code. Neither transcript proves the application is defective. A third transcript that passes only when another test runs first suggests hidden shared state, which requires a different experiment.

The smallest useful experiment changes one suspected condition while preserving others. That gives you a chance to learn why the result changed. Changing the dependency version, test data, assertion, and timeout together hides the cause even if the suite turns green.

## Try it with Codex or Claude Code

Paste this in chat using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md):

```text
Teach failure triage using two synthetic transcripts, not a real project.
A: python3 -m unittest tests.test_ticket -> ModuleNotFoundError: ticket_sdk.
B: same command -> test_create_ticket: expected 201, actual 403.
For each, separate what ran, what is known, and what is unknown. Give one
small next check and what its possible outcomes would mean. Do not change
an assertion, install a dependency, or claim a root cause without evidence.
Explain fixture, reproduction, and exit status in ordinary language.
```

For a real chosen lab, replace the synthetic lines with the actual sanitised output and include the documented setup. Ask the assistant to reproduce the failure before editing, when execution is available and appropriate. Keep the observed result separate from its explanation.

## What you should see

The answer should identify A as a setup/import problem that prevented the intended test from running. For B it should retain uncertainty about authorisation and fixture state. A good next check distinguishes competing explanations. It should not recommend weakening the assertion just because 403 is the current output.

## If it goes wrong

If the assistant retries indefinitely, ask what new evidence a retry will produce. If it increases a timeout, ask whether there is evidence of slow successful work rather than a wrong selector or unavailable service. If it fixes unrelated failures, restate the chosen scope. If it reports “tests pass,” request the exact executed command, result, and any skipped tests.

## Go deeper

Read the debugging and testing recipes in Claude Code’s [common workflows](https://code.claude.com/docs/en/common-workflows), then stop before PR creation. These are examples of requests, not guarantees of diagnosis. The academy’s [traces and diagnosis lab](../../labs/07-traces-and-diagnosis.md) supplies optional deeper investigation practice.

## Optional practice

Ask for one new synthetic failure with two plausible causes. Choose the first discriminating check and explain why. Attempt that choice before receiving a hint. The tutor should not give you an incident’s hidden root cause as an example.
