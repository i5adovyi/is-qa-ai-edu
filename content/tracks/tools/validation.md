# Validate inputs before anything happens

## Start here

Read the two beginner topics in this track first. You should recognize a tool name, its arguments, and the application's role. This lesson introduces **validation**: checking proposed input against explicit rules. It does not require writing a validator. Open Codex or Claude Code using the [quickstart](../../../docs/ASSISTANT-QUICKSTART.md) and use the supplied fictional data. Your first task is to notice which rule each input violates.

## The idea in plain language

Three questions belong at a tool boundary. Is the input shaped correctly? Does it make sense for this operation? Is this caller allowed to do it? A **schema** describes data shape, such as a required string field. A **business rule** describes meaning, such as a valid date range. **Authorization** decides whether the identified caller may act on the chosen object.

These checks complement each other. A ticket ID can be a valid string and still belong to another customer. A requested date can use the correct format and still fall outside the allowed reporting period. Asking the model to be careful is useful guidance, but the executing software must reject unacceptable requests independently. Otherwise a malformed proposal reaches the real system before anyone notices.

## A small example

Signal Desk's fictional `read_test_run` accepts `run_id`, a nonempty string, and `max_failures`, an integer from 1 to 20. Unknown fields are rejected. The caller is allowed to read only runs in project `demo-shop`.

`{"run_id":"demo-shop:42","max_failures":5}` fits these stated rules. Replacing 5 with `"five"` breaks the type rule. Adding `include_secrets:true` introduces an undeclared field. Using a run from another project may fit the schema while failing authorization. We have not executed any request; these are examples of decisions a boundary would make.

An SDET should inspect rejection behavior as carefully as success. A useful failure says which public rule failed without revealing another project's data. It should occur before the read or write that the rejected call requested.

## Try it with Codex or Claude Code

```text
Explain this fictional tool contract without executing tools or changing files:
read_test_run requires run_id (nonempty string) and max_failures (integer 1..20).
Reject unknown fields. Caller can read only project demo-shop.
Use these demonstration inputs:
1. {"run_id":"demo-shop:42","max_failures":5}
2. {"run_id":"demo-shop:42","max_failures":"five"}
3. {"run_id":"other-project:42","max_failures":5}
Explain shape, meaning and permission checks separately. Show where execution
would be blocked and which evidence would prove no operation happened.
Do not pretend a JSON schema alone implements access control.
```

If you want to see code afterward, ask for a tiny disposable demonstration and an explanation of every line. Keep that separate from the academy's student lab implementations so your own practice remains yours.

## What you should see

The assistant should explain a type failure separately from an access failure. It should identify a runtime observation, such as an unchanged synthetic call counter, that could demonstrate rejection before execution. A reassuring error message alone does not prove that order. This is the same testing instinct you use when verifying that a rejected API request did not still update a database row.

## If it goes wrong

If the assistant automatically converts `"five"` to 5, explain that this contract requires rejection; silent coercion changes the interface. If it treats missing and null as identical, ask it to show both cases separately. If it derives authorization from model-supplied project names, ask where the trusted caller identity comes from. Do not repair a rejected call by granting wider permissions.

## Go deeper

Read [JSON Schema's object reference](https://json-schema.org/understanding-json-schema/reference/object), specifically Properties, Required Properties, and Additional Properties. Skip Pattern Properties and Unevaluated Properties. The reading is public and requires no installation. Notice that listing a property and requiring it are separate choices. Continue with results and errors next; use the retained [tool-authority lab](../../labs/03-tool-authority.md) only when you choose implementation practice.

## Optional practice

Ask for one new input that violates exactly one rule. Classify the failure yourself and say what must remain unchanged. Let your tutor check the classification before adding multiple simultaneous faults.
