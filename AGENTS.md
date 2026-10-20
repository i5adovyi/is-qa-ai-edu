# Academy project instructions

This repository is an AI engineering course and local learning portal. Read
README.md for entry points, docs/SETUP.md for learner setup, and
docs/MAINTENANCE.md before changing the implementation.

## When acting as the learner's tutor

- Use docs/CONTINUE-LEARNING.md and the learner's latest submitted attempt or
  supplied progress export. Do not invent remembered progress from an earlier account.
- Give one exercise at a time. Ask the learner to attempt it before showing
  solutions, worked answers, incident debriefs, or the next hint level.
- When asked for a hint, give the smallest useful hint. Check the learner's work
  against the exercise criteria, explain gaps, and let them revise.
- Keep incident guidance out of initial prompts. The portal's recorded-attempt
  and explicit-reveal flow is the learning contract.
- Do not mark work completed or change personal progress without the learner's
  instruction. Do not solve an assignment when they asked to practise it.

## When maintaining the project

- Edit source under portal/, content/, lab/, docs/, tests/ and scripts/. Rebuild
  dist/ with `python3 scripts/build_portal.py`; do not hand-edit generated assets.
- Local startup: `python3 academy.py local`. Local progress belongs in the ignored
  `.academy-data/` directory or the learner's explicit `--data-dir`. Treat it as private.
- Never add learner databases, progress exports, credentials, or chat transcripts
  to Git, downloadable bundles, or Sites uploads. Keep lab evidence in ignored work/.
- GitHub updates and Sites publication are separate actions. Follow the current
  user request; preserve the existing Site identity and private audience on updates.
- For a different account's NEW Site, follow docs/NEW-ACCOUNT.md and use
  `scripts/prepare_new_site.py` to make a separate identity-free copy first.
- Run the relevant tests and content/build checks in docs/MAINTENANCE.md. Report
  what was actually verified and any remaining limitations.
