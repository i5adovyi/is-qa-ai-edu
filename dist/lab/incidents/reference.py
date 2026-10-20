"""Instructor/reference solutions. Intentional spoilers: attempt the incident first.

Learner runs never import this file. Checks import it only to evaluate behavior;
they never print expected answer objects.
"""
import datetime
import re


def solve(case, data):
    if case == "INC-01":
        good = [r["id"] for r in data["reports"] if r["revision"] == data["current_revision"]
                and r["discovered"] > 0 and r["failures"] == 0]
        observations = {}
        for row in data["executions"]:
            if row["revision"] == data["current_revision"]:
                observations.setdefault(row["test"], set()).add(row["result"])
        flaky = sorted(k for k, values in observations.items() if {"pass", "fail"} <= values)
        return {"usable_reports": good, "flaky_tests": flaky,
                "release": "ready" if good and not flaky else "blocked"}
    if case == "INC-02":
        pages = data["pages"]
        seen = set()
        cursor = None
        complete = bool(pages)
        for page in pages:
            if page["cursor"] != cursor or page["cursor"] in seen or page.get("truncated", False):
                complete = False
            seen.add(page["cursor"])
            cursor = page["next_cursor"]
        complete = complete and cursor is None
        records = []
        for page in pages:
            for row in page["records"]:
                state = "missing" if "amount" not in row else "null" if row["amount"] is None else "value"
                raw = row["date"]
                date = None
                try:
                    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
                        date = datetime.date.fromisoformat(raw).isoformat()
                    elif re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", raw):
                        a, b, year = map(int, raw.split("/"))
                        locale = data["locale"]
                        if locale == "DMY" or (locale is None and a > 12 >= b):
                            date = datetime.date(year, b, a).isoformat()
                        elif locale == "MDY" or (locale is None and b > 12 >= a):
                            date = datetime.date(year, a, b).isoformat()
                except ValueError:
                    pass
                records.append({"id": row["id"], "amount_state": state,
                                "amount": row.get("amount"), "date": date})
        eligible = [row for row in data["evaluation"] if row["id"] not in data["training_ids"]
                    and not row["baseline_cached"] and not row["candidate_cached"]]
        gain = sum(row["candidate"] - row["baseline"] for row in eligible) / len(eligible) if eligible else None
        return {"complete": complete, "records": records, "holdout_gain": gain}
    if case == "INC-03":
        create, notify, unknown = [], [], []
        checkpoint = 0
        contiguous = True
        for op in sorted(data["operations"], key=lambda op: op["seq"]):
            status = data["remote"].get(op["id"], "unavailable")
            if status == "absent":
                create.append(op["id"])
            elif status == "unavailable":
                unknown.append(op["id"])
            elif status == "present" and op["id"] not in data["notifications"]:
                notify.append(op["id"])
            if contiguous and status == "present" and op["seq"] == checkpoint + 1:
                checkpoint = op["seq"]
            else:
                contiguous = False
        return {"create": create, "notify": notify, "unknown": unknown, "checkpoint": checkpoint}
    if case == "INC-04":
        principal, workspace = data["principal"], data["workspace"]
        grants = {(g["principal"], g["workspace"]) for g in data["grants"]}
        revoked = set()
        manifest = data["skill"]
        major = manifest["version"].split(".")[0]
        compatible = (major, manifest["units"]) in {("1", "dollars"), ("2", "cents")}
        result = []
        for event in data["events"]:
            if event["type"] == "switch":
                principal, workspace = event["principal"], event["workspace"]
            elif event["type"] == "revoke":
                key = (event["principal"], event["workspace"])
                grants.discard(key)
                revoked.add(key)
            elif event["type"] == "request":
                key = (principal, workspace)
                status, value, source = "ok", None, None
                if key not in grants:
                    status = "reauthorize" if key in revoked else "denied"
                elif not compatible:
                    status = "incompatible"
                else:
                    entry = next((c for c in data["cache"] if
                                  (c["principal"], c["workspace"], c["query"], c["skill_version"]) ==
                                  (principal, workspace, event["query"], manifest["version"])), None)
                    value = entry["value"] if entry else event["value"]
                    value = value / 100 if major == "2" else value
                    source = "cache" if entry else "tool"
                result.append({"id": event["id"], "status": status, "value": value, "source": source})
        return {"results": result}
    if case == "INC-05":
        schedule, deferred, spent = [], [], 0
        active, retry_starts = [], set()
        for job in data["jobs"]:
            earliest = max(job["arrival"], job["retry_after"])
            chosen = None
            for start in range(earliest, data["deadline"] - job["duration"] + 1):
                fits = all(sum(a <= tick < b for a, b in active) < data["max_concurrency"]
                           for tick in range(start, start + job["duration"]))
                if fits and not (job["retry"] and start in retry_starts):
                    chosen = start
                    break
            if spent + job["cost"] > data["budget"] or chosen is None:
                deferred.append(job["id"])
                continue
            schedule.append({"id": job["id"], "start": chosen})
            active.append((chosen, chosen + job["duration"]))
            if job["retry"]:
                retry_starts.add(chosen)
            spent += job["cost"]
        revision, value = data["record"]["revision"], data["record"]["value"]
        updates = []
        for update in data["updates"]:
            status = "conflict"
            if update["expected_revision"] == revision:
                status = "applied"
                revision += 1
                value += update["delta"]
            updates.append({"id": update["id"], "status": status, "revision": revision})
        return {"schedule": schedule, "spent": spent, "deferred": deferred,
                "updates": updates, "final_value": value}
    if case == "INC-06":
        version = max(r["version"] for r in data["requirements"])
        values = {}
        for req in data["requirements"]:
            if req["version"] == version:
                for name, value in req["constraints"].items():
                    values.setdefault(name, []).append(value)
        conflicts = sorted(name for name, requested in values.items() if any(v != requested[0] for v in requested))
        accept, ignore = [], []
        for artifact in data["artifacts"]:
            valid = not conflicts and artifact["version"] == version and all(
                name in artifact["values"] and artifact["values"][name] == requested[0]
                for name, requested in values.items())
            (accept if valid else ignore).append(artifact["id"])
        return {"requirement_version": version, "status": "clarify" if conflicts else "ready" if accept else "needs_work",
                "accept": accept, "ignore": ignore, "questions": conflicts}
    if case == "INC-CAPSTONE":
        ids = [r["id"] for r in data["records"]]
        rollback = all(data["target_schema"] in row["compatible_with"] for row in data["records"])
        snapshot = data["snapshot"]
        rollback = rollback or (snapshot["verified"] and set(ids) <= set(snapshot["ids"])
                                and data["reverse_migration_tested"])
        action = "rollback" if rollback else "forward_fix" if data["forward_migration_tested"] else "stop"
        unknown = [key for key, status in data["remote"].items() if status == "unavailable"]
        ready = action != "stop" and data["verification"].get(action, False) and not unknown \
            and data["revision"] == data["evaluation_revision"]
        return {"action": action, "preserve": ids, "unknown_operations": unknown,
                "release": "ready" if ready else "blocked"}
    raise ValueError("Unknown incident")


