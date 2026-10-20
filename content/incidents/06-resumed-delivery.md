# INC-06 — The resumed delivery

You return to a task after a break. The handoff says the implementation is nearly complete, a worker returns another artifact, and two stakeholders react differently to the proposed result. The automated checks do not by themselves settle whether the delivery is useful.

**Placement:** after lessons 06, 12, 20 and 22–23. **Plan:** 75–105 minutes. **Requirements:** Python 3.9+.

```sh
python3 -m lab.incidents init INC-06 --workspace work/incidents/INC-06
python3 -m lab.incidents run --workspace work/incidents/INC-06
```

Read the generated brief and contract. Identify the user journey before deciding whether to accept the current artifact. Keep the original handoff and each source of requirements.

## Your first attempt

Use **20 minutes and eight evidence checks**. Give two explanations for the disagreement and identify one observation or narrowly worded question that would distinguish them. State which decisions you are authorized to make without asking.

Save your attempt before requesting a hint. Do not silently choose the stakeholder whose request is easiest to implement.

## Work to submit

Implement the generated decision contract in `student.py`. Produce a requirement-to-artifact comparison and a revised acceptance brief. Separate current confirmed requirements, conflicting claims, and your assumptions.

Write one clarification question that could change the delivery decision. Include your provisional action while waiting, with its limits. Then document how you would treat pending worker output and resume from the current evidence.

Do not invent a stakeholder reply. In the local fixture, use only the supplied observations. If they cannot resolve a decision, preserve that uncertainty.

## Evidence packet

- Initial handoff, current requirement sources and artifact observations.
- Two explanations and the discriminating check or question.
- Revised acceptance brief with any unresolved decision explicitly marked.
- Actual executable result plus a separate human usefulness review.
- A transfer prediction and handoff that someone else can resume.

The checker assesses the supplied decision contract. A useful real product still requires feedback from its actual users.

[Incident route](README.md) · [Assessment](ASSESSMENT.md)
