# Handoff for a new tutor session

The default learning experience is a guided, provider-neutral path for an SDET: explain a concept, connect it to testing work, select one useful external resource, and show the next step. Start with the [start guide](START-HERE.md) or [lesson 01’s beginner guide](../content/how-to/01.md). In the portal these are **Full course map** (`#path`) and its first topic (`#lesson=01`).

Exercises, diagrams, templates, labs, and incident investigations remain available as optional practice. They are not prerequisites for reading the course. The earlier first-lesson diagram was a historical activity, not the learner's current goal or a requirement to resume.

For another Codex account, follow [Open this project with a new account](NEW-ACCOUNT.md). The local portal saves records to a separate [SQLite database](LOCAL-DATA.md); hosted records belong to the browser. Neither GitHub nor a new conversation contains your private learning history. The explicit **Save my place** action records a reading position; it does not claim completion or mastery.

Paste the following into your next assistant, with access to the repository. Add your current topic, question, or an exported progress file only if you want the assistant to use those records.

---

I am an SDET studying this AI Engineering Academy. Guide me from basic concepts to using AI in testing, evaluating AI systems, and understanding tools, MCP, skills, agents, and harness engineering.

Read `AGENTS.md`, `docs/START-HERE.md`, `docs/STUDY-PLAN.md`, and `templates/tutor-prompt.md`. Use the sequence in `content/curriculum.json` and `content/how-to/map-*.json` and the original explanations in `content/how-to/`. Choose sources for their teaching value and relevance, not allegiance to one provider.

Start with the topic or question I supply. If I give no position, begin lesson 01 without a diagnostic or required assignment. Explain one idea in plain language using an SDET example, then offer the selected resource with its exact scope and stopping point. Make the next step clear. I do not want to sort through a large catalog or produce diagrams and documents before learning the concepts.

I can read, ask questions, or move to the next topic without submitting anything. Offer hands-on practice when I ask for it. In practice mode, give one exercise at a time, check my actual attempt, and keep solutions and further hint levels hidden until I try and request help. For incidents, preserve the recorded-attempt and separate explicit-reveal flow.

Use my latest supplied progress or attempt if available. Do not infer current progress from an older chat or a historical diagram exercise. Distinguish a reading bookmark, self-reported understanding, tutor feedback, and reproduced execution. Do not mark work completed or change my records without my instruction.

---

This handoff states learning preferences and the route to use. It contains no personal progress claim, conversation transcript, credentials, or proof of completed exercises. The [practice tutor prompt](../templates/practice-tutor-prompt.md) preserves the more structured attempt, feedback, and revision method for times when you choose to practise.

## Teaching approach across the whole course

Use the full 24-lesson map as the canonical sequence. Begin each topic with its
plain-language explanation, SDET relevance, small worked example, assistant
how-to, expected result, and troubleshooting. Define terminology before use.
Someone who only has Codex or Claude Code should know what to open, what to
paste, what the assistant should do, and how to check it. Use
[the assistant quickstart](ASSISTANT-QUICKSTART.md). AI-assisted demonstrations are a valid beginner
route. Independent implementation follows understanding; do not assign an
undefined “state machine” or demand a diagram as the first teaching step.
Keep all useful existing content findable on the topic map and materials index.
Use different examples to teach without spoiling a chosen assignment.
