# What AI can do for an SDET

Start with a familiar situation: a test fails in CI and passes on your laptop. An AI assistant can help you read the log, suggest explanations, or draft a test change. It cannot establish the cause simply by producing a convincing explanation. You still need the failing run, the relevant code, and a way to check the hypothesis.

This distinction is the foundation of the course: **AI helps you propose and investigate; evidence tells you whether the result is right.** You already use that judgment as an SDET. Learning AI builds on it.

## Four terms you actually need now

**A model** is the component that generates a response. A large language model, or LLM, learns patterns during training and uses its input to generate text or code. It can reason usefully about examples, but it can also invent a function, misunderstand a requirement, or confidently explain the wrong failure.

**An assistant** is the application around a model. It may add conversation history, file access, search, or the ability to run commands. A model's answer and a tool's execution result are different things. An assistant saying “the tests pass” is only a claim unless a test runner actually ran the relevant tests and returned that result.

**A prompt** is the request you give it. “Explain this failure using this log” is a prompt. So is “write a test.” The second leaves much more unspecified: which behavior, framework, fixtures, and expected result?

**Context** is the information available for the current response: instructions, messages, selected files, and tool results. A file existing somewhere in your repository does not mean the model has read it. An account remembering your preferences does not mean the assistant has the latest build log.

## Where this helps in your work

An assistant can turn a long failure log into a short timeline, suggest boundary cases you missed, explain unfamiliar test code, or draft repetitive setup. These are useful starting points because you can compare the output with something concrete.

Suppose a checkout test reports “element not found.” The assistant suggests adding a longer wait. That might hide the symptom. The page might instead be showing an authentication error, the selector might have changed, or the feature might be broken. The useful contribution is a set of plausible explanations and the evidence that would distinguish them. A larger timeout alone is not a diagnosis.

Be especially careful with generated expected values. If the assistant reads a buggy implementation and writes tests that reproduce its behavior, the tests may pass while protecting the bug. Requirements and agreed examples remain your source for what *should* happen.

## What you are learning toward

First, you will learn to use AI in ordinary testing work: giving useful context, reviewing generated tests, and checking claims. Then you will learn to test software that contains AI: answers can vary, retrieved evidence can be wrong, and an agent can choose the wrong action. Tools, MCP, skills, and harnesses come after those foundations.

You do not need to learn neural-network mathematics, buy a new subscription, install an agent framework, or draw a diagram to start. Reading this page is a valid first session. If a term is unclear, ask your tutor to explain that term using a testing example.

## Keep this idea

Treat a fluent AI response as a useful proposal whose important claims need checking. That is enough to continue to prompting and context. There is nothing to submit.

The selected external reading and its exact scope appear below in the portal. For plain-file reading, follow the [study plan](../../docs/STUDY-PLAN.md).
