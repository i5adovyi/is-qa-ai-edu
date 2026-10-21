# Why fluent answers can still be wrong

## Start here

Continue after tokens and context. You will learn why repeated requests can produce different answers and why confident language does not prove a claim. An SDET already knows that a passing demonstration is weaker than repeatable evidence; the same habit is useful with language models.

## The idea in plain language

A language model generates an output using patterns learned during training and the information supplied in its current context. **Training** changes the model’s learned parameters; **inference** uses those parameters to produce a response. Asking a question normally performs inference, not a new training run on your project.

During generation, several next pieces of text may be plausible. **Sampling** chooses among possible outputs according to the model and its configuration. A **temperature** setting, when supported, can change this selection process. Lower variation does not establish correctness, and the same settings do not guarantee identical outputs across every service or model version.

A **hallucination** is generated information that is unsupported or false. It can be a nonexistent API method, fabricated citation, invented test execution, or a confident guess about a requirement. Some wrong answers are ordinary misunderstandings of incomplete input. In either case, repeating “be accurate” does not supply the missing evidence.

## A small example

A synthetic bug report says: “The Save button did nothing on Firefox.” One answer claims a JavaScript error. Another claims the network request timed out. Both are possible explanations, but neither is observed in the report.

A stronger response distinguishes what happened from what might explain it: the user reports no visible result; the browser is Firefox; the console, request status, and expected behaviour remain unknown. It proposes checking one of those sources. This is useful even without a diagnosis because it moves the investigation toward evidence.

Now add “The server received the request and returned 403.” The network-timeout explanation becomes less plausible. The assistant should revise its answer when the evidence changes, rather than defend its earlier story.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
I am learning how to assess AI answers. Use this synthetic report only:
“The Save button did nothing on Firefox.”
List observed information separately from two possible explanations.
For each explanation, name one observation that could support or weaken it.
Do not invent logs, percentages, test results, or a definite root cause.
Then explain how “server returned 403” changes the investigation.
This is a teaching example; do not run tools or solve an academy assignment.
```

If you want to observe variation, repeat the first request in a fresh chat once. Treat the two outputs as examples, not a statistically meaningful benchmark. You do not need a temperature control or a second subscription to learn the distinction.

## What you should see

The response should label the two explanations as hypotheses. The new status code should influence the next check without magically proving which permission is missing. A credible answer can be uncertain and still be actionable. A confident answer can be wrong even when its terminology sounds professional.

## If it goes wrong

If you get a precise probability with no measurement, ask what data produced it. If the assistant says it “verified” an API, ask for the actual source or executed check. If it invents a log, remove that claim from the working context. Do not preserve a useful-looking fabrication in a handoff, where another session may mistake it for established evidence.

## Go deeper

Read Google’s [Introduction to Large Language Models](https://developers.google.com/machine-learning/crash-course/llm), especially “What is a language model?” and the discussion of problems with LLMs. Stop before the linked fine-tuning module. The full course has mathematical prerequisites; this selected conceptual reading does not require completing them. The [evaluation versus demo article](../../articles/evaluation-vs-demo.md) explains why repeated checks matter.

## Optional practice

Ask for a different synthetic failure report and classify three assistant claims as observed, inferred, or unsupported. Try first. Your tutor should explain only the mistaken classifications after you submit your reasoning; it should not expose incident debriefs.
