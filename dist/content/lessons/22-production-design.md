# 22 · Design a production boundary and service contract

> Optional practice edition. You can read this explanation without completing its exercises. For the guided SDET route, use [Start here](../../docs/START-HERE.md).

Stage 8 · 105 minutes · Advanced

Translate a successful local prototype into a scoped operating plan with ownership, reliability targets and controlled rollout.

## What you will be able to do

- Define users, deployment scope and service-level indicators.
- Separate application permissions from model behavior.
- Plan staged rollout, fallback and rollback with measurable triggers.

## The idea

A prototype answers “Can this work?” A production plan answers “Under what conditions will we operate it, who responds when it fails, and how do we stop it safely?” You do not need to deploy a real service to learn these decisions. Signal Desk remains local and synthetic while you design the boundary explicitly.

Start with the user and supported task. For example, internal support staff receive evidence-backed local drafts for three ticket categories. State unsupported actions, such as sending messages or changing accounts, as part of the scoped product contract. This is not merely a warning; deployment credentials and available tools should reflect the scope.

Choose service-level indicators that correspond to user experience. Draft availability, completion latency and useful-draft rate measure different things. A request that returns quickly with an error may meet a latency target but fail availability. A technically valid draft may still be unhelpful. Define the denominator and measurement window for every indicator so results are interpretable.

Roll out gradually. Begin with replayed synthetic cases, then shadow operation on appropriately authorized data, then a limited user group if justified. A shadow run observes and proposes without taking the production action. Define promotion and rollback criteria in advance. Keep a fallback path, such as manual triage with the evidence packet, so the system can fail usefully.

## Worked example

A course-level operating contract might say:

```text
Users: internal reviewers in a synthetic demonstration.
Scope: create local drafts; no external sends or account changes.
Availability indicator: proportion of requests returning draft or useful review status.
Latency indicator: elapsed time from accepted request to terminal status.
Quality indicator: reviewed drafts meeting the evidence/usefulness rubric.
Rollback trigger: any unauthorized side effect or cross-scope evidence acceptance.
Fallback: save ticket and evidence packet for manual handling.
```

Set numerical targets only after measuring your environment. Arbitrary “99.99% reliable” claims do not become meaningful because they appear in an architecture document. For this course, use modest explicit exercise targets and label them as local learning criteria.

## Exercise 1 · Guided service contract

Write a one-page contract covering users, supported tasks, data scope, allowed actions, ownership, indicators and fallback. Define each indicator's numerator, denominator and observation window. Identify a case that should count as a useful review outcome rather than an unexplained error.

**Deliverable:** service contract. **Pass:** an operator can tell what the system promises and what events count against each target.

## Exercise 2 · Build a rollout plan

Design three rollout stages with entry criteria, exit criteria, data access and rollback procedure. Use your evaluation suite as the first gate. Include an explicit approval boundary before any real external integration; the exercise itself uses only local synthetic data. Rehearse disabling the agent and producing a manual handoff packet.

**Deliverable:** rollout plan and rollback rehearsal record. **Pass:** rollback is an executable sequence with an owner; disabling the system does not lose pending work.

## Exercise 3 · Adversarial metric interpretation

Create ten requests: six useful drafts, two useful review outcomes, one fast error and one timeout. Calculate availability, latency coverage and useful-outcome rate according to your definitions. Then change the definition to count every HTTP-like response as success and explain how it hides user failure.

Assign each request a synthetic start time and terminal time, and predeclare a timeout deadline. Retain the timed-out request in the ten-request denominator; record its deadline and missing completion instead of inventing a successful duration. Under the worked contract, eight of ten requests are useful outcomes, while nine have a non-timeout terminal response. Report both the useful-outcome count and the timing coverage, and state whether your latency statistic includes errors or censored timeout observations.

**Deliverable:** metric table and interpretation note. **Pass:** the original denominator remains explicit; missing or timed-out requests cannot disappear from the report.

## Hints and solution outline

A useful review outcome identifies missing evidence and the next action. It can count as an operationally completed request while still being separate from a successful draft. Keep those categories visible. Credentials should allow only the operations required for the rollout stage. A rollback can disable new runs, preserve checkpoints, reconcile pending writes and route work to humans. Test this sequence in the local sandbox before claiming operational readiness.

## Reflection

Who is responsible when a draft is technically valid but misleading? Which target would be easiest to game? What evidence would justify expanding from draft creation to a real action?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Google SRE book: Service-level objectives](https://sre.google/sre-book/service-level-objectives/)
- [OpenTelemetry: Traces](https://opentelemetry.io/docs/concepts/signals/traces/)
