# Claude entry point: AI Engineering Academy

Read [AGENTS.md](AGENTS.md) before working. It is the shared source of assistant
instructions for this repository. Read [README.md](README.md) for the project
idea, source map, runtime modes, and commands. Keep detailed working rules in
AGENTS.md rather than creating a separate, drifting rule set here.

## Essential context

This project guides an SDET from AI basics to using AI in testing, testing AI
systems, and understanding agents and harnesses. It gathers useful knowledge
from multiple providers into a clear sequence with original explanations and
one selected external resource per topic. The default path lives in
`content/sdet-path.json` and `content/guide/` (portal `#guide`).

The fictional Signal Desk case study, original lessons, exercises, incidents,
Python labs, templates, and PDF fieldbook remain available as optional practice
and reference. Drawing or writing artifacts is not a condition for learning.

- **Tutoring:** start with [the tutor handoff](docs/CONTINUE-LEARNING.md). Explain
  one concept and its relevance to SDET work, then give one bounded reading step.
  Use topic 01 when no position is supplied. Do not require an assignment,
  diagnostic, or a saved progress file before teaching.
- **Chosen practice:** give one exercise at a time, check the actual attempt,
  and offer a small hint when asked. Keep solutions and incident debriefs hidden
  until the learner tries and deliberately requests help. The
  [practice tutor prompt](templates/practice-tutor-prompt.md) preserves this mode.
  A reading bookmark does not prove completion or practical mastery.
- **Implementation:** use [maintenance guidance](docs/MAINTENANCE.md), inspect
  the working tree, and edit source before rebuilding dist/. Unfinished student
  components and seeded failures are intentional exercises.
- **Local use:** `python3 academy.py local` starts the portal. Learning records
  persist in the project's ignored SQLite database, separate from Git and chats.
  See [local data and recovery](docs/LOCAL-DATA.md).
- **Hosted use:** the OpenAI Site is static and keeps browser-local progress.
  It does not synchronize with SQLite. Export/import JSON to move records.
- **Another account:** the source works independently of the original login.
  Follow [NEW-ACCOUNT.md](docs/NEW-ACCOUNT.md) to prepare a separate Site copy;
  publishing it requires the target account's supported Sites integration.

Do not assume prior conversation history, tool connections, or credentials are
available in this session. A configured URL or a passing historical report is
not proof of current access or current test results. Follow the user's actual
task and report only actions and checks that occurred.
