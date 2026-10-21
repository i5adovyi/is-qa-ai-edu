# Teach a task with a few examples

## Start here

You have learned to state a clear task and acceptance criteria. Sometimes a definition still leaves room for interpretation. A small example can show the intended pattern more clearly than another paragraph of instructions. This lesson teaches when examples help and how they can accidentally mislead you.

## The idea in plain language

A **zero-shot** request supplies no examples of completed input/output pairs. A **few-shot** request supplies a small number. The examples appear in the current context; they do not normally retrain the model’s parameters. They help communicate a category boundary, response format, or level of detail.

An example has two parts: an input and the desired output. Good examples match the written rule and include useful variation. If every urgent ticket mentions “login,” an assistant may learn the accidental pattern “login means urgent.” That is different from the intended rule “urgent means a confirmed outage affecting many users.”

An **evaluation case** checks behaviour after you design the request. If you put its answer directly into the prompt, success on that case is weak evidence of generalisation. **Generalisation** means handling new relevant cases rather than repeating demonstrations. Keep teaching examples separate from cases you use to assess improvement.

## A small example

Signal Desk classifies tickets as `access`, `billing`, or `other`. The rule says access concerns signing in or permissions; billing concerns charges or invoices. A useful pair might be “Cannot sign in” → `access` and “Invoice has the wrong tax number” → `billing`.

Now consider “I can sign in, but where is my invoice?” If all earlier examples contained only one topic word, the assistant may overweight “sign in.” A good demonstration includes the difference between mentioning a topic and reporting a problem about it. A clear unknown or ambiguous case can also show when the assistant should ask for clarification.

Examples should not contradict the policy. If the written instruction says to return `other` when unclear, but a demonstration invents a specific category, the model receives conflicting guidance. Fix the contract before increasing the number of examples.

## Try it with Codex or Claude Code

Open chat through the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Teach few-shot prompting with this synthetic classification task.
Categories: access means sign-in/permission problems; billing means charge
or invoice problems; other means neither is established.
Examples: “Cannot sign in” -> access. “Wrong invoice tax number” -> billing.
Explain the rule these examples demonstrate and one accidental shortcut
they could encourage. Add one different teaching example that clarifies
the boundary. Do not claim this trains model weights or proves accuracy.
Keep separate any new cases you propose for evaluation; do not answer them.
```

Read the proposed example against the written category definitions. If it reveals an ambiguity in your definitions, improve those first. You may continue learning without running a model comparison or creating a dataset file.

## What you should see

The response should explain why example diversity matters and identify a possible shortcut. It should keep unanswered evaluation cases separate. The demonstration should use the same output labels as the rule. It should not treat a request containing ten examples as universally better than one containing two.

## If it goes wrong

If the assistant copies a demonstration’s answer for a different situation, ask which rule supports that label. If it adds categories, restate the allowed choices. If a benchmark suddenly improves after its cases were included in the prompt, recognise that the test may no longer measure unseen behaviour. Avoid presenting that improvement as evidence of reliable production performance.

## Go deeper

Read “Zero-shot vs few-shot prompts,” “Optimal number of examples,” and “Consistent formatting” in Google’s [prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies). Stop at “Add context.” These conceptual sections are public and need no Gemini account. The retained [prompt experiment guide](../../how-to/03.md) explains how to compare a changed request.

## Optional practice

Ask your tutor for a category rule and two imperfect examples. Identify one misleading pattern, then propose a better teaching example. Submit it before asking for feedback; keep the tutor’s new evaluation cases unanswered until you attempt them.
