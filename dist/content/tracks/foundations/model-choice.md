# Choose prompting, retrieval, or model adaptation

## Start here

You now know the basic limits of models, context, and embeddings. This lesson connects those concepts to a real decision: should you improve the request, supply better information, change the model, or train something? You can practise the decision with a fictional example without subscribing to additional services.

## The idea in plain language

A model choice begins with the task. A fast classifier, a code assistant, and an image reader have different requirements. **Latency** is how long you wait. **Cost** includes both model usage and the surrounding system. **Quality** must mean specific behaviour, such as correctly refusing to invent a missing policy, rather than “sounds intelligent.”

Several changes solve different problems. Better prompting clarifies the task and expected output. **Retrieval-augmented generation**, or RAG, supplies relevant external information at answer time. **Fine-tuning** further trains a model using examples to influence its behaviour. Training from scratch builds learned parameters through a much larger training process. None is a universal next step after a weak answer.

For frequently changing facts, supplying authoritative current evidence is usually the first question. For a stable output pattern, examples and evaluation may reveal whether prompting is enough. Fine-tuning does not automatically grant access to a live database or keep a policy current. A larger model also cannot reliably infer a private requirement you never supplied.

## A small example

Signal Desk wants to classify invented support tickets as `access`, `billing`, or `other`. It also wants to answer questions about the current refund policy. These are two different tasks.

The classifier needs explicit category definitions and representative examples, including ambiguous tickets. The policy answer needs the current applicable policy and evidence for each claim. If yesterday’s policy changed, buying a larger model is not a substitute for updating the source.

Before selecting anything, define a few acceptable behaviours: no invented category, uncertain cases marked for review, citations for policy claims, and an agreed response-time limit. Compare candidate approaches on the same cases. A good result on one carefully chosen example is not enough to justify a migration.

## Try it with Codex or Claude Code

Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Help me choose an approach conceptually; do not buy, install, or call APIs.
Signal Desk needs (A) classify tickets into access/billing/other and
(B) answer questions about a refund policy that changes weekly.
For each, explain when clearer prompting, supplied evidence/RAG,
or fine-tuning could address the problem. Name the evidence needed before
choosing. Use no current price or model-performance claims unless sourced.
Explain latency and evaluation in beginner terms. Stop before implementation.
```

Then ask which failure would *not* be fixed by switching models. This question helps you diagnose the system, rather than turn every weak result into a purchase decision. Your existing assistant is enough for the teaching discussion.

## What you should see

The answer should separate missing facts from unclear instructions and recurring behaviour problems. It should suggest evaluating relevant examples, including missing or conflicting policy evidence. A recommendation should explain its assumptions and tradeoffs. No model name should be treated as universally best, and model rankings should not be invented from memory.

## If it goes wrong

If the assistant recommends fine-tuning immediately, ask what labelled examples exist and why simpler approaches failed. If it recommends RAG for every task, ask whether an ordinary lookup or deterministic rule is enough. If a benchmark is cited, check whether its inputs and success criteria resemble your work. Public benchmark scores do not establish your system’s permission handling or factual correctness.

## Go deeper

Read Microsoft’s [Exploring and comparing different LLMs](https://github.com/microsoft/generative-ai-for-beginners/blob/main/02-exploring-and-comparing-different-llms/README.md), focusing on model distinctions and the prompting, RAG, and fine-tuning discussion. Stop before its knowledge check. Product examples illustrate categories; verify current availability separately before adopting one. Continue with the [evaluation guide](../../how-to/16.md) when you are ready to measure an actual choice.

## Optional practice

Ask your tutor for a new fictional AI failure. Choose one first intervention and explain what evidence would change your mind. Attempt the decision before asking for a worked comparison. A concise spoken answer is sufficient.
