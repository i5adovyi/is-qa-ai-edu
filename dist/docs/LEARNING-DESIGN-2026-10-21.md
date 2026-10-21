# Learning-design correction — 21 October 2026

## What went wrong

The first edition optimized for breadth, exercises, runnable labs, and evidence of practical work. A first-time learner then reported getting lost within two minutes. The start button led to diagram preparation; the sidebar offered many destinations; the tutor handoff required an attempt before explaining the subject. Those choices did not serve the requested goal: gather scattered knowledge and guide an SDET from basic concepts to advanced topics.

The earlier automated checks established that links, persistence, exercises, and packaging worked as tested. They did not establish that the educational sequence matched the learner's intent. The initial closeout is a historical implementation record, not proof of a successful learner experience.

## The corrected experience

The default route now starts with eight original reading topics. Each explains a concept through SDET work, identifies relevant prior knowledge, selects one external reading with a bounded scope and access notes, and offers a next topic. Alternatives and practical material are collapsed and optional. The course draws on multiple providers; an external academy's catalog is not the study plan.

The homepage has one primary reading action. The main navigation separates the guided path from the optional collection. Save my place records an explicit reading location without awarding completion. Notes and the reading location use the same private local/hosted progress system as existing records.

## Preservation

No original lesson, exercise, lab, incident, solution gate, article, book, or capstone was removed. All 24 practical lessons and all 15 labs remain accessible through their complete indexes. Topic-specific related links are selections, not replacements for those indexes.

The old project overview, start orientation, study schedule, and practice tutor are preserved as clearly labeled optional or historical documents. Existing lesson and exercise identifiers remain stable. Personal progress is not reset or marked complete by this redesign. The original PDF remains available as a practice fieldbook; it is not advertised as the new guided reading edition.

## Follow-up standard

Judge the next iteration by whether a new learner can identify the first topic, understand why it matters, and find a next step without choosing among unrelated tracks. Additional pages alone do not improve that outcome. Keep advanced details accessible, but introduce them when their purpose is clear.

The source pages and the scope of selected external material were reviewed. External enrollment, every embedded video, and learner comprehension are separate checks. Software regression results for this revision belong in the verification record; do not infer them from older releases.

## Whole-course correction after learner testing

The eight-primer revision did not solve the learner's problem. It made the original full curriculum look missing and left the detailed lessons assuming knowledge they had not taught. The learner's example was being asked to implement a state machine without first learning what a state machine was. Passing UI tests in that release did not establish that its learning approach was useful.

The revised approach applies to all 24 lessons, while preserving the eight stages, stable lesson/activity IDs, original lesson bodies, articles, labs, incidents, and capstones. The full course is again the main visible map. Eight short primers remain supporting introductions. A new material finder indexes all distributed Markdown documents and the external library; each lesson and stage collects relevant existing materials.

Every lesson begins with a new beginner guide: definitions before jargon, SDET relevance, a small explained example, concrete steps using Codex or Claude Code, observable expected results, common failure recovery, and one bounded external reading. The assistant quickstart explains the difference between a chat prompt and terminal command, how to open the actual project, and how to learn without local setup. AI-assisted demonstrations are a legitimate beginner route. Independent implementation is offered after understanding. Drawing diagrams and producing documents are not entry requirements.

The original explanations and three exercises remain on each lesson page. Deliberate practice keeps its attempt-first contract, while normal explanations are available immediately. The original lesson solution outline now requires meaningful recorded attempts for all three exercises and a separate reveal; individual exercise workspaces continue to provide their own hints. Incident gates are unchanged. Downloadable source remains inspectable and is not an examination-security system.

Independent review caught stale imperative map titles, conflicting primer route instructions, inappropriate “try first” copy on explanatory pages, and a skill-installation handoff that mixed workspace names and host-specific commands. These were corrected. Bookmark and next-lesson controls appear before the long lesson so mobile readers do not have to scroll past every optional exercise to continue.

Preservation was checked against commit 8264fe535a5c19c3e2038eaaf41291c162b2682b: every previously tracked file remains present; 141 original teaching and lab files are byte-for-byte unchanged. The old short reading selections are retained in [PRIMER-READINGS.md](PRIMER-READINGS.md). Current setup, tutor handoff, README, AGENTS.md, and CLAUDE.md describe one full course rather than competing required routes.

These changes address observed product and instructional defects. Automated tests and editorial review cannot prove that a learner understands the material. The next useful evidence is a learner completing a short lesson with the new guidance and describing where they still get stuck; no mastery, certificate, or commercial valuation is inferred from the test suite.

## Subject tracks supersede the fixed-sequence navigation

Later learner feedback clarified that a single sequence still hid the shape of the subject. The reference was a subject-oriented academy: visible, independent tracks and a clear beginner-to-advanced route inside each. The current implementation therefore expands to 14 subjects and 84 topics, with four curated paths across them. It preserves all earlier teaching and practice and retains the original 24-lesson map as a compatible route. See [the current study plan](STUDY-PLAN.md), [complete catalog](SUBJECT-CATALOG.md), and [verification record](VERIFICATION.md).

The lesson is to distinguish a catalog, a guided path, and optional practice. A catalog shows what exists. A path selects what to learn next. Practice lets a learner apply an understood idea. Collapsing all three into a single sequence made the academy harder to understand even when its individual pages and tests were technically correct.
