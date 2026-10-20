# Learning experience review and proposed additions

Reviewed 20 October 2026, after the learner's first tutoring session.

**Conclusion:** the academy has substantial coverage of agent engineering and unusually explicit distinctions between simulations, working integrations, and measured model behavior. Its next revision should improve the progression from a first attempt to independent performance, then connect the existing components to live model-driven execution.

This is the original review and implementation roadmap. Its eight workstreams have since been implemented; see the [implementation record](LEARNING-EXPERIENCE-IMPLEMENTATION.md) for the delivered files, verification, and remaining empirical checks. The findings below describe the pre-change edition and are retained to explain the decisions.

## Scope and evidence

This pass read all 24 lesson texts; inspected the eleven-lab sequence and component/integration requirements; reviewed setup, prerequisites, assessment, study planning, the tutor prompt, the model bridge and provider-adapter brief; and examined the portal's rendering, quizzes, and progress model. Selected lab instructions, capstone briefs, and library material were inspected in greater depth.

The repository contains 72 lesson exercises, eleven lab guides, and 43 resource entries. The library already provides an essential route, vendor routes, and follow-up tasks. The assessment manual already includes scoring anchors, oral defense, and reassessment. The study plan already includes weekly reflection and retention exercises. These should be extended rather than recreated.

Checks performed in this pass:

- `python3 scripts/check_content.py` passed its lesson, lab, quiz, resource metadata, and local link/section checks.
- A Node VM reproduction invoked the actual portal Markdown renderer on all eight component-lab hint pages. Every page produced zero functional collapsible sections and three escaped `<details>` opening tags. Lesson 01's heading-based hint section produced one functional collapsible section as a control.
- Curriculum inspection found exactly one multiple-choice question per lesson and a predictable sequence of correct-answer positions. The sequence is deliberately omitted here to avoid spoiling learner attempts.
- Portal state inspection found lesson completion, document notes, selected quiz answers, resource bookmarks, and self-assessed stage gates; no exercise-attempt history or structured feedback records.

This was a learning-design and content review, not a repeat of the earlier fresh-clone execution or external-link audit. No new claim is made that every exercise was completed, every external resource was consumed, or a live provider integration was tested.

## 1. Repair progressive hints and reconcile the learning route

**Priority: immediate.**

The [component-lab hints](../content/labs/hints/01.md) use raw HTML `<details><summary>` sections. The portal renderer in `portal/app.js` escaped that HTML in the reviewed edition. Opening a hint page exposed all three hint bodies together, despite the course's promise of progressive help. This mattered directly to a learner who asked for a small hint without the solution.

Support a deliberately narrow, safe disclosure format, or convert the hint content to a format the renderer supports. Keep each level independently closed and keyboard accessible. Do not solve this by allowing arbitrary raw HTML.

Two content inconsistencies also need repair:

- Lesson 08's objective in [curriculum metadata](../content/curriculum.json) still asks for a protocol-shaped offline simulator. The [lesson itself](../content/lessons/08-mcp-request-lifecycle.md) now teaches an actual SDK exchange. The portal displays the stale objective.
- Week 4 in the [study plan](STUDY-PLAN.md) asks for three validated drafts, while the revised [skill lesson](../content/lessons/09-reusable-skills.md) and [installation lab](../content/labs/10-installed-skill.md) produce evidence-review artifacts. Align the named submissions.

**Completion check:** on all eight hint pages, no hint body is initially visible; revealing the first hint leaves the other two closed. Lesson objectives and scheduled submission names agree with the actual exercises.

## 2. Add a short beginner preparation module and scaffold the first stage

**Priority: highest learning benefit.**

