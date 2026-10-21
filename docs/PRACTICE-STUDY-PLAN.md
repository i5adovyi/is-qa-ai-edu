# Follow a twelve week study plan — retained practice edition

The original schedule is preserved as an optional practical track. Its exercises, evidence requirements, and stage gates apply only when you choose that track. Start with the [guided SDET study plan](STUDY-PLAN.md) for explanations and selected readings.

Use two 90-minute study sessions and one three-hour build session per week as a scheduling scaffold. Its twelve weeks contain 72 calendar hours; they are not a guarantee that every exercise and extension fits. The differentiated lesson estimates separate reading, guided work, independent work, and optional extensions. Record actual pace before compressing the schedule. Add optional reading after producing the week's artifact.

Check the [prerequisites and lesson-to-lab map](PRACTICE-MAP.md) first. Add preparation time if basic Python or terminal use is new. When assistant access is available, include the [model bridge](../lab/model-bridge.md) in week 1's prompt comparison and revisit it for week 7's evaluation; otherwise record those runs as not attempted and continue offline.

| Week | Focus | Required practice | Evidence to keep |
| --- | --- | --- | --- |
| 1 | Foundations, lessons 01-03 | Diagnostic and five-ticket baseline | Task contracts and initial experiment log |
| 2 | Context, lessons 04-06 | Conflicting evidence and compressed handoff | Before/after context packets |
| 3 | Tools, lessons 07-08 | Lab 01 and Lab 03 | Rejected malformed inputs and scope tests |
| 4 | Skills, lesson 09 | Lab 02 and a reusable skill; lab 10 if using the installation extension | Activation table and three evidence-review artifacts, with structural checks and independent semantic review; host behavior remains pending until actually run |
| 5 | Development, lessons 10-12 | Bounded bug fix and review; Lab 13 Part A can start here | Failing test, patch, passing check, handoff |
| 6 | Harnesses, lessons 13-15 | Lab 04 and Lab 05 | Timeout, exhausted-budget, and recovery traces |
| 7 | Evaluation, lessons 16-18 | Lab 06 | Frozen dataset, baseline comparison, failure taxonomy |
| 8 | Delegation, lessons 19-21 | Lab 07; Lab 13 Part B after these lessons | Worker briefs and single-vs-multiple-worker comparison |
| 9 | Production, lessons 22-23; lesson 24 proposal clinic | Lab 08 and selection of one capstone | Release criteria, incident scenario and proposal; the capstone is not yet complete |
| 10 | Capstone build | Implement smallest useful user journey | Working baseline and evaluation cases |
| 11 | Capstone hardening | Failure injection and fresh-case review | Incident report and measured revision |
| 12 | Capstone defense | Reproduce from a clean copy; explain to a reviewer | Final dossier and personal next-step plan |

Add the [integration route](INTEGRATION-LABS.md) alongside this core schedule: lab 09 after week 3, lab 10 after week 4, and lab 11 after lab 08 in week 9. Reserve another 5–9 focused hours, either as additional sessions or one to two extra weeks. The original 72-hour plan does not include these new sessions.

Lab 08 supplies the decision helper used by the composed harness in Lab 11 and the later model/tool loop. Complete that bounded helper for the engineering integration route even if your final capstone is QA or research. It does not require building a second full support capstone.

For the real-life incident route, add the investigations below after their prerequisites. They are distributed through the course, so you practice diagnosing unfamiliar evidence before the final project. The original 72-hour scaffold does not include their full additional time.

| Placement | Investigation | Additional planning range |
| --- | --- | --- |
| Week 5, after Lab 13 Part A | [INC-01: The morning change request](../content/incidents/01-morning-change.md) | 90–120 minutes |
| Week 6, after Lab 05 | [INC-03: The interrupted update](../content/incidents/03-interrupted-update.md) | 75–105 minutes |
| Weeks 6–7, after lessons 07–09 and 13–15; revisit Lab 10 | [INC-04: The Monday workspace](../content/incidents/04-monday-workspace.md) | 75–105 minutes |
| Week 7, after the evaluation lessons | [INC-02: The weekly evidence brief](../content/incidents/02-evidence-brief.md) | 75–105 minutes |
| Week 8, after Lab 13 Part B | [INC-05: The busy afternoon](../content/incidents/05-busy-afternoon.md) | 90–120 minutes |
| Week 9, after lessons 22–23 | [INC-06: The resumed delivery](../content/incidents/06-resumed-delivery.md) | 75–105 minutes |
| Weeks 11–12, after your chosen product's working baseline | [INC-CAPSTONE: The release rehearsal](../content/incidents/07-release-rehearsal.md) | 150–210 minutes |

