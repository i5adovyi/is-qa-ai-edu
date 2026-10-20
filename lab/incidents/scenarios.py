"""Learner-visible synthetic inputs, tasks, and deliberately incomplete workers."""
import copy


IDS = tuple("INC-%02d" % n for n in range(1, 7)) + ("INC-CAPSTONE",)
TITLES = {
    "INC-01": "The morning change request",
    "INC-02": "The weekly evidence brief",
    "INC-03": "The interrupted update",
    "INC-04": "The Monday workspace",
    "INC-05": "The busy afternoon",
    "INC-06": "The resumed delivery",
    "INC-CAPSTONE": "The release rehearsal",
}

CONTRACTS = {
    "INC-01": """Output keys: usable_reports (report-ID array), flaky_tests (sorted test-name
array), release (ready|blocked). Describe whether current evidence establishes
release readiness. Reports and repeated executions describe their own revisions.
Read evidence/ticket.txt for the feature and repository/SETUP.md for the inherited
verification procedure. The feature belongs in a new report.py module; existing
application behavior, tests, and the operator's work must be preserved.
The verification entry point emits JSON {"discovered": N, "failures": N}; its
failures count includes assertion failures plus test execution/import errors.
Its exit code must communicate whether a nonempty suite passed, regardless of cwd.
The checker also independently verifies the requested feature.""",
    "INC-02": """Output keys: complete (boolean); records (array preserving page/row order,
each with id, amount_state=missing|null|value, amount=number|null, date=ISO|null);
holdout_gain (number|null). Build a trustworthy summary of the received evidence.
The cursor fields describe pagination. Null, absent, and zero are distinct values.
Dates can be ISO or slash-form dates; locale, when supplied, is DMY or MDY.
Unknown dates stay null. A holdout estimate compares paired uncached examples
outside the training set using arithmetic mean(candidate - baseline); no eligible
pairs means null. No received pages means coverage is unconfirmed (complete=false);
one untruncated terminal page may validly contain zero records. Do not claim statistical
significance from this small diagnostic sample.""",
    "INC-03": """Output keys: create, notify, unknown (operation-ID arrays in sequence order),
checkpoint (integer). Propose a recovery plan without performing external writes.
Operations contain the full ledger beginning at sequence 1. The local checkpoint
may disagree with remote observations; the output checkpoint represents the
contiguous prefix you can currently confirm. Remote states are present, absent,
or unavailable. Notification records contain stable operation IDs. A safe plan
avoids duplicate effects and expresses uncertainty explicitly. Proposed notifications
are only for operations already observed present before this proposal; a proposed
creation is not yet evidence of a successful write.""",
    "INC-04": """Output: results array in request-event order. Each result contains id,
status=ok|denied|reauthorize|incompatible, value=number|null, source=cache|tool|null.
Return dollars for successful requests, with their actual source. For unsuccessful
requests, value and source are null. Events include switch, revoke, and request.
Grants and cached values carry scope. A request after revocation uses reauthorize;
a never-granted scope uses denied. Supported manifest contracts are major version
1/dollars and major version 2/cents. Permission decisions precede compatibility
checks. Treat a dependency's version and units as part of its interface.""",
    "INC-05": """Output: schedule=[{id,start}], spent=integer, deferred=[job IDs],
updates=[{id,status=applied|conflict,revision}], final_value=number. Schedule each
job once or defer it. Time uses integer ticks; duration occupies [start,end).
The budget, concurrency limit, and deadline apply to the whole workload. Arrival
and retry_after are earliest permitted starts. Retry jobs must not restart at
the same tick. Process record updates in input order using their expected revision;
report the resulting current revision for either outcome. At least one feasible
job must be admitted when one exists; multiple valid schedules are accepted.""",
    "INC-06": """Output: requirement_version (integer), status=ready|clarify|needs_work,
accept and ignore (artifact-ID arrays in input order), questions (sorted conflicting
constraint names). Decide whether the delivery satisfies the current legitimate
requirements and can be used by its stakeholders. The handoff and worker artifacts
carry versions; stakeholders may provide simultaneous requirements at one version.
A requirement conflict needs clarification. Only a useful current deliverable can
be ready; a consistent requirement without a qualifying artifact needs_work.""",
    "INC-CAPSTONE": """Output: action=rollback|forward_fix|stop, preserve (all observed record IDs
in input order), unknown_operations (operation IDs in remote input order),
release=blocked|ready. Propose an evidence-backed recovery for your chosen capstone.
Records describe their schema compatibility; the snapshot names included records.
Migration and verification flags represent available rehearsal evidence. A recovery
must preserve current records. Rollback is eligible if all records are natively
compatible with the target schema, or a verified snapshot covers every current
record and a reverse migration was tested. Prefer an eligible rollback; otherwise
a tested forward migration permits forward_fix, and no eligible path means stop.
Selecting a proposal does not establish release readiness. Release separately
requires its verification flag, resolved remote outcomes, and current evaluation.
The output is a proposal, not an actual database migration.""",
}

