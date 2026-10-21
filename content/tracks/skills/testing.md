# Test whether a skill actually helps

## Start here

You now understand installation and invocation. This page introduces a small evaluation plan before asking you to run one. An **evaluation** compares observed behavior against stated expectations. You can discuss the plan using the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) without model access beyond your current conversation. Actual host trials are optional and should use synthetic fixtures and disposable workspaces.

## The idea in plain language

A skill has several independent quality questions. Was it available? Was it selected when appropriate? Did it follow the procedure? Was its answer factually supported? Did it stop correctly when required information was missing? Did it avoid unrelated actions? One green structural check answers only a small part of that list.

**Positive cases** should activate the workflow. **Negative cases** should not. A **regression case** captures behavior that must remain correct after a change. **Semantic checking** asks whether the result means the right thing, not merely whether fields exist. A JSON report can satisfy its schema while confidently asserting an unsupported root cause.

Use fresh sessions when comparing selection so earlier instructions do not leak into later trials. Record the package version and host/model identity when available. Compare the same inputs before and after a change. A handful of examples is useful local regression evidence; it is not a precise estimate of success across every workplace task.

## A small example

Imagine a skill that summarizes synthetic API failures. One case includes a status code and log excerpt. Another omits the endpoint. An unrelated case asks for a definition. A fourth includes misleading instructions inside the log. Expected behavior differs: summarize supported facts, ask a focused question, answer without the workflow, or preserve the log's status as data.

You should state those expectations before inspecting the assistant's answer. Otherwise it is easy to rewrite the criteria around whatever the model produced. An SDET already knows this trap from tests that assert an implementation's current output rather than a requirement.

## Try it with Codex or Claude Code

```text
Teach me to evaluate a fictional skill without running it or writing code.
Skill purpose: summarize a synthetic API failure using supplied evidence and
suggest one diagnostic check. It must not invent missing facts or make changes.
Show a small demonstration case and explain structural versus semantic checks.
Then explain how to compare version A and version B using the same cases,
fresh sessions, and recorded package/host identity. Do not reveal the academy's
installed-skill fixture answers. Distinguish simulated, observed and not-tested.
```

When you choose actual practice, use the [retained installed-skill lab](../../labs/10-installed-skill.md) and its documented artifact checker. Inspect its semantic expectations only after making your own attempt and deliberately requesting feedback.

## What you should see

The proposed comparison should separate activation from answer quality. A correct answer with the wrong skill selected is not a clean activation pass. A missing dependency should produce a clear blocked result, not invented replacement policy. If host access is unavailable, the report should leave behavior untested while still reporting successful package inspection accurately.

## If it goes wrong

If every test uses the exact phrase in the description, add paraphrases later; the original set may overfit selection. If the validator checks only keywords, inspect whether those words support the actual claim. If a prompt says “do not use the skill” in a negative-selection test, it changes what you are measuring. If retries are used, preserve the first result and report the retry policy instead of keeping only the best answer.

## Go deeper

Read [OpenAI's skill-building guidance](https://developers.openai.com/plugins/build/skills), specifically Define the workflow boundary and Test the skill. Stop before packaging. This public reading is useful across compatible hosts; it does not require publishing a plugin. The Evaluation track later covers datasets, rubrics, holdouts, and broader measurement in more depth.

## Optional practice

Write one positive case and one unrelated case for a skill you understand. Predict expected selection and one output criterion before running anything. Ask your tutor to review that pair first; expand the test set only after those boundaries are clear.