DEBRIEFS = {
    "INC-01": "The local application is not broken. A wrapper ran zero tests, an old report described another revision, and external-clock evidence is inconsistent. Repair discovery, preserve the human edits, and distinguish current evidence from reassuring artifacts.",
    "INC-02": "Valid JSON does not establish complete coverage. Preserve missing versus null versus zero, decline ambiguous dates, and recompute a paired holdout result without training overlap or cache reuse. Do not turn a small diagnostic sample into a significance claim.",
    "INC-03": "A transport timeout does not prove a failed write. Reconcile stable operation IDs against authoritative state, deduplicate notifications, and keep unavailable outcomes unknown. A local checkpoint is an optimization, not proof of remote truth.",
    "INC-04": "Account, workspace, permissions, and skill semantics are part of the execution context. Recheck grants for every request, scope cached data precisely, and validate upgraded contracts. Revocation calls for reauthorization, not stronger automatic credentials.",
    "INC-05": "Budgets are shared, retries can synchronize, and a read is not a write lock. Admission and scheduling must respect total resources; compare-and-swap conflicts must be explicit. A valid schedule need not be the optimal schedule.",
    "INC-06": "The latest legitimate requirement supersedes a stale handoff. Late workers do not change that. Conflicting stakeholder values require clarification; passing an old rubric does not make a deliverable useful.",
    "INC-CAPSTONE": "Rollback is a data transformation, not just a version label. A snapshot missing newer records is not a lossless recovery plan. Preserve evidence and data, reconcile uncertain operations, and require verification tied to the current release.",
}


