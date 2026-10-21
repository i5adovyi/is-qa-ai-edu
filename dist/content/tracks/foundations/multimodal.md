# Images, screenshots, and multimodal evidence

## Start here

You understand uncertainty and embeddings. Now consider a very practical SDET question: what can an assistant learn from a screenshot? You can read this lesson without an image-capable account. Its text-only example teaches the same evidence boundaries; uploading a synthetic screenshot is an optional extension.

## The idea in plain language

A **modality** is a kind of input or output, such as text, images, audio, or video. A **multimodal** model handles more than one kind. A **vision-language model** connects images and language, for example by describing an interface or answering a question about a chart.

An image can reveal visible layout, text, colour, and relative position. It does not automatically reveal the application’s internal state, network response, keyboard order, or screen-reader experience. **OCR**, optical character recognition, extracts visible text; it can misread small text or numbers. A visual model can also misinterpret a control or miss a subtle change.

For testing, separate a visual observation from a behavioural assertion. “The screenshot shows a red error message” is an observation. “The form correctly blocks submission for every invalid email” requires execution against cases. A screenshot may document one state without proving the transition that led there.

## A small example

Signal Desk’s synthetic screenshot description is: “A ticket form has Subject, Description, a grey Send button, and red text below Subject: Required.” The supplied requirement says the button should become available when both fields contain text.

From this description, you can discuss the required-field message and apparent disabled appearance. You cannot conclude that Send has the correct disabled attribute, that tab navigation skips it, or that filling both fields will enable it. Those checks need browser interaction, accessibility information, or code inspection. Even an actual screenshot cannot supply those facts on its own.

For a visual comparison, also record viewport, browser, zoom, theme, and data. A different line wrap may result from font loading or a narrower viewport rather than a product regression. A crop that omits those conditions can make a harmless difference look like a defect.

## Try it with Codex or Claude Code

Open chat through the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md). Use this prompt without attaching any private work image:

```text
Teach me how to use visual evidence in testing. This is a text description,
not an image you have inspected: a ticket form has Subject, Description,
a grey Send button, and “Required” below Subject. Requirement: Send becomes
available when both fields contain text.
Separate what the description supports from what needs interaction,
accessibility inspection, or code. Give one check for each missing kind
of evidence. Do not claim to have seen pixels or run a browser.
```

If your assistant supports image inputs, you may attach a harmless screenshot you created and ask it to compare the actual pixels with the description. Ask it to name unreadable regions rather than complete them from imagination. Use the product’s ordinary attachment flow; installation is not needed for the text route.

## What you should see

The answer should label the evidence type correctly. It should propose an interaction to check enabling, and an accessibility check for semantics. It should not convert “grey” directly into “disabled,” or claim that one screenshot proves responsiveness across screen sizes. If an image was not provided, it should explicitly work from the written description.

## If it goes wrong

When a label is misread, provide a clearer crop or the exact text as a separate source. When the assistant claims the button is clickable, request execution evidence. If a screenshot contains account names or secrets, use a synthetic reproduction instead. Image understanding is useful assistance, but visual guesses should not silently become assertions in your automated tests.

## Go deeper

Read the introduction and model concepts in Hugging Face’s [Introduction to Vision Language Models](https://huggingface.co/learn/smol-course/unit3/1). Stop before selecting or training models. This public reading requires no GPU or account. For choosing evidence rather than merely collecting it, revisit the [context guide](../../how-to/04.md).

## Optional practice

Ask for a new synthetic screen description and identify one supported claim and two unverified claims. Explain which additional evidence you would request. Submit your attempt before asking for feedback; no drawing or screenshot creation is required.
