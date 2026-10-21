# Ask for structured results and validate meaning

## Start here

You can improve an ordinary-language request. Now learn what changes when software must consume the result. A human can understand “looks like an access problem,” but an automated workflow may need fixed fields. You will learn the difference between a correctly shaped response and a correct decision.

## The idea in plain language

**JSON** is a text format for structured data. An **object** groups named fields, such as `category` and `evidence`. A **schema** specifies allowed fields and value types. A **validator** checks a result against those rules. A string such as `"access"` is text; `null` can represent an explicitly missing value when the contract allows it.

Three checks are different. **Parsing** asks whether the text is valid JSON. **Schema validation** asks whether it has the required shape. **Semantic validation** asks whether the meaning follows the evidence and task rules. A perfectly valid object can still contain a fabricated root cause or an unauthorised action.

Some model APIs offer mechanisms that constrain output shape. A chat request saying “return JSON” is not automatically the same mechanism. Even a constrained format does not guarantee factual correctness. Your surrounding application must also handle refusal, missing evidence, truncation, tool errors, and unsupported outputs without pretending they are successful decisions.

## A small example

Signal Desk wants a result with `category`, `evidence`, and `needs_review`. An invented ticket says, “I cannot sign in.” A possible teaching result is:

```json
{"category":"access","evidence":"I cannot sign in.","needs_review":false}
```

That object shows the format. It does not prove a real classifier ran. If the result instead includes `"root_cause":"expired password"`, the extra field may violate a strict schema and the fact is unsupported. If the ticket says only “Help,” forcing a precise category encourages invention; the contract needs an allowed uncertain outcome.

The meaning of `needs_review` must also be defined. Does it mean missing information, a risky action, or low confidence? A field name alone cannot settle that policy. Define the decision before asking the model to serialise it.

## Try it with Codex or Claude Code

Open chat via the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md), then paste:

```text
Teach structured output using synthetic ticket classification.
Fields: category is access/billing/other; evidence is a copied phrase or null;
needs_review is true when the ticket lacks evidence for a clear category.
Explain JSON, schema, and semantic validation before showing examples.
Compare “I cannot sign in” with “Help”. Show one valid teaching object and
one valid-JSON object whose meaning is unsupported. Explain the difference.
Do not claim a schema guarantees truth or that an API was called.
```

You may ask the assistant to point to each field in the example. You do not need to install a validator yet. In later tools and harness tracks, you can inspect real validation code that enforces allowed arguments and outcomes.

## What you should see

The explanation should separate syntax, shape, and evidence. The ambiguous input should not acquire a fabricated detail. It should use a real JSON boolean (`true` or `false`) rather than a quoted word when the contract requires a boolean. It should describe the limits of a conceptual example honestly.

## If it goes wrong

If a parser fails, inspect whether prose or code fences were included where raw JSON was expected. If parsing succeeds but a decision is wrong, examine task semantics rather than changing punctuation. If a retry invents missing evidence to satisfy required fields, allow an explicit unknown state. Never execute a model-suggested action solely because its JSON was well formed.

## Go deeper

Read “Properties,” “Required Properties,” and “Additional Properties” in [Understanding JSON Schema: object](https://json-schema.org/understanding-json-schema/reference/object). Skip pattern matching and composition initially. Public reading needs no installation. The academy’s [tool contracts guide](../../how-to/07.md) shows why structured arguments also need authority checks.

## Optional practice

Ask your tutor for one valid-looking object and its source ticket. Decide separately whether it parses, fits the stated schema, and is supported by evidence. Try each judgement before asking for feedback; do not turn this into a full programming assignment unless you choose to.