DETAILED_CONTRACTS = {
    "INC-01": """Return {"usable_reports": [report IDs], "flaky_tests": [test names],
"release": "ready" or "blocked"}. A release needs a successful report for the
current revision with at least one discovered test. Evaluate repeated executions
of each test at that revision; any observed pass AND fail requires investigation.
Also repair repository/tools/check.py to discover repository/tests from any cwd,
print JSON {"discovered": N, "failures": N}, and fail if zero tests ran.
Preserve the existing application, tests, and the human's uncommitted notes; add the requested report.py feature.
The acceptance checker evaluates report selection and wrapper behavior, including
an empty test directory. It cannot judge the quality of your incident narrative.""",
    "INC-02": """Return {"complete": bool, "records": [{"id": str, "amount_state":
"missing"|"null"|"value", "amount": number|null, "date": ISO date|null}],
"holdout_gain": number|null}. Records retain input page order. Report completeness
requires a page chain starting at cursor null and ending with next_cursor null;
duplicate, missing, unreachable, or truncated pages are incomplete.
ISO dates are accepted; numeric slash dates require an explicit DMY/MDY locale
unless only one interpretation is valid. Do not infer an ambiguous date.
Compute the candidate minus baseline mean only over paired evaluation examples
that were not training examples and were not cached in either evaluation run.
No eligible pairs means null. This is a diagnostic estimate, not significance.""",
    "INC-03": """Return {"create": [operation IDs], "notify": [operation IDs],
"unknown": [operation IDs], "checkpoint": integer}. A remote lookup has status
present, absent, or unavailable. A present operation must not be created again.
Only a confirmed-absent operation may be proposed for creation; unavailable is
unknown. Propose a notification only for a present operation whose stable
notification key is not recorded. Never advance checkpoint past an operation
that has not been observed present. The full ledger begins at sequence 1; rebuild
the confirmed contiguous checkpoint even when the local checkpoint disagrees.
Arrays follow operation sequence.
This command proposes effects; it does not perform external writes.""",
    "INC-04": """Return {"results": [{"id": str, "status": "ok"|"denied"|
"reauthorize"|"incompatible", "value": number|null, "source": str|null}]}.
Process events in order. Permissions belong to a principal AND workspace;
revocation clears that exact permission. A switch does not grant permission.
Only cache entries matching principal, workspace, query, and skill version may
be reused. Valid skill manifests declare major version 1 with units dollars,
or major version 2 with units cents. Convert valid values to dollars. Unsupported
contracts produce incompatible, even if a cache entry exists. A revoked request
requires reauthorization; a scope never granted is denied. No automatic grants.""",
    "INC-05": """Return {"schedule": [{"id": str, "start": integer}],
"spent": integer, "deferred": [job IDs],
"updates": [{"id": str, "status": "applied"|"conflict", "revision": integer}],
"final_value": number}. Schedule each job once or defer it. Starts must meet
arrival and retry_after, finish by deadline, and respect max_concurrency.
Only scheduled jobs consume their estimated token cost from the shared budget.
Jobs retrying together need distinct integer starts to avoid a synchronized burst.
Do not spend budget per worker as though each worker owned the whole pool.
Process updates in listed order with compare-and-swap expected_revision. Apply
delta only on an exact match; conflict must not overwrite the record.
The checker permits different valid schedules; it requires at least one feasible
job when a schedule exists, but does not optimize throughput for you.""",
    "INC-06": """Return {"requirement_version": integer, "status":
"ready"|"clarify"|"needs_work", "accept": [artifact IDs],
"ignore": [artifact IDs], "questions": [constraint names]}.
Use the highest requirement version, including events after a handoff.
Combine that version's stakeholder constraints. Different requested values for
one constraint require clarification; do not choose a stakeholder silently.
An artifact is accepted only if it targets that version and satisfies every
constraint. All others are ignored. Ready requires at least one accepted
artifact and no conflict. Questions list exactly the conflicting constraints.
An algorithmically valid artifact can still be useless for the current workflow.""",
    "INC-CAPSTONE": """Return {"action": "rollback"|"forward_fix"|"stop",
"preserve": [record IDs], "unknown_operations": [operation IDs],
"release": "blocked"|"ready"}. Preserve every observed record, including new
schema records. A rollback is possible only if every record can be represented
in the target schema, OR a verified snapshot includes every current record and
a tested reverse migration is available. Otherwise choose forward_fix only if
a tested forward migration is available; choose stop if neither is justified.
Unknown remote operation outcomes block release; a stale evaluation revision
also blocks it. Ready additionally requires the selected recovery path to have
its verification flag true. This is a recovery proposal, not a database migration.
Choose support, qa, or research with init --project; apply the same technical
case to that capstone's stakeholders. Explain your operational tradeoffs separately.""",
}


CORRECT_WRAPPER = '''import json
from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
suite = unittest.defaultTestLoader.discover(str(root / "tests"))
count = suite.countTestCases()
result = unittest.TextTestRunner(stream=sys.stderr).run(suite)
failures = len(result.failures) + len(result.errors)
print(json.dumps({"discovered": count, "failures": failures}))
raise SystemExit(0 if count > 0 and result.wasSuccessful() else 1)
'''
