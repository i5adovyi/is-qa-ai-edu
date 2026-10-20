# Prepare for projects beyond this course

The core curriculum already teaches contracts, context, tools, bounded execution, evaluation, and operations. The added labs now make model/tool loops, worker coordination, retrieval comparisons, and local review/rollback executable. The remaining bridge to your next project is learning to diagnose your own environment, compare changing models, and turn new evidence into a versioned evaluation set.

Use these checks where they become relevant. They are not extra prerequisites for lesson 01. An experienced learner can demonstrate the artifact and skip the preparation; an unfamiliar term signals a small practice task, not a reason to abandon the course.

## Prerequisites at the point of use

| Before | Show this artifact | If you cannot yet do it |
| --- | --- | --- |
| Lesson 01 | One labeled connection; a distinction between a proposal and observed outcome | Complete beginner entry checks A/B |
| Python labs | A valid JSON edit, regenerated file, and explained failed assertion | Complete [terminal preparation](../content/onboarding/terminal-worksheet.md); practice functions/dictionaries before implementing helpers |
| Coding mission | `git status`, a narrow diff, a commit ID, and a safe revert in a disposable repository | Use lab 13's isolated mission; do not experiment on the only copy of important work |
| MCP or provider adapters | Interpreter/dependency identity and the exact command that runs your environment | Record executable path, Python version, pinned requirements, working directory, and output path |
| HTTP provider route | A request/response sketch and a distinction among validation failure, authorization failure, rate limit, timeout, and invalid response content | Complete mission 1 below using supplied observations before using a paid API |
| Model migration | Same-case outputs from baseline and candidate, with configuration and resource use | Complete mission 2; do not substitute provider marketing claims for your own task evidence |
| Expanding project data | A new case with provenance, label justification, privacy review, and split decision | Complete mission 3; preserve an untouched final set |

## Three short missions for future projects

### Mission 1 · Diagnose environment and API boundaries

**Placement:** after lesson 07, before an optional provider route. **Time:** 30–60 minutes, plus preparation if the terminal is new.

From the repository root run:

```sh
python3 -c "import sys; from pathlib import Path; print(sys.executable); print(sys.version); print(Path.cwd())"
git status --short
git rev-parse HEAD
```

For a ZIP download without Git metadata, record “archive, no commit metadata” and the download/source version you actually have; do not invent a commit. For the MCP environment, run its own Python executable with the same inspection command. Explain why the system interpreter and a virtual environment can have different installed packages.

Now inspect [five synthetic API observations](../content/practice/api-observations.json). For each, write: what is observed; whether the next action belongs to input repair, access/configuration review, bounded retry, reconciliation, or response validation; and what you cannot conclude. No network request or credential is needed. Do not treat a successful HTTP status as proof of a valid task result, or a timeout as proof that no effect occurred.

**Deliverable:** `work/readiness/environment.md` and a five-row diagnosis table. Include the selected API's current official documentation link if you actually implement a provider call; log configuration names and nonsecret metadata, never credential values.

**Pass:** another learner can identify the interpreter and source version you used, reproduce the command, and distinguish transport observations from validated task outcomes. The local worksheet is not evidence that a remote API credential works.

### Mission 2 · Compare a model or configuration change

**Placement:** after lessons 16–18 and lab 12's prerequisite gates. **Time:** 30–60 minutes for the plan and initial small comparison; allow extra time/cost for actual repeated model runs.

Choose one candidate change: a different accessible model, a model revision, or one request configuration supported by your provider's current official documentation. Hold the task contract, tools, sources, and rubric fixed. Select six development cases: two ordinary, two incomplete/conflicting, one malformed proposal, and one premature-completion challenge. Freeze a separate four-case final set before tuning.

Use lab 12's actual adapter when available, with a new output directory for each run. Record requested and returned model identity separately when exposed; configuration, prompt/corpus versions, attempts, latency, and available usage. Keep unavailable fields explicitly unavailable. Run at least three repetitions on a chosen difficult case before making a claim about variability.

Predeclare a release decision: no new hard-gate failures; ordinary-case usefulness must meet your stated threshold; resource changes must be acceptable under your own budget. Inspect every discordant case. Preserve the baseline configuration and rehearse restoring it if the candidate fails. A newer model is not automatically a better fit for your task.

**Deliverable:** paired comparison, frozen manifest, one regression or an honest tested-limit statement, and a revert record. If using scripted configurations, label this a migration-process rehearsal; actual model comparison remains pending.

**Pass:** claims name the evaluated cases/configurations, include regressions and all observed attempts, and demonstrate restoration of the baseline. Do not tune repeatedly on the final set and continue calling it unseen.

### Mission 3 · Learn from new data without losing the benchmark

**Placement:** after lessons 16–17, revisited during the capstone. **Time:** 30–60 minutes.

Use the local synthetic setting. Add three new observations: a paraphrase of an existing request, a genuinely new policy exception, and a report with insufficient evidence to label confidently. For each, create a case record with source, date, consent/data-use basis where applicable, sensitivity, input, permitted evidence, expected/forbidden behavior, and label rationale. In a real project, use only data you are authorized to retain and remove unnecessary personal details.

Classify each observation as development feedback, a related robustness family, or a potential fresh final case. A paraphrase is related to its parent, not independent corroboration. Keep ambiguous labels explicit. Version the dataset and rubric together when policy changes; preserve the old version for reproducibility rather than silently rewriting history.

Run the old fixed benchmark and the new cases separately. Report which former cases changed meaning because policy changed, which regressions are implementation defects, and which questions need domain review. Set one trigger for revisiting the dataset, such as a new permitted action or changed source scope.

**Deliverable:** dataset change note, three provenance records, split decision, and before/after result table or mechanically documented manual evaluation.

**Pass:** new feedback becomes reviewable cases without leaking labels into runtime context, erasing historical results, or inflating an untouched-set claim.

## Choose later depth from an observed need

Fine-tuning, training models from scratch, GPU serving, advanced embedding/reranking systems, multimodal/OCR pipelines, streaming audio, distributed infrastructure, and detailed statistical inference are optional later specializations. They are not silently included in this course's practical gate. Choose one when your own measured failure or deployment requirement justifies it.

For example, an OCR problem needs document-quality evidence and extraction evaluation; a latency problem may need profiling before a new model; an ambiguous policy may need a domain decision rather than more engineering. The portable habit is to diagnose the boundary, propose one measurable change, and preserve enough evidence to know whether it helped.
