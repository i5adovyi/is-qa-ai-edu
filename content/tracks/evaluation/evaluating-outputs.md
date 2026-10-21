# Test an AI answer before trusting it

## Start here

Begin here if you already understand what an AI assistant does but have never evaluated one. You need only this page and an existing Codex or Claude Code conversation. No Python, model API, dataset download, or testing framework is required. The [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) explains how to open a conversation and paste the demonstration.

Your goal is to separate three questions: did the output have the right shape, did it follow the task, and was its answer supported? An SDET already distinguishes a passing assertion from a working feature. Apply that same habit to an assistant's confident response.

## The idea in plain language

An **evaluation**, often shortened to **eval**, is a repeatable comparison between observed behavior and an expectation. A **test case** supplies an input and the conditions for accepting the result. The **oracle** is the basis for judging correctness: a requirement, a known calculation, a trusted reference, or a carefully defined human judgment.

Some properties are easy to check exactly. An output must contain a ticket identifier; a number must be within a range. Other properties need interpretation. A summary must preserve the customer's actual complaint without inventing a cause. That interpretation needs a **rubric**: concrete criteria that different reviewers can apply consistently.

Do not ask the producing assistant whether its own answer is good and treat its confidence as a test result. Another model's judgment is also fallible. Start with observable checks and inspect disagreements yourself. A model can help propose cases; a human still owns what correct behavior means.

## A small example

Signal Desk receives this synthetic report: “SD-52: Search returns no results after I choose French. English search works. Started this morning.” The task is to summarize observed behavior in one sentence without asserting a cause.

Output A says: “SD-52 reports empty French search results while English works; onset was this morning.” Output B says: “SD-52 is caused by a broken French search index and requires a rebuild.” Both look like plausible support summaries. Only A stays within the supplied evidence. B has invented both a diagnosis and a remedy.

Three useful checks are: the correct ticket ID appears, the language contrast is preserved, and no unsupported cause is asserted. These are separate checks because a sentence can satisfy one and fail another. Exact wording is unnecessary; different faithful summaries can pass.

## Try it with Codex or Claude Code

Paste the following into your assistant. This is a teaching demonstration, so seeing its worked comparison is appropriate. It does not reveal any retained course assignment answer.

```text
Teach me to evaluate an AI summary using this synthetic example only.
Report: SD-52: Search returns no results after I choose French.
English search works. Started this morning.
A: SD-52 reports empty French search results while English works;
onset was this morning.
B: SD-52 is caused by a broken French search index and requires a rebuild.
First explain expected behavior. Then check ticket identity, preservation
of observations, and unsupported claims separately for A and B.
Quote only the supplied evidence supporting each judgment.
Do not run commands, access tickets, or create files.
End by explaining what this tiny example cannot prove about a real assistant.
```

Read its comparison against the original report. If the assistant invents a requirement, ask it to identify where that requirement came from. This verification is the central activity, not copying its verdict into a document.

## What you should see

The explanation should accept faithful paraphrasing and reject the unsupported diagnosis. It should distinguish a formatting check from an evidence check. It should also say that two outputs tell you little about other languages, missing information, conflicting reports, or repeated runs.

When classifying many outputs, **precision** asks how many accepted outputs were actually acceptable; **recall** asks how many acceptable outputs you successfully accepted. A checker that rejects everything avoids false acceptance but is not useful. The right tradeoff depends on the consequence of each mistake.

## If it goes wrong

If the assistant scores only grammar, restate the task's evidence constraint. If it insists there is exactly one valid sentence, request a second faithful paraphrase. If it gives an unexplained “9/10,” replace that score with explicit pass/fail criteria and an “uncertain” option for genuinely ambiguous cases.

An empty response should be a recorded failure or abstention under an explicit rule, not silently removed from the total. Otherwise a broken system can appear better merely by answering fewer difficult questions.

## Go deeper

Read Google's [Accuracy, recall, precision, and related metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall), specifically Accuracy, Recall, and Precision. Stop before the end-of-page exercises. The prerequisite is understanding counts and fractions; public reading requires no account. Its classification terminology helps you reason about checker mistakes, although it does not by itself evaluate open-ended prose.

Next, learn to build representative cases in the retained [dataset lesson](../../how-to/16.md). The article [Evaluation versus a convincing demo](../../articles/evaluation-vs-demo.md) explains why a few appealing examples are insufficient.

## Optional practice

Give your tutor a new synthetic bug report and propose two acceptance criteria. Ask for one flawed summary to evaluate, with the tutor's verdict withheld until you attempt it. You can continue reading without doing this practice or saving an artifact.
