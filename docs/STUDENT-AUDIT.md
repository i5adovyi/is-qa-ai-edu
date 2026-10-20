# Final audit from a fresh student clone

Audited on 20 October 2026, starting with a new authenticated GitHub clone of release `dcb8914`. The clone had no learner work, cached Python environment, installed teaching skill, or saved portal progress. Fixes were applied to the source and then checked again in isolated copies. The audit ran on macOS ARM64 with Python 3.9.6 and 3.12.14; Windows instructions were reviewed but not executed.

## What was covered

- All 24 lessons and all 72 exercise instructions, including inputs, expected artifacts, pass criteria, and hints. See the [exercise-by-exercise matrix](EXERCISE-AUDIT.md).
- All 11 lab guides, all eight intentionally failing starter helpers, their disclosed completed implementations, deliberate regressions, student train/holdout/release gates, and crash recovery.
- Fresh MCP dependency installation, actual client/server requests, the failing and completed tool-extension exercise, changed corpus data, and repaired stdout contamination.
- Skill installation, duplicate refusal, missing dependency and repair, and eight actual fresh Codex host trials: matching requests, unrelated requests, missing reference, novel prompts, and changed evidence.
- The seeded coding sandbox, its repair and three rejected faulty alternatives; model-bridge export/replay and malformed input paths.
- Nine templates, three capstone briefs, the research source pack, calculation examples, and the first-session setup instructions.
- Every portal document, internal link/section, downloadable asset, all 96 quiz choices, all eight stage pages, and mobile document layouts. Interaction checks also cover notes, progress transfer, search, saved resources, and the simulator.
- All external learning destinations. See the [link audit](LINK-AUDIT.md) for exact URLs, response limitations, and publisher-page follow-up.

## Defects fixed

1. **Completed student work failed the test suite.** Two tests accidentally used the learner's current file as if it were still blank. They now create explicit unfinished fixtures.
2. **A student syntax error broke the working examples.** Student code was imported during reference CLI startup. It is now loaded only for a requested student operation; syntax/import failures produce a clear `student_import` diagnostic.
3. **A valid checkpoint could fail to resume in a new process.** Function fingerprints depended on unordered constant serialization. Canonical fingerprints now survive a different Python hash seed while still rejecting changed source, functions, profile, or context limits.
4. **Repeating the MCP copy command could erase an implementation.** The learner-copy instructions now refuse an existing destination, including a guarded PowerShell alternative.
5. **Several exercises assumed missing artifacts or earlier state.** Instructions now supply the handoff and policy-change fixtures, preserve the repaired lesson-10 sandbox, explain solo-review alternatives, distinguish learner scripts from bundled commands, and specify complete student-harness evaluation.
6. **The research input could expose grading answers.** The guide now separates question/source input from reviewer-only labels and explains the additional pairs required by the capstone.
7. **Fresh-copy setup and final navigation were incomplete.** A setup manual now covers cloning/downloading, working directories, Python versions, expected skips/failures, server lifetime, and progress transfer. Lesson 24 leads to capstones instead of looping back to lesson 01.

## Recovery compatibility

The corrected component binding is `composed-v2`. Preserve old `composed-v1` evidence with its original checkout and interpreter, or start a new run after updating. Do not edit a checkpoint to force a match. Component bindings are consistency checks for trusted local code, not signatures or an operating-system sandbox.

## Results and limits

The final [verification record](VERIFICATION.md) contains release test totals and reproduction commands. The lab command audit retained 114 checks, including the initial failures and successful retests. The completed student route passed 28 cases, 11 failure scenarios, three integration probes, and all eight helper gates. The full test suite also passed with completed student code and with a deliberately broken student import in isolated copies.

The MCP baseline passed 13/13; its intentionally unfinished extension failed 13/16 and the completed extension passed 16/16. Fresh host trials produced actual review artifacts and correctly withheld them for irrelevant requests or missing dependencies. These checks do not establish broad model reliability.

Reviewing every open-ended exercise is not the same as finishing 72 original student projects. Manual rows in the matrix audit the instruction and expected reasoning. No independent learner pilot, cross-platform execution, video playback, paid-course completion, or optional skill-description A/B study was performed. Those limits are explicit rather than counted as passes.
