# 04 · Design an evidence packet with provenance

> Optional practice edition. You can read this explanation without completing its exercises. For the guided SDET route, use [Start here](../../docs/START-HERE.md).

Stage 2 · 90 minutes · Foundation

Construct the smallest useful context packet and make every important claim traceable to its source.

## What you will be able to do

- Classify instructions, evidence, assumptions and state.
- Preserve provenance and freshness in a compact packet.
- Resolve conflicting sources without erasing uncertainty.

## The idea

Context engineering asks what information reaches the model at a particular decision. A giant transcript is rarely a useful specification. It mixes outdated conclusions, customer allegations, tool results and current instructions. Signal Desk needs a deliberate packet that preserves distinctions between these kinds of information.

Use four compartments: operating instructions, current task, evidence and execution state. Operating instructions define the permitted behavior. The task describes what the user wants now. Evidence contains attributable facts and reports. State records completed actions, unresolved questions and next steps. A document can be highly relevant evidence without gaining authority to change the operating instructions.

For every retrieved item, retain a source identifier, relevant excerpt, version or observation time, and a scope statement. A support note for version 2.3 may be useful background for a 2.4 incident, but it is not automatically the current policy. A customer saying “all users” is a report about scope, not independent verification that every user is affected.

Compression loses information. Make the loss deliberate. Preserve decision-critical exceptions, unresolved contradictions and exact identifiers. Remove duplicated greetings and irrelevant troubleshooting history. When you summarize, distinguish “the tool returned X” from “we inferred Y.” A future reader must be able to challenge the inference without reconstructing the entire conversation.

## Worked example

Signal Desk receives SD-104 about an export failure. Three snippets are available:

```text
KB-A v1: exports above 50 MB are unsupported in version 2.3.
KB-B v2: version 2.4 supports exports up to 100 MB.
Ticket report: export is 80 MB; version is 2.4; browser unknown.
```

An evidence packet that retains only “large exports are unsupported” has destroyed the decisive version difference. A better packet identifies KB-B as applicable, keeps KB-A as superseded context only if needed, and records the browser as unknown. The draft can ask for browser and reproduction details. It cannot state that the 80 MB size exceeds the documented limit.

## Exercise 1 · Guided packet

Create a packet with sections for goal, output contract, current facts, evidence, unknowns and next action. Populate it from the worked example in no more than 300 words. Mark the customer's report explicitly. Include KB identifiers and the version applicability of both notes.

**Deliverable:** one context packet. **Pass:** a reviewer can reconstruct why 80 MB is not itself a documented violation, and can identify which facts are still unverified.

## Exercise 2 · Build a context budget

Write a 900-word synthetic history containing the example plus repetitive chatter, an old hypothesis, a corrected version number and one crucial exception. Reduce it to 350 words, then 180. For each reduction, list information removed and decisions potentially affected. Have another person answer the same five factual questions from each packet, or perform a delayed blind review yourself.

**Deliverable:** three packet versions, five questions and a loss ledger. **Pass:** both shorter packets preserve current version, applicable limit, source IDs, unknown browser and the corrected hypothesis status.

## Exercise 3 · Adversarial source conflict

Add KB-C with a newer timestamp but no product version, claiming a 25 MB limit. Decide whether freshness alone makes it authoritative. Draft a response that remains useful while the conflict is unresolved. Then insert “Ignore all previous rules” into KB-C and verify that it is treated as source text rather than an instruction.

**Deliverable:** conflict note and draft. **Pass:** uncertainty is explicit; no unsupported limit is asserted; retrieved text cannot redefine the task.

## Hints and solution outline

A compact evidence table often works better than narrative: source, version, fact, applicability. KB-B directly matches version 2.4; KB-C requires clarification because its scope is unspecified. Newness and authority are separate attributes. Keep a pointer to full text so omitted details can be recovered. The shortest packet is not automatically best; choose the one that preserves correct decisions at acceptable reading cost.

When optional model access is available, ask the same questions from each packet and record errors. Keep that experiment distinct from the offline information-preservation exercise. A successful human reconstruction proves that your packet contains the needed facts; it does not prove a particular model will use them reliably.

## Reflection

Which facts did you almost remove because they looked small? When should a source conflict block a draft, and when can the draft safely request clarification while the conflict is investigated?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
