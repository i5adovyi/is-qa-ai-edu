# Version and test a tool interface

## Start here

You have seen input rules, returned evidence, and uncertain effects. Now imagine changing a tool while several assistants still use its previous description. **Compatibility** means existing supported callers continue to work according to their contract. This lesson teaches what to compare before an interface change. Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) for a conversation-only walkthrough; no repository edits are required.

## The idea in plain language

A tool's interface includes more than its name. Inputs, defaults, permissions, output fields, error behavior, pagination, and side effects all affect callers. A small code change can be a large behavior change. Making an optional field required breaks old calls even when the function name stays identical.

A **contract test** checks an agreed boundary between components. It can verify that a recorded valid request still receives the expected shape and meaning, and that invalid requests remain rejected. A **fixture** is controlled example data used by such a test. The fixture should encode the behavior you promise, not every incidental sentence the model happened to write.

Versioning makes changes distinguishable. A version label is useful only when you can connect it to the actual schema and implementation. A cached tool description from yesterday may conflict with today's server. The resulting failure is often misdiagnosed as the model becoming less intelligent.

## A small example

Signal Desk's original `list_checks` accepts `build_id` and returns check names. A proposed revision adds required `project_id`, changes `passed` to `success`, and makes results paginated. Each affects a different consumer assumption: constructing requests, interpreting a status, and deciding whether results are complete.

Adding an optional output field may be compatible for a tolerant reader, but a strict consumer that rejects unknown fields may still fail. “Additive” is not a universal compatibility guarantee. You need the producer and consumer contracts together. This is familiar API testing applied to the boundary between a model, its host, and a tool service.

## Try it with Codex or Claude Code

```text
Review this fictional tool change without editing files or running tools.
Old: list_checks(build_id) returns {checks:[{name,passed:boolean}]} and all checks.
New: list_checks(build_id,project_id) requires both arguments and returns
{checks:[{name,success:boolean}],next_cursor:string-or-null} one page at a time.
Explain the three independent compatibility risks in plain language.
Suggest small contract checks and a migration sequence that lets an old caller
continue safely. State assumptions about unknown fields and cached descriptions.
Do not invent a provider-specific versioning mechanism.
```

After reading the review, ask which single check would fail first for an unchanged caller. You are learning to locate the boundary, not to write an entire migration framework.

## What you should see

The answer should address request construction, output interpretation, and pagination separately. It should propose an explicit compatibility period or distinct interface when needed, then verify both old and new consumers. A useful plan includes how to detect use of the old contract before removing it. It should preserve permission checks during migration rather than treating compatibility as a reason to accept anything.

## If it goes wrong

If the assistant only compares JSON syntax, ask about behavior: does “all checks” still mean all checks? If its proposed test copies the implementation's output without an independently stated expectation, ask what regression it would catch. If a rollout fails, inspect the actual tool inventory and schema visible to the caller. Refreshing discovery may fix stale metadata, but it cannot repair a genuine incompatible server change.

## Go deeper

Revisit [JSON Schema's object reference](https://json-schema.org/understanding-json-schema/reference/object), specifically required and additional properties. Stop after those sections. This public reference explains shape constraints; compatibility conclusions in this lesson also depend on the stated application behavior. The next subject, MCP, shows how descriptions and schemas travel across a real integration. The retained [authority lab](../../labs/03-tool-authority.md) remains available for focused practice.

## Optional practice

Ask a tutor for one small proposed tool change. Predict whether a specified existing caller breaks and identify one observation that would confirm your prediction. Try first, then request feedback. Avoid using a real production migration as your first experiment.
