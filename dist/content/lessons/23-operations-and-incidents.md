# 23 · Operate the system and learn from incidents

Stage 8 · 90 minutes · Advanced

Practice diagnosis, containment and learning so failures improve the system instead of becoming repeated surprises.

## What you will be able to do

- Triage incidents using traces and observable impact.
- Write a runbook with containment and recovery steps.
- Convert an incident into a regression case and ownership changes.

## The idea

Operations is the work of keeping the system useful after the demonstration. Failures may come from changed policy, unavailable tools, corrupted state, model behavior or an integration bug. The first goal during an incident is to understand impact and stop further harm. Root-cause analysis can follow once the system is contained.

A runbook should be executable by someone who did not build the system. Include symptoms, diagnostic queries or commands, containment actions, recovery checks and escalation ownership. Avoid instructions such as “investigate the AI issue” without saying where to look. Reference trace fields and artifact locations established in the harness lessons.

Distinguish symptoms from causes. A sudden drop in valid drafts could be a model change, a missing knowledge file or a validator rejecting a new schema. Check evidence before choosing the explanation. Compare affected and unaffected runs, locate the first failing boundary, and inspect recent changes. Preserve the relevant artifacts before rerunning or overwriting them.

An incident review should improve the system. Describe what happened, user impact, detection, contributing conditions and corrective actions. Assign owners and verification for each action. “Be more careful” is not an engineering correction. A new regression case, an atomic state update or a clearer deployment check can prevent recurrence. Do not claim that one patch eliminates every related risk.

## Worked example

After a knowledge refresh, Signal Desk marks most export tickets as needing review. The trace shows retrieval returning KB-EXPORT-3 while the validator's allowed-source set still contains KB-EXPORT-2. The system is failing closed, so unsupported drafts are blocked, but useful output drops.

Containment can restore the previous consistent knowledge-and-validator version. Recovery requires replaying affected tickets and checking that no drafts were silently lost. The root cause is a deployment consistency defect: two coupled artifacts were updated separately. The corrective action is to version and activate them together, plus add a mismatch test.

## Exercise 1 · Guided runbook

Write a runbook for “draft success rate drops after a policy update.” Include five diagnostic steps, a safe containment action, a recovery check and an escalation condition. State which data should be preserved before rollback. Use actual local trace paths where available or clearly marked illustrative paths.

**Deliverable:** runbook. **Pass:** another learner can follow it without your memory; the first steps inspect evidence rather than assume a model problem.

## Exercise 2 · Build an incident rehearsal

Simulate the knowledge/validator mismatch in a temporary copy or with scripted traces. Record detection time, affected cases, containment, recovery and unresolved questions. Re-run the affected evaluation cases after repair. The bundled lab's trace reader and evaluation command can help, but do not modify shared fixtures without preserving a copy.

**Deliverable:** incident timeline, repaired configuration and replay results. **Pass:** the system returns to a known consistent state; affected work is accounted for; recovery is verified by behavior.

## Exercise 3 · Adversarial incomplete evidence

Remove one trace event and add an operator note confidently blaming the model. Introduce a second unrelated slow tool call. Diagnose the incident without treating the note as proof or confusing the slow call with the first failing boundary. Record what cannot be concluded from missing evidence.

**Deliverable:** evidence-based diagnosis. **Pass:** the report distinguishes observations, hypotheses and unknowns; it does not invent a complete timeline when records are absent.

## Hints and solution outline

A useful timeline records UTC or clearly labeled local timestamps consistently. Start with the deployment version and the first validation error. Compare source IDs in retrieval output with the validator's evidence set. Roll back coupled artifacts together. The post-incident action should include an automated consistency check and a deployment manifest linking policy, knowledge and validator versions. Add the incident as a named regression case in the evaluation dataset, with its provenance and expected behavior.

For a real service, escalation and notification follow the organization's authorized channels. This exercise requires only a local incident record; it does not authorize contacting real customers or teammates.

## Reflection

Which missing trace field slowed diagnosis? What manual step was most error-prone? Which corrective action changes the system, and which merely documents a risk that remains?

## Related reading

These optional primary sources were checked on 20 October 2026. The lesson and exercises are original; reading is supplementary. Product interfaces can change.

- [Google SRE book: Service-level objectives](https://sre.google/sre-book/service-level-objectives/)
- [OpenTelemetry: Traces](https://opentelemetry.io/docs/concepts/signals/traces/)
