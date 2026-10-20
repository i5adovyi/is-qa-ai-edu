# INC-04 — The Monday workspace

You resume a familiar workflow after an account change and a routine package update. Some saved material is available immediately; a later action behaves differently from the previous session. The user expects continuity without exposing unrelated information.

**Placement:** after lessons 07–09 and 13–15; revisit Lab 10's package and host evidence distinction. **Plan:** 75–105 minutes. **Requirements:** Python 3.9+. Identities and permissions are fictional fixture values; do not change a real account.

```sh
python3 -m lab.incidents init INC-04 --workspace work/incidents/INC-04
python3 -m lab.incidents run --workspace work/incidents/INC-04
```

Read the generated brief and contract. Establish the current request and execution environment before relying on material from the previous session.

## Your first attempt

Spend **20 minutes and eight evidence checks** comparing relevant observations. Offer two explanations for the changed behavior and a check with different predicted outcomes. Record what the current user has actually authorized.

Save your attempt before asking for guidance. Treat retained state as evidence to assess, not automatic permission to use it.

## Work to submit

Implement the decision contract in `student.py`. Produce an environment comparison that identifies which differences matter to the task and which do not. Demonstrate both an allowed case and a case where continuing would require a new decision.

Write a concise user-facing handoff explaining the outcome and a specific next action. Avoid a blanket request for more privileges. If package or dependency behavior changed, state which observed contract you verified; do not infer compatibility from a familiar package name.

## Evidence packet

- Initial scope and environment observations.
- Two explanations and a discriminating check.
- An artifact showing how current and retained information were treated.
- Actual boundary-check results and an explicit description of what the simulation cannot establish.
- A transfer prediction and a handoff with any needed clarification or stop condition.

The fixture does not authenticate real users or enforce an operating-system sandbox. Assess the simulated behavior and keep any actual host claims separate.

[Incident route](README.md) · [Assessment](ASSESSMENT.md)
