# Follow a twelve week study plan

Plan for two 90-minute study sessions and one three-hour build session each week. Add optional reading only after producing the week's artifact. The core route is approximately 72 hours of scheduled practice; actual completion time depends on experience and how far you take the capstone.

Check the [prerequisites and lesson-to-lab map](PRACTICE-MAP.md) first. Add preparation time if basic Python or terminal use is new. When assistant access is available, include the [model bridge](../lab/model-bridge.md) in week 1's prompt comparison and revisit it for week 7's evaluation; otherwise record those runs as not attempted and continue offline.

| Week | Focus | Required practice | Evidence to keep |
| --- | --- | --- | --- |
| 1 | Foundations, lessons 01-03 | Diagnostic and five-ticket baseline | Task contracts and initial experiment log |
| 2 | Context, lessons 04-06 | Conflicting evidence and compressed handoff | Before/after context packets |
| 3 | Tools, lessons 07-08 | Lab 01 and Lab 03 | Rejected malformed inputs and scope tests |
| 4 | Skills, lesson 09 | Lab 02 and a reusable skill | Activation table and three validated drafts |
| 5 | Development, lessons 10-12 | Bounded bug fix and review | Failing test, patch, passing check, handoff |
| 6 | Harnesses, lessons 13-15 | Lab 04 and Lab 05 | Timeout, exhausted-budget, and recovery traces |
| 7 | Evaluation, lessons 16-18 | Lab 06 | Frozen dataset, baseline comparison, failure taxonomy |
| 8 | Delegation, lessons 19-21 | Lab 07 | Worker briefs and single-vs-multiple-worker comparison |
| 9 | Production, lessons 22-23; lesson 24 proposal clinic | Lab 08 and selection of one capstone | Release criteria, incident scenario and proposal; the capstone is not yet complete |
| 10 | Capstone build | Implement smallest useful user journey | Working baseline and evaluation cases |
| 11 | Capstone hardening | Failure injection and fresh-case review | Incident report and measured revision |
| 12 | Capstone defense | Reproduce from a clean copy; explain to a reviewer | Final dossier and personal next-step plan |

Lesson 24's 90-minute estimate covers its proposal clinic. Its build and defense occupy weeks 10–12, with approximately 10–20 focused project hours depending on the chosen brief. Do not add a second full support capstone when choosing the QA or research route.

## A productive study session

Begin by recalling the last session without looking at notes. Read one concept and work through its example. Attempt the exercise yourself. Ask a tutor for a hint only when you can describe what you tried. End by recording a prediction for the next experiment. Leave a small, explicit next action so restarting does not require reconstructing your whole context.

## Weekly review

Spend 20 minutes answering four questions: What can I now do that I could not do last week? Which artifact proves it? Which misconception changed? Which failure remains unexplained? Move unfinished work to the next week; do not mark it complete because the calendar advanced.

## Shorter and longer routes

For six weeks, combine adjacent weeks and reserve 12-16 hours each week. For a slower route, split each week's study and build across two weeks. The stage gates stay the same. If you are already experienced, attempt a stage gate first and study only what the attempt reveals.

## Peer review without a cohort

Give a colleague one artifact and one rubric, not the entire repository. Ask them to reproduce a command and change one input. If nobody is available, use a fresh assistant session with only the submission and rubric, then manually verify its criticism. This is weaker than an independent expert review; treat its output as hypotheses to investigate.

## Retention practice

At the end of weeks 4, 8, and 12, redraw the system architecture from memory. Explain how context differs from authority, why retries need idempotency, and why a holdout cannot be used for repeated tuning. Revisit one earlier exercise with a new ticket. Transfer to a different input is stronger evidence than recognizing a familiar solution.
