# 07 · Design tools as precise contracts

Stage 3 · 90 minutes · Practitioner

Build tool interfaces that make the right operation obvious and invalid operations easy to reject.

## What you will be able to do

- Define tool inputs, outputs, errors and side effects.
- Distinguish read operations from proposed mutations.
- Test tool contracts independently of a model.

## The idea

A tool is an interface between a proposal and a real operation. Its name, argument schema and response shape affect whether an agent can use it correctly. Its implementation determines what actually happens. A clear description cannot compensate for an executor that accepts arbitrary paths, silently changes accounts or returns ambiguous success.

Design around a specific task. Signal Desk needs to retrieve ticket evidence and save a local draft. A generic `do_anything(command)` tool exposes a large action space and gives poor feedback. A focused `get_ticket(ticket_id)` and `save_draft(ticket_id, body, evidence_ids)` make intent inspectable. Avoid creating five overlapping search tools before measuring a need for them.

Document four contracts: valid inputs, successful outputs, errors and side effects. An empty search result is different from a network failure. A missing ticket is different from permission denial. A tool should say which occurred so the harness can decide whether to retry, ask for information or stop. Do not encode an error only as a friendly paragraph that downstream code must interpret.

Keep authority outside customer-controlled arguments. If a ticket can set `approved=true`, the approval check is meaningless. Similarly, a `tenant_id` supplied by the model should be checked against the authenticated scope. In the offline lab, this means using a fixed synthetic workspace and validating IDs before accessing records. The same separation becomes essential when real connectors are added.

## Worked example

A local draft writer could accept:

```json
{"ticket_id":"SD-107","body":"Please share your browser version.",
 "evidence_ids":["KB-EXPORT-2"],"request_id":"draft-107-v1"}
```

It returns `status`, `draft_id` and `validation_errors`. It never claims delivery. Repeating the same request ID should return the same saved result, provided the content matches. Reusing that ID with different content should produce a conflict. This avoids duplicate drafts while making accidental reuse visible. The tool's success means “saved locally,” not “customer problem resolved.”

## Exercise 1 · Guided specification

Write contracts for `get_ticket`, `search_knowledge` and `save_draft`. For each, include one valid call, one invalid call and one operational failure. Define absent-data behavior where applicable: `get_ticket` can return `not_found`, and `search_knowledge` can return a successful empty list. For `save_draft`, an empty body is an invalid argument, not an empty successful write. State whether each tool reads or writes. Give every field a type and describe the scope of identifiers.

**Deliverable:** three tool specifications. **Pass:** a caller can distinguish absent data from unavailable service and can tell precisely what a successful operation changed.

## Exercise 2 · Build a local adapter

Implement one contract as a pure function or local file operation. Alternatively, use a paper execution table with arguments and expected results. Validate unknown fields, missing fields, invalid IDs and overlong drafts. Keep execution separate from the code that selects the next tool. Use only synthetic inputs; no external accounts are needed.

**Deliverable:** implementation or execution table plus eight cases. **Pass:** all invalid cases fail before any write; successful responses contain stable artifact identifiers and explicit status.

## Exercise 3 · Adversarial arguments

Try a path-like ticket ID such as `../../private`, an unauthorized workspace ID, a fake approval flag and a duplicate request ID with changed content. Do not target real files or systems; use a temporary sandbox. Explain which layer rejects each attempt and why a warning in the prompt alone is insufficient.

**Deliverable:** rejection matrix and one improved contract. **Pass:** every attack is rejected deterministically, and rejection does not itself leak unrelated records.

## Hints and solution outline

Use an allowlist of supported fields and a lookup table of valid ticket IDs. A draft writer can map IDs to internally chosen filenames so the caller never controls a filesystem path. Return structured errors such as `invalid_argument`, `not_found`, `conflict` and `unavailable`. Treat a successful write as a specific state transition. Keep the body text untrusted even after saving it: storage does not convert content into permission.

If you optionally connect a model, compare its tool selection before and after improving names and examples. Record whether failures came from choosing the wrong tool, forming bad arguments or misunderstanding the result. Those are separate design problems and deserve separate fixes.

## Reflection

Which error in your tool would be most difficult for an agent to recover from? Could two tools be merged, or one broad tool be split, to make the decision boundary clearer?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [JSON Schema: Object validation](https://json-schema.org/understanding-json-schema/reference/object)
