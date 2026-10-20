# Claude entry point: AI Engineering Academy

Read [AGENTS.md](AGENTS.md) before working. It is the shared source of assistant
instructions for this repository. Read [README.md](README.md) for the project
idea, source map, runtime modes, and commands. Keep detailed working rules in
AGENTS.md rather than creating a separate, drifting rule set here.

## Essential context

This project teaches practical AI engineering through a continuous fictional
case study, Signal Desk. It combines lessons, exercises, incident investigations,
runnable Python labs, a local/hosted learning portal, and a PDF fieldbook.
The aim is independent engineering judgment backed by reproducible evidence.

- **Tutoring:** give one exercise at a time, check the learner's own attempt,
  and offer a small hint when asked. Do not reveal answers or incident debriefs
  before the attempt and deliberate request. Start with
  [the tutor handoff](docs/CONTINUE-LEARNING.md); confirm actual current progress.
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
