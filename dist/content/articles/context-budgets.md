# Context is an engineering budget

**Stage 2 · Original field guide · 25-minute lesson plus a 45-minute experiment**

You ask an agent to diagnose a failed deployment. It receives a ticket, a thousand-line log, a project guide, an old incident report, a tool catalog and twenty previous messages. The answer sounds convincing. It proposes changing a timeout. Buried in the log, however, is a rejected credential. The failure is not necessarily an inability to understand authentication. The useful observation may never have become the center of the decision.

Context engineering means designing what information is available when a decision happens. A larger context window gives you more capacity. It does not relieve you of deciding what belongs there. Anthropic discusses context selection and persistent state as engineering problems, while the historical *Lost in the Middle* experiments show why the location of evidence is worth testing. Neither source establishes a universal performance curve for whichever model you use today. Measure your own workload. [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Lost in the Middle](https://arxiv.org/abs/2307.03172).

## Design the decision before the packet

Start with a question narrow enough to score: “Which failure category is supported by this deployment record, and which observation supports it?” That question needs different context from “Fix the repository and deploy it.” The first requires evidence and classification rules. The second additionally requires source files, allowed actions, validation commands and authority to operate infrastructure.

For the classification task, write a context manifest before writing a prompt:

| Information | Include now? | Reason |
| --- | --- | --- |
| Current task and answer format | Yes | Defines the decision |
| Relevant failure lines with timestamps | Yes | Supplies direct evidence |
| Environment and software version | Yes | Bounds interpretation |
| Complete build log | By reference | Available for follow-up |
| Earlier guessed explanations | Usually no | May anchor the next answer |
| Deployment credentials | No | Unnecessary for classification |
| Current policy on incident severity | Yes, dated | Determines business classification |

This manifest makes omission deliberate. A reference is useful only if the agent can actually retrieve it. A path to a file outside its environment is a dead end disguised as context.

## Use a budget that fits the experiment

Suppose you deliberately limit a packet to 6,000 tokens for a laboratory exercise. Reserve 800 for the task and output contract, 700 for project guidance, 2,500 for evidence, 500 for a handoff note, and 1,500 for tool descriptions and recent observations. These numbers are an experimental allocation, not provider recommendations. Count tokens with your selected model's supported tooling where available; character counts are only rough proxies.

The hard limit should leave room for generated output and tool responses. Many APIs distinguish input, output and combined limits. Read their current documentation before implementing a truncation policy. Never claim “under budget” solely because your hand-written document is short; hidden tool schemas, conversation history and repeated results also consume context.

Spend tokens on differences that can change the answer. A complete stack trace may be essential once. Five repeated copies seldom help. A tiny detail such as “this policy replaces version 2” can be more valuable than pages of background.

## Separate instructions, evidence and assumptions

A retrieved ticket can contain sentences that look like commands. Store it as evidence with an identifier, origin and timestamp. Explain its trust level in the surrounding application. The runner must enforce permissions independently; formatting a document as a quotation does not create a security boundary.

A compact packet might say:

```text
Task: classify DEP-047; do not modify files.
Allowed labels: configuration, network, application, unknown.
Evidence E1: current deploy log, collected 14:05 UTC, lines 88–94.
Evidence E2: release manifest, revision 67b0, service api-gateway.
Known: E1 reports credential rejection before health checks start.
Unresolved: whether the credential expired or was revoked.
Output: label, evidence_ids, uncertainty, next_read_only_check.
```

This supports a precise answer: the system can identify a likely category while preserving uncertainty about the cause. “Unknown” is a valid result when the evidence cannot distinguish possibilities.

## Summaries need a recovery path

A handoff note should preserve the goal, confirmed facts, decisions, rejected hypotheses with reasons, unfinished work and artifact locations. It should also preserve what has *not* been checked. “Tests pass” loses important information. “Ran the three parser tests at revision 67b0; integration tests were not run” is operationally useful.

Treat summaries as derived artifacts. Keep references to the original evidence so a later worker can recover details. When a summary conflicts with a current file, inspect the file and record the correction. Do not let a confident summary silently become the authoritative source.

Avoid copying every previous thought into memory. Store decisions and evidence. Your future agent needs to know that a timeout was ruled out because the authentication failure happened first, not every speculative route explored before that conclusion.

## Run a context ablation

Create five deployment records with known causes. Build three packet versions: complete logs, selected evidence with references, and selected evidence with one crucial observation removed. Keep the task and scorer unchanged. For each version, collect the label, valid supporting evidence, time, input size and any unsupported claim.

Repeat each condition several times if using a live model. Randomize case order and use fresh sessions to reduce accidental carryover. A cheaper packet that loses the only decisive evidence is not an improvement. A smaller packet that performs equally well is promising, but five cases are insufficient to establish broad reliability.

Add a position test: move the same fact to the beginning, middle and end without changing its wording. Add a contradiction test: supply an older policy and a newer one with clear effective dates. These probes reveal whether your system handles the information organization you actually intend to use.

## Submission and review

Submit the manifest, three packet variants, raw results and a short decision record. The reviewer should be able to reproduce which evidence each answer saw. Pass when your selected packet preserves the decisive information, distinguishes facts from guesses and supports recovery after a fresh session. The strongest result is a documented tradeoff, not a claim that one prompt format is always superior.
