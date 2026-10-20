# Install and test a real Signal Desk skill

The bundled [skill](signal-desk-evidence-review/SKILL.md) reviews an invented support draft against its evidence. [Lab 10](../labs/10-installed-skill.md) installs it into a disposable workspace, launches a fresh compatible Codex session, and tests activation, an unrelated task, and a missing reference. The files are local; running a model session uses your existing host access and may consume your plan allowance. File installation and structural tests require no model or network.

The sample is deliberately narrow. It does not provide a customer-service integration, prove general prompt-injection resistance, or enable account mutations. Its validator checks schema, citation membership, claim coverage, and the uncertainty decision; a human must still judge whether cited text supports a claim.

## Files

- [SKILL.md](signal-desk-evidence-review/SKILL.md): metadata and concise procedure.
- [Review contract](signal-desk-evidence-review/references/review-contract.md): task-specific judgment rules, loaded when the skill applies.
- [Output template](signal-desk-evidence-review/assets/review-template.json): JSON artifact shape.
- [Validator](signal-desk-evidence-review/scripts/check_packet.py): deterministic local preflight and output checks.
- [Ticket packet](fixtures/ticket.json): three claims, three sources, one untrusted source instruction.
- [Recorded host evidence](HOST-EVIDENCE.md): actual version, observed behavior, and limits of the test.

Keep the course package under `content/`. Install copies under `work/<name>/.agents/skills/`; `work/` is ignored by Git. Never use the original package as your missing-file experiment. The install command refuses existing workspace destinations so a repeat cannot silently overwrite your learning artifacts.

## Installation contract

Run from the academy repository root:

```sh
python3 -m lab.skill_lab install
python3 -m lab.skill_lab validate
python3 work/skill-practice/.agents/skills/signal-desk-evidence-review/scripts/check_packet.py \
  work/skill-practice/fixtures/ticket.json
```

Use `--workspace work/skill-second-attempt` for another attempt. Destinations must be dedicated children of this repository's `work/` folder; parent traversal and symlink components are rejected. The installer copies the skill and fixture, then records a SHA-256 inventory in `installation.json`. Its `host_behavior` field remains `not_tested`: a copy is not proof of host discovery. The inventory describes the current validated files and is not a cryptographic signature or a third-party trust assessment.

No global skill directory, account setting, or configuration file is changed. To remove a practice installation, delete only the dedicated practice directory after saving any evidence you need.

## Official host documentation

Checked on 20 October 2026: Codex searches repository `.agents/skills` locations for skill folders, and can select a skill from its metadata or accept an explicit `$skill-name` invocation. If discovery does not refresh, start a fresh session. Installation paths differ between hosts; this exercise verifies Codex, not every compatible agent application. [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills).

The CLI exercise records JSON events and the final message, uses workspace-write sandboxing, and makes only temporary command-line configuration choices. Consult your installed `codex exec --help` if flags differ. [OpenAI: Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli).
