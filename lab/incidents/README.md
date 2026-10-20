# Local incident workspaces

Seven fictional operational assignments add ambiguity to the academy's smaller labs.
Start with the incident brief in the portal, then create its local workspace:

```sh
python3 -m lab.incidents init INC-01 --workspace work/incidents/INC-01
python3 -m lab.incidents run --workspace work/incidents/INC-01
python3 -m lab.incidents check --workspace work/incidents/INC-01
```

Python 3.9 or later is sufficient. INC-01 also needs Git. All fixtures are local;
there are no provider accounts, API keys, package installations, or service calls.
The initial worker is deliberately incomplete, so the first `check` exits 1.
Invalid commands, missing files, and blocked guidance exit 2.

Read `brief.md`, `CONTRACT.md`, `input.json`, and `evidence/` in the generated
workspace. Edit `student.py` to implement `handle(data)`. INC-01 also includes an
inherited disposable Git repository; its contract names the allowed repair and
the human work that must be preserved. Existing workspaces are never overwritten.
Choose a new directory for a new attempt or variant.

Before requesting guidance, save a hypothesis tied to a real evidence file and
a concrete next check:

```sh
python3 -m lab.incidents attempt --workspace work/incidents/INC-01 \
  --hypothesis "Write your own hypothesis here" \
  --evidence input.json \
  --next-check "Write the observation that could disprove your hypothesis"
python3 -m lab.incidents hint --workspace work/incidents/INC-01 --level 1
```

Replace the quoted placeholders with your own work. Saving an attempt reveals
nothing automatically. Hints are separately requested at levels 1, 2, and 3.
Only when you want to compare your reasoning, run:

```sh
python3 -m lab.incidents debrief --workspace work/incidents/INC-01
```

Hint and debrief commands require a saved attempt. CLI attempts are stored in
`.incident-attempts.json` inside that workspace; portal attempts are separate.
The gate supports a learning habit, not access control. Source readers can
intentionally open reference code; do not do so before your attempt.

`run` retains each proposal as `runs/run-00001.json`, `runs/run-00002.json`, and
so on, with input and worker hashes. `runs/latest.json` is a convenience copy.
`check` similarly retains numbered `runs/check-00001.json` records and updates
`runs/check.json`; it evaluates the current input plus transfer and boundary
workloads. It does not print expected answer objects. Evidence hashes are checked
before and after execution. Keep baseline inputs unchanged; write notes in a new
file instead of rewriting the evidence to fit your theory.

After your first recovery, prove transfer in a fresh workspace:

```sh
python3 -m lab.incidents init INC-01 --workspace work/incidents/INC-01-transfer --variant transfer
```

Use IDs `INC-01` through `INC-06`, then `INC-CAPSTONE`. For the final incident,
choose just one of your existing capstones:

```sh
python3 -m lab.incidents init INC-CAPSTONE \
  --workspace work/incidents/INC-CAPSTONE --project qa
```

`--project` accepts `support`, `qa`, and `research`; it records the stakeholder
context, not a different production integration. Explain how the recovery
proposal affects your selected capstone's users.

The simulator checks executable contracts and evidence preservation. A human
still reviews competing hypotheses, useful questions, provenance, recovery
tradeoffs, and honest unknowns. Suggested investigation budgets are planning
exercises, not enforced wall-clock or API-spend controls. Scheduling uses integer
ticks, and remote outcomes, identity changes, and migrations are fictional data.
This is not production load, security, distributed transaction, or migration
validation. Student Python runs with your local permissions; execution has a
five-second timeout but is not an operating-system sandbox.