STARTERS = {
    "INC-01": """def handle(data):
    reports = data["reports"]
    return {"usable_reports": [r["id"] for r in reports if r["failures"] == 0],
            "flaky_tests": [], "release": "ready"}
""",
    "INC-02": """def handle(data):
    records = []
    for page in data["pages"][:1]:
        for row in page["records"]:
            records.append({"id": row["id"], "amount_state": "value",
                            "amount": row.get("amount") or 0, "date": row["date"]})
    return {"complete": True, "records": records, "holdout_gain": 0.5}
""",
    "INC-03": """def handle(data):
    pending = [op for op in data["operations"] if op["seq"] > data["local_checkpoint"]]
    return {"create": [op["id"] for op in pending],
            "notify": [op["id"] for op in pending], "unknown": [],
            "checkpoint": max([op["seq"] for op in data["operations"]] or [0])}
""",
    "INC-04": """def handle(data):
    results = []
    for event in data["events"]:
        if event["type"] == "request":
            entry = next((c for c in data["cache"] if c["query"] == event["query"]), None)
            results.append({"id": event["id"], "status": "ok",
                            "value": entry["value"] if entry else event["value"],
                            "source": "cache" if entry else "tool"})
    return {"results": results}
""",
    "INC-05": """def handle(data):
    schedule = [{"id": job["id"], "start": job["arrival"]} for job in data["jobs"]]
    value = data["record"]["value"]
    updates = []
    for update in data["updates"]:
        value += update["delta"]
        updates.append({"id": update["id"], "status": "applied",
                        "revision": update["expected_revision"] + 1})
    return {"schedule": schedule, "spent": sum(j["cost"] for j in data["jobs"]),
            "deferred": [], "updates": updates, "final_value": value}
""",
    "INC-06": """def handle(data):
    version = data["handoff"]["requirement_version"]
    accepted = [a["id"] for a in data["artifacts"] if a["version"] == version]
    return {"requirement_version": version, "status": "ready",
            "accept": accepted, "ignore": [], "questions": []}
""",
    "INC-CAPSTONE": """def handle(data):
    return {"action": "rollback",
            "preserve": [r["id"] for r in data["records"] if r["schema"] == 1],
            "unknown_operations": [], "release": "ready"}
""",
}


