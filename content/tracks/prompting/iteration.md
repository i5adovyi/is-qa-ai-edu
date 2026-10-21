# Improve a prompt one failure at a time

## Start here

You can define a task, add examples, and recognise untrusted instructions. Now learn to improve a request when the output disappoints you. The first step is to name the failure precisely. “Make it better” may produce a different answer without fixing the problem you actually care about.

## The idea in plain language

A **prompt revision** changes the instructions or supplied context. A **failure mode** is a recognisable way the result violates its intended behaviour: invented facts, missing categories, excessive detail, incorrect formatting, or an unsupported action. Different failure modes need different interventions.

If the answer invents a requirement, provide the authoritative requirement and allow an unknown outcome. If it is verbose, define the necessary fields or stopping point. If it makes the wrong decision despite a clear rule and sufficient evidence, more adjectives may not help; inspect the examples, model capability, or surrounding workflow.

Change one meaningful part at a time when you want to understand the cause of improvement. Keep the input and success criteria stable for comparison. A model response can vary, so one favourable rerun is an observation rather than proof that the revision reliably works.

## A small example

Original request: “Summarise this failed test.” Synthetic input: “Firefox; create-ticket; expected 201; actual 403; no server log supplied.” The assistant answers: “An expired token caused the failure.” The problem is an unsupported root cause, not merely an unfriendly tone.

A targeted revision asks for “observed result, possible explanations, and missing evidence” and says not to turn a hypothesis into a confirmed cause. Adding “You are the world’s best QA expert” does not supply evidence for token expiry. Adding a hundred irrelevant log lines can make the request harder to follow.

After the revision, use a different failure where the cause is actually known. The assistant should still report established causes when evidence supports them. A prompt that labels everything unknown may avoid false claims while becoming unhelpful. Improvement requires preserving useful behaviour too.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and paste:

```text
Help me debug a prompt using this synthetic example, without running tools.
Request: “Summarise this failed test.”
Input: Firefox; create-ticket; expected 201; actual 403; no server log.
Bad answer: “An expired token caused the failure.”
Name the specific failure, propose one targeted prompt revision, and explain
what evidence is still missing. Do not invent a better log. Then suggest one
different case that could reveal a regression, but leave its answer for me.
```

Read the proposed revision before trying it. You should be able to explain which sentence addresses the failure. If you decide to compare outputs in your assistant, preserve the original request, revised request, and actual outputs privately. You do not need a hosted evaluation product for this first comparison.

## What you should see

The assistant should identify an unsupported causal claim and propose an evidence-sensitive structure. It should not claim the new prompt is guaranteed. The follow-up case should check another important behaviour rather than repeat the same example with a different identifier. A good explanation makes the tradeoff visible.

## If it goes wrong

If the revision grows into a huge instruction block, ask which lines address observed failures. If it changes the task itself, return to the original outcome. If the assistant improves one output by copying its expected answer into the prompt, test a new case. If the failure involves missing tool access or wrong data, fix that layer instead of repeatedly rewriting instructions.

## Go deeper

Read the introductory discussion of nondeterminism and evaluation, plus the relevant-context guidance, in OpenAI’s [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering). Skip API setup and model-specific recipes. Public reading requires no credits. Continue with the retained [prompt experiments lesson](../../how-to/03.md) for paired comparisons and held-out cases.

## Optional practice

Ask your tutor for one faulty output and its input. Identify the failure mode and propose a single revision before seeing an example answer. Your tutor should test your reasoning with a different case, not silently mark the prompt reliable.