The six investigations total **8–11 hours**, with **2.5–3.5 hours** for the capstone incident. At six hours per week, reserve about two to three additional weeks for this route. If an incident replaces optional repetitive case authoring, record that substitution; keep the original stage gate. If the capstone incident fits inside your already reserved hardening time, count those hours once. Do not add all three capstones.

The order is INC-01, INC-03, INC-04, INC-02, INC-05, INC-06, then INC-CAPSTONE. Stable IDs are labels, not a prerequisite sequence. Each investigation begins with a neutral brief, a constrained evidence-gathering budget, and a first attempt. Hints and debriefs require that saved attempt and an explicit request. Use the [incident route](../content/incidents/README.md) for the CLI, evidence packet and assessment.

## Preparation and extension budget

Before week 1, reserve 15–25 minutes for [diagram and outcome entry checks](../content/onboarding/README.md), plus 20–40 minutes for the terminal check if choosing the engineering route. If functions, JSON, or terminal basics remain unfamiliar, allow additional preparation sessions. Do not delay the paper-based first lesson until programming feels fluent.

| Placement | Addition | Provisional additional time | Scope |
| --- | --- | --- | --- |
| Each lesson | Three applied checks, attempt/feedback record | 10–20 minutes | Use instead of some optional reading, or add time; do not count a quiz as practical mastery |
| Each stage gate | New-domain transfer and delayed recall | 20–40 minutes initially; 5–10 minutes per revisit | Record actual misconceptions and adjust spacing |
| Week 5 or later | Git/environment readiness and lab 13 coding mission | Lab 13 total below | Reproduce, patch, review, commit/revert, and resume; worker portion waits until week 8 |
| After week 9, lesson 16, and the lab 11 component gate; lab 09 for MCP | [Lab 12](../content/labs/12-model-tool-loop.md) | 85–145 minutes scripted plus actual MCP; optional live comparison 45–90 minutes | Preserve actual model usage as a separate evidence gate |
| After week 8 | [Lab 13](../content/labs/13-coding-and-workers.md), including its earlier coding portion | 2–4 hours total | Scripted independent processes first; actual assistant workers optional and separately labeled |
| After week 7 | [Lab 14](../content/labs/14-retrieval-comparison.md) | 90–150 minutes | Fixed corpus/query experiment, source scope, compression and refresh |
| After week 9 | [Lab 15](../content/labs/15-review-and-operations.md) | 90–150 minutes | Human review, release checks, pending work and rollback |
| Weeks 7–11 as relevant | [Three future-project missions](FUTURE-PROJECT-READINESS.md#three-short-missions-for-future-projects) | 30–60 minutes each, plus actual provider costs/time if selected | Environment/API diagnosis, controlled model migration, and new-data feedback |

Labs 12–15 add approximately 6.5–11.5 hours before optional actual model work; labs 09–11 add the separate 5–9 hours above. Applied checks and transfer add further time unless replacing optional reading. At six hours per week, reserve roughly two to four extra weeks for those integration labs and roughly two to three more for the incident route. That makes about **16–19 weeks** for the base plan plus both routes, before any additional preparation, applied-check, recall, future-project mission, or live-model sessions that do not fit into existing time. This is a planning envelope, not a measured completion promise. Revisit the calendar after observing your pace.

All durations are planning ranges, not results of measured learner trials. Use [the pacing log](../templates/pacing-log.md) and choose one extension at a time. Learners without a current model account can finish the concept and local engineering evidence while keeping live gates visibly pending.

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

Use the [eight transfer prompts and recall process](../content/assessment/transfer-and-retention.md). Select cards from errors in your own attempts. Start with the next available session; lengthen intervals after independent recall and shorten them after repeated errors or heavy hints. Preserve the old response and explain what changed. The schedule adapts to observed recall rather than declaring one fixed interval sequence universally optimal.

## Choose reading and media deliberately

The [short original walkthroughs and selected readings](../content/walkthroughs/README.md) provide a different-domain example, full text transcript, and pause points before your own attempt. Use one segment when stuck. There are no fabricated video timestamps and no requirement to finish all external courses before building.