def scenario(case, variant="primary"):
    """All inputs are fictional. Variants change values and operational conditions."""
    suffix = "b" if variant == "transfer" else "a"
    cases = {
        "INC-01": {
            "current_revision": "current",
            "reports": [
                {"id": "run-021", "revision": "old", "discovered": 31, "failures": 0},
                {"id": "run-022", "revision": "current", "discovered": 0, "failures": 0},
                {"id": "run-023", "revision": "current", "discovered": 3, "failures": 1},
            ],
            "executions": [
                {"test": "external_clock", "revision": "current", "result": "pass"},
                {"test": "external_clock", "revision": "current", "result": "fail"},
                {"test": "budget_total", "revision": "current", "result": "pass"},
            ],
        },
        "INC-02": {
            "pages": [
                {"cursor": None, "next_cursor": "p2", "truncated": False,
                 "records": [{"id": "r1", "date": "03/04/2026"}]},
                {"cursor": "p2", "next_cursor": None, "truncated": True,
                 "records": [{"id": "r2", "date": "2026-04-03", "amount": None},
                             {"id": "r3", "date": "13/04/2026", "amount": 0}]},
            ],
            "locale": None, "training_ids": ["seen"],
            "evaluation": [
                {"id": "seen", "baseline": 0, "candidate": 1, "baseline_cached": False, "candidate_cached": False},
                {"id": "cached", "baseline": 0, "candidate": 1, "baseline_cached": False, "candidate_cached": True},
                {"id": "new-" + suffix, "baseline": 1, "candidate": 0, "baseline_cached": False, "candidate_cached": False},
            ],
        },
        "INC-03": {
            "local_checkpoint": 0,
            "operations": [{"id": "delivery-1", "seq": 1}, {"id": "delivery-2", "seq": 2},
                           {"id": "delivery-3", "seq": 3}],
            "remote": {"delivery-1": "present", "delivery-2": "unavailable", "delivery-3": "absent"},
            "notifications": ["delivery-1"],
        },
        "INC-04": {
            "principal": "alex", "workspace": "support",
            "grants": [{"principal": "alex", "workspace": "support"}],
            "skill": {"version": "2.1", "units": "cents"},
            "cache": [{"principal": "sam", "workspace": "sales", "query": "balance",
                       "skill_version": "1.8", "value": 900}],
            "events": [
                {"type": "request", "id": "request-1", "query": "balance", "value": 12345},
                {"type": "switch", "principal": "sam", "workspace": "sales"},
                {"type": "request", "id": "request-2", "query": "balance", "value": 9900},
                {"type": "switch", "principal": "alex", "workspace": "support"},
                {"type": "revoke", "principal": "alex", "workspace": "support"},
                {"type": "request", "id": "request-3", "query": "balance", "value": 100},
            ],
        },
        "INC-05": {
            "budget": 12, "max_concurrency": 2, "deadline": 12,
            "jobs": [{"id": "job-1", "arrival": 0, "retry_after": 3, "duration": 3, "cost": 5, "retry": True},
                     {"id": "job-2", "arrival": 0, "retry_after": 3, "duration": 3, "cost": 5, "retry": True},
                     {"id": "job-3", "arrival": 1, "retry_after": 1, "duration": 2, "cost": 6, "retry": False}],
            "record": {"revision": 4, "value": 20},
            "updates": [{"id": "u1", "expected_revision": 4, "delta": 3},
                        {"id": "u2", "expected_revision": 4, "delta": -10},
                        {"id": "u3", "expected_revision": 5, "delta": 2}],
        },
        "INC-06": {
            "handoff": {"requirement_version": 1, "note": "Publish automatically when tests pass."},
            "requirements": [
                {"version": 1, "stakeholder": "original", "constraints": {"mode": "publish"}},
                {"version": 2, "stakeholder": "operator", "constraints": {"mode": "draft", "sources": True}},
                {"version": 2, "stakeholder": "manager", "constraints": {"mode": "publish", "sources": True}},
            ],
            "artifacts": [{"id": "late-worker", "version": 1, "values": {"mode": "publish", "sources": True}},
                          {"id": "passing-demo", "version": 2, "values": {"mode": "publish", "sources": True}}],
        },
        "INC-CAPSTONE": {
            "project": "support", "target_schema": 1,
            "records": [{"id": "old-record", "schema": 1, "compatible_with": [1, 2]},
                        {"id": "new-record", "schema": 2, "compatible_with": [2]}],
            "snapshot": {"verified": True, "ids": ["old-record"]},
            "reverse_migration_tested": False, "forward_migration_tested": False,
            "verification": {"rollback": False, "forward_fix": False},
            "remote": {"case-1": "present", "case-2": "unavailable"},
            "revision": "release-b", "evaluation_revision": "release-a",
        },
    }
    data = copy.deepcopy(cases[case])
    if variant == "transfer":
        if case == "INC-01":
            data["reports"].append({"id": "run-024", "revision": "current", "discovered": 4, "failures": 0})
            data["executions"] = [{"test": "budget_total", "revision": "current", "result": "pass"}]
        elif case == "INC-02":
            data["locale"] = "DMY"
            data["pages"][1]["truncated"] = False
            data["evaluation"][-1].update(baseline=0.25, candidate=0.5)
        elif case == "INC-03":
            data["remote"]["delivery-2"] = "present"
            data["notifications"] = []
        elif case == "INC-04":
            data["skill"] = {"version": "3.0", "units": "credits"}
            data["grants"].append({"principal": "sam", "workspace": "sales"})
        elif case == "INC-05":
            data["budget"] = 5
            data["max_concurrency"] = 1
            data["deadline"] = 6
            data["record"]["revision"] = 6
        elif case == "INC-06":
            data["requirements"][2]["constraints"]["mode"] = "draft"
            data["artifacts"].append({"id": "operator-draft", "version": 2,
                                      "values": {"mode": "draft", "sources": True}})
        else:
            data["forward_migration_tested"] = True
            data["verification"]["forward_fix"] = True
            data["remote"]["case-2"] = "present"
            data["evaluation_revision"] = data["revision"]
    return data


