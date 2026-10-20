# Review an agent incident

## User impact

What happened, who was affected, and what is known versus still uncertain? Use synthetic or appropriately redacted evidence.

## Timeline

| Time | Observed event | Evidence | Response |
| --- | --- | --- | --- |
| Fill in | Fill in | Fill in | Fill in |

## Containment and recovery

What stopped further harm? What state was preserved? What was rolled back or replayed? How did you verify that recovery did not duplicate a side effect?

## Contributing conditions

Inspect task definition, context, model decisions, tools, permissions, budgets, persistence, and evaluation coverage. Avoid attributing every failure to “the model hallucinated.”

## Corrective actions

Give each action an owner, a concrete change, and a verification check. A prompt warning alone is insufficient for a runtime authorization defect.

## Regression case

Add the smallest fixture that reproduces the incident. Explain how the new check would have caught it before release.
