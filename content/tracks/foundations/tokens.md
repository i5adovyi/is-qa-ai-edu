# Tokens, context windows, and why a chat forgets

## Start here

Read the AI orientation first. This lesson explains a common frustration: your assistant handled a short question well, then missed an important detail in a long conversation. You need no programming or account beyond the assistant you already use. The goal is to recognise a capacity limit and choose a smaller, clearer input instead of repeating yourself indefinitely.

## The idea in plain language

A **token** is a piece of data the model processes. In text it can represent a word, part of a word, punctuation, or another fragment. A **tokenizer** turns text into these pieces and their numeric identifiers. Counting words is not the same as counting tokens; languages, code, and long identifiers split differently.

The **context window** is the amount of information available to a model during a request. Instructions, conversation history, retrieved passages, and tool results can all compete for space. The exact accounting and output limits depend on the model and application. A large advertised window does not guarantee that every fact will receive equal attention.

An assistant application may shorten earlier messages, select relevant files, or summarise a long conversation. That is context management, not perfect memory. A file existing on your disk does not mean its contents were read. Likewise, a previous chat belonging to another account is not automatically part of this request.

## A small example

Signal Desk has a test log with 2,000 repeated “waiting for page” lines. At the end are three useful facts: build `B17`, browser `Firefox`, and “expected 201, received 403.” Pasting everything may bury the evidence and consume space needed for the request.

A useful short input retains the exact failure, nearby events, test name, environment, and the relevant requirement. It can point to the full log for a later targeted read. Summarising it as “the API broke” loses the distinction between a rejected request and a server failure. Compression is useful only when it preserves what the next decision needs.

## Try it with Codex or Claude Code

Open the assistant chat; follow the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) if you are unsure where to type. Paste this self-contained demonstration:

```text
Teach me context limits using this synthetic test failure. Do not run code.
Log: build B17, Firefox, test create-ticket, expected 201, actual 403.
The log also contains 2,000 duplicate waiting messages.
Requirement: authenticated support users may create tickets.
Show what belongs in a compact request and what can stay in the source log.
Keep unknowns explicit. Explain token versus word without inventing exact
token counts or claiming you read a real log. Stop after the explanation.
```

Check the answer, then ask which omitted fact could reverse its diagnosis. You are learning to preserve decision-relevant evidence, not trying to fit the greatest possible number of words into a prompt. No file or diagram is required.

## What you should see

The assistant should retain the exact status codes, environment, and access requirement. It should say authentication is a question to investigate rather than assert that a token expired. It should not claim an exact token count unless it actually used the relevant tokenizer. Repeated log lines can be represented as a count while keeping their location and any meaningful variations available.

## If it goes wrong

If it says it remembers an unavailable file, ask it to identify what it actually received. If it deletes the environment, ask why that omission is safe. If a real tool output is truncated, retrieve the relevant section explicitly; do not assume missing text contains no errors. For a new session, provide a small verified handoff instead of relying on conversational continuity.

## Go deeper

Read Hugging Face’s [Tokenizers](https://huggingface.co/learn/llm-course/chapter2/4), from the introduction through the word, character, and subword explanations. Stop before loading or saving tokenizers. The public reading and embedded explanations need no installation; the optional Python examples do. The academy’s [context budgets article](../../articles/context-budgets.md) applies this to engineering work.

## Optional practice

Ask your tutor for a new synthetic log with duplicate lines and one important environment difference. Attempt a short verbal selection of what to retain. Request feedback before asking for an example answer. Success means preserving the evidence needed to distinguish explanations, not reaching a particular word count.