The learner's actual feedback was: “I'm not sure how to start the diagram.” [Lesson 01's guided exercise](../content/lessons/01-systems-before-agents.md#exercise-1--guided-map) simultaneously asks for six boxes, labeled data flows, a human boundary, model-versus-code judgments, a rationale, and a five-line contract. These are reasonable final deliverables but a large first step.

Add a preparation module with three independent entry checks:

1. Interpret a tiny diagram: boxes represent responsibilities; arrows represent information crossing between them.
2. Distinguish a model response from a tool result and a verified outcome, using an unrelated worked example.
3. For the coding route, run a command, find its output file, edit a JSON field, and identify a failed assertion. Add a small Python/terminal catch-up worksheet for a failed check.

Break the first exercise into checkpoints: one relationship, its data label, another relationship, the complete flow, then the contract and explanation. Use a blank worksheet and a worked example from another domain. Preserve the learner's responsibility for solving Signal Desk.

Many later exercises ask learners to author both fixtures and expected answers: eight knowledge notes in lesson 05, twelve cases in lesson 16, ten drafts in lesson 17, and eight comparison tickets in lesson 21. Authoring is valuable, but it can overwhelm a learner who is still acquiring the underlying concept.

Supply a small starter fixture pack for initial practice, then require learner-authored cases for transfer. Separate provided examples from final evaluation cases.

**Completion check:** a beginner can produce the first small artifact without viewing the target solution, explain what each notation means, and identify the next step. Record observed time and requests for help during a learner trial.

## 3. Make feedback and mastery visible in the portal

**Priority: high.**

The [assessment manual](ASSESSMENT.md) is stronger than the portal's assessment workflow. Currently, the portal can record a completion tick and a quiz choice, but it cannot preserve the sequence of attempt, feedback, revision, and reassessment.

Add an exercise workspace containing:

- Stable exercise ID and the current requested step.
- Learner attempt and supporting artifact references.
- Hint level requested, feedback, revision, and remaining misconception.
- Status such as not started, attempted, needs revision, or reviewed.
- Separate labels for self-review, tutor feedback, and reproduced execution evidence.
- Export/import of the complete learning record, preserving older attempts.

The existing tutor prompt already describes progressive help. Add a “prepare tutor packet” action that packages the exercise, pass criteria, learner attempt, and requested help level. It must exclude solution sections and instructor reference code by default. This can work by copying text into an available assistant; a hosted tutoring backend is not required.

Expand the current one-question-per-lesson checks with short explanations, trace interpretation, prediction questions, and new-case application. Use plausible distractors and avoid predictable answer positions. Add annotated weak, adequate, and strong submissions using different scenarios so learners can calibrate their scoring without copying the assigned answer.

**Completion check:** a learner can resume with their last attempt and feedback intact; a tutor receives no hidden solution; a correct quiz choice alone cannot be displayed as verified practical mastery.

## 4. Connect the harness to actual model-driven tool use

**Priority: highest technical addition after the learning support.**

The current [complete student harness](../content/labs/11-complete-student-harness.md) connects all eight student components to a working fixed workflow. This is a valid and useful achievement. The [model bridge](../lab/model-bridge.md) replays one saved model decision, and the [provider adapter](../lab/provider-adapter-design.md) is explicitly an implementation brief. [Lesson 13](../content/lessons/13-agent-loop-state-machine.md) correctly explains that arbitrary next-tool proposals require a separate implementation.

Add an integration lab with two clearly separate gates:

1. **Scripted planner gate:** a supplied planner interface proposes a next action; the harness validates and dispatches it, returns an observation, and decides whether execution can continue. Provide starter code and fault fixtures.
2. **Optional live-model gate:** implement a provider adapter against current official documentation. Record real model identity, request configuration, measured latency, and available usage metadata. Exercise malformed output, refusal, rate limit, timeout, repeated action, cancellation, and premature completion.

Reuse the existing local MCP server for an evidence lookup within this path. Also provide an optional host-connection exercise showing discovery and use of that same server in an actual assistant host. A successful SDK client/server exchange and a successful model-selected tool call should have different evidence labels.

Teach practical model behavior at this seam: structured output versus semantic correctness, tokenization versus character counts, nondeterministic sampling, and repeated-run comparisons. Build on the existing context-budget material and tokenizer resources.

**Completion check:** at least one run contains a model-proposed tool call, a validated execution, an observed result, and a subsequent model decision. Scripted failures still terminate predictably; unsupported completion is rejected; actual provider measurements remain distinct from simulated accounting.

## 5. Add a complete coding-agent and multi-agent practicum

**Priority: high for the user's intended skills.**

Lessons 10–12 supply a real seeded bug, repair evidence, and review practice. Lessons 19–21 supply thoughtful delegation and coordination exercises. However, live coding-agent and multi-agent execution remain optional and are not supported by one complete, reproducible practicum.

Extend the coding sandbox into a small repository mission:

- Inspect project guidance, reproduce a defect, create a scoped change, and preserve the original failure.
- Compare an instruction file, a reusable skill, and a tool configuration by changing one at a time.
- Inspect a diff, make a commit, review a proposed patch, and rehearse reverting it.
- Interrupt the task and resume from a handoff in a fresh session.

Then add a real two-worker exercise with separate writable directories and an integration owner. Run the same cases with one worker and two workers. Supply fixtures for a stale result, duplicate completion, worker failure, and conflicting findings. Keep a scripted process-based mode for learners without model access, and label it as such.

**Completion check:** logs establish which worker used which inputs and produced which artifact; integration rejects stale or conflicting output according to its contract; comparison includes parent effort and all workers. External publication can remain an optional final step.

## 6. Extend retrieval into a measured, realistic experiment

**Priority: medium, after the current context foundations.**

[Lesson 05](../content/lessons/05-retrieval-and-grounding.md) teaches lexical retrieval, exceptions, recall, and claim support. [Lab 02](../content/labs/02-context-budgets.md) adds deterministic packing. These are appropriate foundations. The missing next step is a runnable comparison that tests when a more sophisticated retriever is worth using.

Provide a versioned synthetic corpus with paraphrases, metadata constraints, policy changes, duplicate passages, contradictory sources, and unanswerable questions. Compare the lexical baseline with an optional local embedding or hybrid retriever. Include an optional reranking step only when the earlier comparison identifies a need.

Measure retrieval recall and final claim support separately. Add experiments on chunk boundaries, metadata filtering, source refresh, and context compression. Retain a fixed evaluation set while changing one component.

**Completion check:** the learner identifies which cases improved or regressed, reports the required evidence actually retrieved, and can explain whether an error arose in search, selection, generation, or grading.

## 7. Build a small human-review and operations exercise

**Priority: medium; extends existing production lessons.**

The course already teaches authorization, service contracts, metrics, rollback, and incidents. The [production lesson](../content/lessons/22-production-design.md) intentionally uses a local, synthetic environment. Add one concrete local user journey to make those plans executable.

Create a review queue where a person can inspect the draft and sources, request a correction, approve a specific version, or reject it. Test stale approval after the draft changes. The approved effect can remain a synthetic local status change.

Package the system for a clean-environment run and add a CI exercise that runs checks and preserves evaluation artifacts. Rehearse releasing a changed knowledge version, detecting a mismatch, rolling back, and accounting for pending work. A hosted deployment is optional.

**Completion check:** approval refers to the exact reviewed artifact; pending work survives a restart; stale approval is rejected; a fresh checkout can run the release checks and reproduce the rollback.

## 8. Strengthen retention, transfer, pacing, and media

**Priority: medium; develop alongside the early-stage improvements.**

Existing weekly reviews and week 4/8/12 retention exercises are useful. Add a small queue of new-case recall tasks tied to the learner's mistakes. Revisit concepts after increasing intervals, adjusting the schedule based on observed recall rather than presenting one interval pattern as universally optimal.

Introduce short transfer exercises before the capstone: extract structured data from a document, review a QA change, or produce a sourced research note. Keep the same learning objective while changing the domain. These reveal whether the learner understands the principle or merely recognizes Signal Desk terminology.

The library already has seven external video entries and a curated route. Higher-value additions are short original walkthroughs with captions/transcripts, selected reading sections, and a pause point before the learner's own attempt. A new diagram example should use a different scenario from the assigned exercise.

Most lesson metadata uses the same 90-minute estimate. Replace that single number with separate reading, guided practice, independent work, and optional extension estimates. Validate the estimates through actual learner sessions. Use explicit routes for concept-only study, local engineering, and live-model work, showing pending requirements rather than silently equating them.

**Completion check:** the learner solves a new case after a delay, can explain an earlier error, and has one clear next action. A learner without current model access can still progress while seeing which integration evidence remains pending.

## Recommended implementation order

| Pass | Changes | Evidence before moving on |
| --- | --- | --- |
| 1: Repair and orient | Hint rendering; stale lesson metadata; study-plan submissions; first-stage preparation and worksheets | Eight hint pages behave correctly; a beginner completes the first small exercise without the target answer |
| 2: Tutor and assess | Exercise records; progressive help; tutor packets; calibration examples; richer checks | Attempt, feedback, revision, export, and resume all work; no solution leaks into a starter tutor packet |
| 3: Connect the tools | Planner loop; optional provider transport; MCP host/model use; coding-agent and worker practicum | Reproducible tool-use traces and injected failures; measured single-versus-team comparison |
| 4: Broaden and operate | Retrieval comparison; review queue; CI and rollback; transfer and retention activities | New-case performance, clean-environment reproduction, and a demonstrated recovery path |

The first two passes address the learner's observed difficulty most directly. The later passes close the distance between understanding agent systems and operating one independently.

## Keep the scope deliberate

Retain the existing core concepts, offline route, evidence discipline, and capstone choice. Avoid adding many frameworks, another large undirected resource list, or mandatory model training before the learner can operate the current system. An optional extension should have a specific skill, a runnable starting point, and an observable completion criterion.

Keep full solutions available by deliberate choice. The learning design should support honest attempts and progressively stronger help, rather than force a learner to struggle indefinitely or expose an answer when they requested only a hint.