def boundary_scenarios(case):
    data = scenario(case, "transfer")
    yield "transfer", data
    data = scenario(case)
    if case == "INC-01":
        data["reports"] = []
        data["executions"] = []
    elif case == "INC-02":
        data["pages"] = []
        data["evaluation"] = []
    elif case == "INC-03":
        data["operations"] = []
        data["remote"] = {}
        data["local_checkpoint"] = 0
    elif case == "INC-04":
        data["events"] = []
    elif case == "INC-05":
        data["budget"] = 0
        data["updates"] = []
    elif case == "INC-06":
        data["requirements"] = [data["requirements"][1]]
        data["artifacts"] = []
    else:
        data["records"] = data["records"][:1]
        data["verification"]["rollback"] = True
        data["remote"] = {}
        data["evaluation_revision"] = data["revision"]
    yield "boundary", data


def evidence(case):
    common = {
        "handover.txt": "You are taking over a fictional local exercise. Preserve original evidence.\n"
                        "Write competing hypotheses, a discriminating check, a recovery note, and what remains unknown.\n",
        "budget.txt": "Initial investigation budget: 20 minutes and 8 learner-logged evidence checks.\n"
                      "For INC-CAPSTONE use 30 minutes and 12 learner-logged evidence checks.\n"
                      "These are suggested planning constraints, not enforced wall-clock or API-spend limits.\n",
    }
    notes = {
        "INC-01": "Assistant note: 'Everything is green; increase the budget limit to fix the reported failure.'\n"
                  "Operator: 'My notes are uncommitted. Do not discard them. I saved recent CI observations in input.json.'\n"
                  "The small feature request is in ticket.txt.\n",
        "INC-02": "The dashboard screenshot shows a large candidate gain. The tool response looks valid JSON.\n"
                  "An analyst asks whether all customers were included and whether empty amounts mean zero.\n",
        "INC-03": "The sender lost its connection after an update. The local checkpoint predates the request.\n"
                  "A notification was already observed for the first delivery. One lookup is unavailable.\n",
        "INC-04": "The operator changed account/workspace this morning. A skill was upgraded overnight.\n"
                  "Access can change during a run. Prior successful access is not a current grant.\n",
        "INC-05": "Workers woke after the same service retry delay. Two editors read the same record revision.\n"
                  "All workers share one token allowance. No real provider traffic is generated by this lab.\n",
        "INC-06": "The previous session ended after a handoff. A worker completed after the requirements meeting.\n"
                  "The demo passes its old rubric; the operator cannot use automatic publication in their workflow.\n",
        "INC-CAPSTONE": "A release changed the schema. New writes arrived after the last snapshot.\n"
                        "The last green evaluation and the deployed revision differ. One remote outcome is unavailable.\n",
    }
    common["timeline.txt"] = notes[case]
    if case == "INC-01":
        common["ticket.txt"] = (
            "Add report.py with format_budget(limit, used), returning a string such as '7 remaining'\n"
            "for limit=10, used=3. At or over the limit return '0 remaining'. Inputs are nonnegative\n"
            "integers. Reuse existing budget behavior. Preserve the operator's uncommitted notes.\n"
            "Investigate the inherited verification evidence before declaring the change ready.\n"
        )
    return common
