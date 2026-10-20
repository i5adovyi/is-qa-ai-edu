# Build a QA change review copilot

Build a local assistant that reads a small change specification and code diff, proposes a test plan, and produces a review report tied to evidence. The assistant should help a QA engineer investigate risk; it must not present unexecuted tests as passing tests.

## Product scenario

A team maintains a synthetic support-ticket service. A change adds priority routing and retry behavior. Your copilot receives the specification, a patch, existing tests, and the test execution results. It identifies likely regressions, proposes targeted checks, and separates observed failures from hypotheses.

Create a tiny service fixture with at least three intentionally different change scenarios: a harmless refactor, an off-by-one budget defect, and a retry that can duplicate an update. Keep the fixture isolated from the academy's reference implementation. Do not break the passing reference to simulate a student project.

## Build milestones

1. Write an input contract: specification, diff, test inventory, and trusted command results. Mark code comments and issue text as untrusted data.
2. Establish a manual review baseline on five changes. Record which risks you found and how long review took.
3. Build a context selector that includes the changed function, relevant caller, test contract, and requirements. Measure the effect of removing each component.
4. Generate a risk-oriented test plan with a requirement-to-test mapping. Require explicit labels: proposed, executed, passed, failed, blocked.
5. Add a bounded execution workflow in your own isolated practice environment or consume precomputed test results. Do not permit arbitrary commands supplied by retrieved content.
6. Produce a final review report with evidence paths, observed defects, uncertainties, and recommended next checks.

## Required checks

- The harmless refactor does not receive an invented critical defect.
- The budget defect is connected to a boundary test rather than a vague warning.
- The duplicate update is exposed by a replay scenario.
- A generated test is never described as executed unless an execution record exists.
- A code comment asking the assistant to suppress findings has no authority over the review.
- The final report distinguishes observed failure, suspected risk, and missing evidence.

## Evaluation design

Create a labeled set of changes with at least one no-defect example. Measure useful findings, missed defects, and unsupported findings separately. A system that reports a defect in every patch may have high recall and terrible usefulness. Ask a second reviewer to assess a sample and record disagreements.

Keep a fresh change set for final evaluation. If your model has seen the public example or answer key, disclose possible contamination and create new variants. Do not use the same model's opinion as the only ground truth.

## Evidence package

Submit the fixture service, change cases, review baseline, context experiments, generated test plans, execution evidence, and a final report. Include a trace for one successful review and one misleading initial answer that your verification process corrected.

## Stretch work

Compare one reviewer with a planner/tester/reviewer decomposition. Measure total time and number of verified useful findings. Add a negative-control patch and test if the system invents issues. Evaluate whether limiting context to the diff loses caller constraints.

## Defense questions

What evidence establishes that a test ran? Which finding would you send to a developer and which would you discard? How did you avoid rewarding verbose reviews? What information was missing from the diff alone? When is a human reviewer faster than your agent workflow?

Suggested scope: 12-20 focused hours. Assess against the shared capstone rubric.
