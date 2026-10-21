# Give AI enough information to help

A prompt describes the job. Context supplies the facts needed to do it. Making a prompt longer does not automatically improve it; removing ambiguity and supplying relevant evidence often does.

For an SDET, the most useful information is usually familiar: the expected behavior, the observed failure, the environment, and a small relevant slice of code or logs. Add constraints such as the test framework and whether the assistant may edit files or only explain them.

## A testing example

“Fix this flaky test” gives the assistant almost no basis for choosing a fix. A more useful request could be:

> This Playwright checkout test passes locally and fails in CI. Here are the failure message, trace excerpt, test, and CI browser version. Explain plausible causes and identify the next observation that would distinguish them. Do not change code yet. Flag missing information instead of inventing it.

This is an example to read, not an assignment. The important changes are the supplied evidence, the bounded task, and a clear distinction between investigation and editing. A role such as “act as a senior QA engineer” does not replace those details.

An output format helps when the result will be consumed by code. For example, a list of objects with `case`, `expected_behavior`, and `reason` is easier to validate than a loosely formatted essay. Valid JSON still does not prove the content is correct. Structure and meaning need separate checks.

## Why long conversations go wrong

Models process inputs as tokens: units that can be whole words, word fragments, punctuation, or other encoded input. A context window limits how much information can be considered in a request. Applications may select, truncate, or summarize history to fit. Earlier details can become unavailable or lose precision.

If a conversation has become confused, repeating “you already know this” rarely helps. Restate the current objective, the current code version, the actual evidence, and the next decision. This is the beginning of context engineering: deliberately selecting, organizing, and refreshing information as work progresses.

Do not include an entire repository when one failing test and its dependencies would do. Conversely, a tiny code snippet without its contract may encourage an incorrect assumption. Useful context is sufficient, relevant, and current.

## A boundary that matters at work

A log, ticket, or retrieved page can contain text that looks like an instruction. Its contents are evidence to inspect, not automatic authority to change your task or permissions. Share synthetic or approved data when learning; a private customer log is not made safe by putting it inside a prompt.

## Keep this idea

Before blaming the model, check whether it had the right task, facts, constraints, and expected output. Next, see how that changes the quality of generated tests. You can continue without writing a prompt of your own.
