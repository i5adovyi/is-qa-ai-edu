"""Incident simulation and learner-flow tests, including deliberately bad policies."""
import copy
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from lab.incidents import engine, reference
from lab.incidents.__main__ import main
from lab.incidents.scenarios import IDS, scenario, boundary_scenarios
from tests.link_fixtures import directory_link, file_symlink


class IncidentWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="academy-incident-test-")
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def init(self, case="INC-02", name="case", variant="primary"):
        return engine.initialize(case, self.root / name, variant)

    def solved_worker(self, workspace, case):
        implementation = Path(reference.__file__).read_text(encoding="utf-8")
        (workspace / "student.py").write_text(
            implementation + "\n\ndef handle(data):\n    return solve(%r, data)\n" % case, encoding="utf-8")
        if case == "INC-01":
            (workspace / "repository/tools/check.py").write_text(reference.CORRECT_WRAPPER, encoding="utf-8")
            (workspace / "repository/report.py").write_text(
                "from app import remaining_budget\n"
                "def format_budget(limit, used):\n"
                "    return str(remaining_budget(limit, used)) + ' remaining'\n", encoding="utf-8")

    def test_all_starters_fail_real_behavioral_checks(self):
        for case in IDS:
            with self.subTest(case=case):
                workspace = self.init(case, case)
                result = engine.check(workspace)
                self.assertFalse(result["passed"])
                self.assertGreater(len(result["failures"]), 0)
                self.assertEqual(result["workloads"], 3)
                self.assertNotIn("expected", json.dumps(result))

    def test_reference_repairs_all_cases_and_transfer_workspaces(self):
        for case in IDS:
            for variant in ("primary", "transfer"):
                with self.subTest(case=case, variant=variant):
                    workspace = self.init(case, case + variant, variant)
                    self.solved_worker(workspace, case)
                    result = engine.check(workspace)
                    self.assertTrue(result["passed"], result["failures"])

    def test_init_never_overwrites_an_existing_directory(self):
        workspace = self.init()
        before = (workspace / "input.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            engine.initialize("INC-02", workspace)
        self.assertEqual(before, (workspace / "input.json").read_bytes())

    def test_guidance_stays_closed_until_attempt_and_never_auto_reveals(self):
        workspace = self.init()
        for level in (None, 1, 2, 3):
            with self.assertRaisesRegex(ValueError, "attempt first"):
                engine.guidance(workspace, level)
        record = engine.attempt(workspace, "The evidence may describe a partial result.",
                                "input.json", "Compare the received cursor chain with the reported count.")
        self.assertNotIn("debrief", record)
        self.assertNotIn("hint", record)
        for level in (1, 2, 3):
            self.assertEqual(engine.guidance(workspace, level)["level"], level)
        self.assertIn("debrief", engine.guidance(workspace))

    def test_canonical_case_specific_hints_are_used(self):
        workspace = self.init()
        engine.attempt(workspace, "My hypothesis needs a coverage check.", "input.json",
                       "Inspect every returned page before accepting the total.")
        canonical = json.loads((Path(__file__).resolve().parents[1] / "content/incidents.json").read_text())
        item = next(row for row in canonical["incidents"] if row["id"] == "INC-02")
        self.assertEqual(engine.guidance(workspace, 1)["hint"], item["hints"][0])
        self.assertEqual(engine.guidance(workspace)["debrief"], item["debrief"])

    def test_attempt_requires_specific_text_and_real_evidence(self):
        workspace = self.init()
        for hypothesis, evidence_file, next_check in [
            ("?", "input.json", "Inspect the actual returned pages."),
            ("A plausible hypothesis exists.", "missing.json", "Inspect the actual returned pages."),
            ("A plausible hypothesis exists.", "input.json", "?"),
        ]:
            with self.subTest(evidence=evidence_file, hypothesis=hypothesis):
                with self.assertRaises(ValueError):
                    engine.attempt(workspace, hypothesis, evidence_file, next_check)
        self.assertFalse((workspace / ".incident-attempts.json").exists())

    def test_attempt_evidence_cannot_escape_workspace(self):
        workspace = self.init()
        outside = self.root / "outside.txt"
        outside.write_text("private unrelated material")
        directory_link(workspace / "external", self.root)
        for path in ("../outside.txt", str(outside), "external/outside.txt"):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    engine.attempt(workspace, "A plausible hypothesis exists.", path,
                                   "Inspect the actual returned pages.")
        with self.subTest(link="file symlink"):
            file_symlink(workspace / "outside-link", outside)
            with self.assertRaises(ValueError):
                engine.attempt(workspace, "A plausible hypothesis exists.", "outside-link",
                               "Inspect the actual returned pages.")

    def test_worker_path_and_runs_path_cannot_escape_workspace(self):
        workspace = self.init()
        target = self.root / "worker.py"
        target.write_text("def handle(data): return {}")
        (workspace / "student.py").unlink()
        with self.subTest(link="worker file symlink"):
            file_symlink(workspace / "student.py", target)
            with self.assertRaisesRegex(ValueError, "inside"):
                engine.run(workspace)
            (workspace / "student.py").unlink()
        (workspace / "student.py").write_text("def handle(data): return {}")
        (workspace / "runs").rmdir()
        directory_link(workspace / "runs", self.root)
        with self.assertRaisesRegex(ValueError, "inside"):
            engine.run(workspace)

    def test_runs_and_checks_retain_immutable_prior_evidence(self):
        workspace = self.init()
        first = engine.run(workspace)
        first_path = workspace / first["record"]
        first_bytes = first_path.read_bytes()
        checked = engine.check(workspace)
        checked_path = workspace / checked["record"]
        checked_bytes = checked_path.read_bytes()
        self.solved_worker(workspace, "INC-02")
        second = engine.run(workspace)
        second_checked = engine.check(workspace)
        self.assertNotEqual(first["record"], second["record"])
        self.assertNotEqual(first["worker_sha256"], second["worker_sha256"])
        self.assertNotEqual(checked["record"], second_checked["record"])
        self.assertEqual(first_path.read_bytes(), first_bytes)
        self.assertEqual(checked_path.read_bytes(), checked_bytes)
        self.assertTrue(second_checked["passed"])

    def test_changed_evidence_stops_before_worker_execution(self):
        workspace = self.init()
        (workspace / "input.json").write_text("{}")
        (workspace / "student.py").write_text(
            "from pathlib import Path\n"
            "def handle(data):\n    Path('worker-ran').write_text('bad')\n    return {}\n")
        result = engine.check(workspace)
        self.assertFalse(result["passed"])
        self.assertEqual(result["workloads"], 0)
        self.assertFalse((workspace / "worker-ran").exists())
        with self.assertRaisesRegex(ValueError, "Baseline"):
            engine.run(workspace)

    def test_worker_cannot_silently_rewrite_protected_evidence(self):
        workspace = self.init()
        (workspace / "student.py").write_text(
            "from pathlib import Path\n"
            "def handle(data):\n    Path('input.json').write_text('{}')\n    return {}\n")
        with self.assertRaisesRegex(ValueError, "protected evidence"):
            engine.run(workspace)
        failure = json.loads((workspace / "runs/run-00001.json").read_text())
        self.assertIn("protected evidence", failure["error"])

    def test_source_mutation_is_recorded_and_stops_followup_workloads(self):
        workspace = self.init()
        (workspace / "student.py").write_text(
            "from pathlib import Path\n"
            "def handle(data):\n    Path('student.py').write_text('def handle(data): return {}')\n    return {}\n")
        before = engine._hash(workspace / "student.py")
        result = engine.check(workspace)
        self.assertFalse(result["passed"])
        self.assertEqual(result["workloads"], 1)
        self.assertEqual(result["worker_sha256"], before)
        self.assertIn("further execution stopped", json.dumps(result))

    def test_worker_timeout_and_invalid_output_are_reported(self):
        workspace = self.init()
        (workspace / "student.py").write_text("import time\ndef handle(data): time.sleep(2)\n")
        with self.assertRaisesRegex(ValueError, "execution limit"):
            engine.invoke(workspace, {}, timeout=0.05)
        (workspace / "student.py").write_text("def handle(data): print('debug'); return {}\n")
        with self.assertRaisesRegex(ValueError, "JSON-compatible"):
            engine.invoke(workspace, {})
        (workspace / "student.py").write_text("def handle(data): return []\n")
        with self.assertRaisesRegex(ValueError, "JSON object"):
            engine.invoke(workspace, {})
        (workspace / "student.py").write_text(
            "import json\n"
            "def handle(data):\n    print('{\"complete\":NaN}')\n    raise SystemExit(0)\n")
        with self.assertRaisesRegex(ValueError, "JSON-compatible"):
            engine.invoke(workspace, {})

    def test_git_fixture_keeps_human_work_and_has_no_initial_app_failure(self):
        workspace = self.init("INC-01")
        repo = workspace / "repository"
        before = (repo / "operator-notes.txt").read_bytes()
        status = subprocess.check_output(["git", "status", "--short"], cwd=repo, text=True)
        self.assertIn(" M operator-notes.txt", status)
        proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                              cwd=repo, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Ran 3 tests", proc.stderr)
        self.solved_worker(workspace, "INC-01")
        self.assertTrue(engine.check(workspace)["passed"])
        self.assertEqual(before, (repo / "operator-notes.txt").read_bytes())

    def test_wrapper_hardcoded_green_is_rejected_on_empty_suite(self):
        workspace = self.init("INC-01")
        self.solved_worker(workspace, "INC-01")
        (workspace / "repository/tools/check.py").write_text(
            "print('{\"discovered\": 3, \"failures\": 0}')\n")
        result = engine.check(workspace)
        self.assertFalse(result["passed"])
        self.assertIn("zero discovered", json.dumps(result))

    def test_wrapper_must_fail_nonempty_assertions_and_errors(self):
        workspace = self.init("INC-01")
        self.solved_worker(workspace, "INC-01")
        (workspace / "repository/tools/check.py").write_text(reference.CORRECT_WRAPPER.replace(
            "count > 0 and result.wasSuccessful()", "count > 0"))
        result = engine.check(workspace)
        self.assertFalse(result["passed"])
        self.assertIn("nonempty assertion", json.dumps(result))
        self.assertIn("nonempty error", json.dumps(result))

    def test_learner_can_add_feature_tests_without_breaking_wrapper_acceptance(self):
        workspace = self.init("INC-01")
        self.solved_worker(workspace, "INC-01")
        (workspace / "repository/tests/test_report.py").write_text(
            "import unittest\nfrom report import format_budget\n"
            "class ReportTest(unittest.TestCase):\n"
            "    def test_label(self): self.assertEqual(format_budget(10, 3), '7 remaining')\n")
        result = engine.check(workspace)
        self.assertTrue(result["passed"], result["failures"])

    def test_missing_or_incorrect_requested_feature_is_rejected(self):
        workspace = self.init("INC-01")
        self.solved_worker(workspace, "INC-01")
        (workspace / "repository/report.py").write_text(
            "def format_budget(limit, used): return str(limit-used) + ' remaining'\n")
        self.assertFalse(engine.check(workspace)["passed"])

    def test_cli_expected_exit_codes(self):
        workspace = self.init()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["check", "--workspace", str(workspace)]), 1)
            self.assertEqual(main(["debrief", "--workspace", str(workspace)]), 2)
            self.solved_worker(workspace, "INC-02")
            self.assertEqual(main(["check", "--workspace", str(workspace)]), 0)


class IncidentBehaviorTests(unittest.TestCase):
    def test_required_null_and_boolean_numeric_types_cannot_false_pass(self):
        data = dict(boundary_scenarios("INC-02"))["boundary"]
        out = reference.solve("INC-02", data)
        del out["holdout_gain"]
        out["complete"] = 0
        issues = engine.evaluate("INC-02", data, out)
        self.assertIn("required field is missing: holdout_gain", issues)
        self.assertIn("contract assertion failed for complete", issues)
        data = scenario("INC-03")
        out = reference.solve("INC-03", data)
        out["checkpoint"] = True
        self.assertTrue(engine.evaluate("INC-03", data, out))
        out["checkpoint"] = 1.0
        self.assertTrue(engine.evaluate("INC-03", data, out))

    def test_nested_required_fields_and_finite_numeric_values_are_checked(self):
        data = scenario("INC-02")
        out = reference.solve("INC-02", data)
        del out["records"][0]["amount"]
        self.assertTrue(engine.evaluate("INC-02", data, out))
        for bad in (True, float("nan"), float("inf")):
            out = reference.solve("INC-02", data)
            out["holdout_gain"] = bad
            self.assertTrue(engine.evaluate("INC-02", data, out))
        out = reference.solve("INC-02", data)
        out["records"][2]["amount"] = 0.0
        self.assertEqual(engine.evaluate("INC-02", data, out), [])

    def test_every_case_has_distinct_transfer_and_boundary_workloads(self):
        for case in IDS:
            primary = scenario(case)
            self.assertNotEqual(primary, scenario(case, "transfer"), case)
            self.assertEqual(len(list(boundary_scenarios(case))), 2)

    def test_report_gate_rejects_old_and_empty_runs_and_detects_inconsistency(self):
        data = scenario("INC-01")
        result = reference.solve("INC-01", data)
        self.assertEqual(result["usable_reports"], [])
        self.assertEqual(result["flaky_tests"], ["external_clock"])
        self.assertEqual(result["release"], "blocked")
        result = reference.solve("INC-01", scenario("INC-01", "transfer"))
        self.assertEqual(result["release"], "ready")

    def test_page_coverage_handles_missing_duplicate_and_unreachable_pages(self):
        clean = scenario("INC-02", "transfer")
        self.assertTrue(reference.solve("INC-02", clean)["complete"])
        for mutation in ("missing", "duplicate", "unreachable", "truncated"):
            data = copy.deepcopy(clean)
            if mutation == "missing":
                data["pages"].pop()
            elif mutation == "duplicate":
                data["pages"].append(copy.deepcopy(data["pages"][0]))
            elif mutation == "unreachable":
                data["pages"][1]["cursor"] = "elsewhere"
            else:
                data["pages"][1]["truncated"] = True
            self.assertFalse(reference.solve("INC-02", data)["complete"], mutation)

    def test_missing_null_zero_and_ambiguous_dates_stay_distinct(self):
        result = reference.solve("INC-02", scenario("INC-02"))
        self.assertEqual([row["amount_state"] for row in result["records"]], ["missing", "null", "value"])
        self.assertEqual([row["amount"] for row in result["records"]], [None, None, 0])
        self.assertEqual([row["date"] for row in result["records"]], [None, "2026-04-03", "2026-04-13"])
        data = scenario("INC-02", "transfer")
        self.assertEqual(reference.solve("INC-02", data)["records"][0]["date"], "2026-04-03")
        data["locale"] = "MDY"
        self.assertEqual(reference.solve("INC-02", data)["records"][0]["date"], "2026-03-04")
        data["pages"][0]["records"][0]["date"] = "2026-02-30"
        self.assertIsNone(reference.solve("INC-02", data)["records"][0]["date"])

    def test_holdout_removes_both_training_and_cache_contamination(self):
        data = scenario("INC-02")
        self.assertEqual(reference.solve("INC-02", data)["holdout_gain"], -1)
        data["evaluation"][-1]["baseline_cached"] = True
        self.assertIsNone(reference.solve("INC-02", data)["holdout_gain"])

    def test_remote_timeout_does_not_create_duplicates_or_advance_past_unknown(self):
        data = scenario("INC-03")
        result = reference.solve("INC-03", data)
        self.assertEqual(result, {"create": ["delivery-3"], "notify": [],
                                  "unknown": ["delivery-2"], "checkpoint": 1})
        data["local_checkpoint"] = 3
        self.assertEqual(reference.solve("INC-03", data), result)

    def test_remote_reconciliation_supports_replay_and_new_notification(self):
        data = scenario("INC-03", "transfer")
        first = reference.solve("INC-03", data)
        self.assertEqual(first["notify"], ["delivery-1", "delivery-2"])
        data["notifications"] += first["notify"]
        data["remote"]["delivery-3"] = "present"
        second = reference.solve("INC-03", data)
        self.assertEqual(second["create"], [])
        self.assertEqual(second["notify"], ["delivery-3"])
        self.assertEqual(second["checkpoint"], 3)

    def test_identity_change_revocation_and_upgrade_are_independent(self):
        result = reference.solve("INC-04", scenario("INC-04"))["results"]
        self.assertEqual(result[0]["value"], 123.45)
        self.assertEqual(result[0]["source"], "tool")
        self.assertEqual(result[1]["status"], "denied")
        self.assertEqual(result[2]["status"], "reauthorize")
        transfer = reference.solve("INC-04", scenario("INC-04", "transfer"))["results"]
        self.assertEqual([r["status"] for r in transfer], ["incompatible", "incompatible", "reauthorize"])

    def test_cache_requires_all_scope_fields_and_supported_contract(self):
        data = scenario("INC-04")
        cache = {"principal": "alex", "workspace": "support", "query": "balance",
                 "skill_version": "2.1", "value": 456}
        data["cache"] = [cache]
        self.assertEqual(reference.solve("INC-04", data)["results"][0]["value"], 4.56)
        self.assertEqual(reference.solve("INC-04", data)["results"][0]["source"], "cache")
        for key in ("principal", "workspace", "query", "skill_version"):
            changed = copy.deepcopy(data)
            changed["cache"][0][key] = "mismatch"
            self.assertEqual(reference.solve("INC-04", changed)["results"][0]["source"], "tool")

    def test_schedule_checker_accepts_different_valid_nonoverlapping_plans(self):
        data = scenario("INC-05")
        out = reference.solve("INC-05", data)
        self.assertEqual(engine.evaluate("INC-05", data, out), [])
        out["schedule"] = [{"id": "job-2", "start": 5}]
        out["deferred"] = ["job-1", "job-3"]
        out["spent"] = 5
        self.assertEqual(engine.evaluate("INC-05", data, out), [])

    def test_schedule_rejects_budget_burst_conflict_and_no_work_policies(self):
        data = scenario("INC-05")
        good = reference.solve("INC-05", data)
        for mutation in ("budget", "burst", "conflict", "empty", "duplicate", "late"):
            out = copy.deepcopy(good)
            if mutation == "budget":
                out["spent"] = 100
            elif mutation == "burst":
                out["schedule"][1]["start"] = out["schedule"][0]["start"]
            elif mutation == "conflict":
                out["updates"][1]["status"] = "applied"
            elif mutation == "empty":
                out.update(schedule=[], deferred=[j["id"] for j in data["jobs"]], spent=0)
            elif mutation == "duplicate":
                out["schedule"].append(copy.deepcopy(out["schedule"][0]))
            else:
                out["schedule"][0]["start"] = data["deadline"]
            self.assertTrue(engine.evaluate("INC-05", data, out), mutation)

    def test_scheduler_measures_simultaneous_occupancy_not_total_overlap(self):
        data = scenario("INC-05")
        data.update(budget=30, max_concurrency=2, deadline=6)
        data["jobs"] = [
            {"id": "a", "arrival": 0, "retry_after": 0, "duration": 3, "cost": 1, "retry": False},
            {"id": "b", "arrival": 3, "retry_after": 3, "duration": 3, "cost": 1, "retry": False},
            {"id": "c", "arrival": 0, "retry_after": 0, "duration": 6, "cost": 1, "retry": False},
        ]
        result = reference.solve("INC-05", data)
        self.assertEqual(len(result["schedule"]), 3)
        self.assertEqual(engine.evaluate("INC-05", data, result), [])

    def test_old_requirement_and_passing_demo_do_not_settle_stakeholder_conflict(self):
        primary = reference.solve("INC-06", scenario("INC-06"))
        self.assertEqual(primary["status"], "clarify")
        self.assertEqual(primary["questions"], ["mode"])
        self.assertEqual(primary["accept"], [])
        transfer = reference.solve("INC-06", scenario("INC-06", "transfer"))
        self.assertEqual(transfer["accept"], ["operator-draft"])
        self.assertIn("late-worker", transfer["ignore"])
        self.assertEqual(transfer["requirement_version"], 2)

    def test_capstone_partial_snapshot_does_not_allow_data_loss(self):
        data = scenario("INC-CAPSTONE")
        result = reference.solve("INC-CAPSTONE", data)
        self.assertEqual(result["action"], "stop")
        self.assertEqual(result["preserve"], ["old-record", "new-record"])
        data["reverse_migration_tested"] = True
        self.assertEqual(reference.solve("INC-CAPSTONE", data)["action"], "stop")
        data["snapshot"]["ids"].append("new-record")
        self.assertEqual(reference.solve("INC-CAPSTONE", data)["action"], "rollback")

    def test_capstone_verification_revision_and_unknowns_each_block_release(self):
        data = scenario("INC-CAPSTONE", "transfer")
        self.assertEqual(reference.solve("INC-CAPSTONE", data)["release"], "ready")
        for mutation in ("verification", "revision", "unknown"):
            changed = copy.deepcopy(data)
            if mutation == "verification":
                changed["verification"]["forward_fix"] = False
            elif mutation == "revision":
                changed["evaluation_revision"] = "unrelated"
            else:
                changed["remote"]["case-2"] = "unavailable"
            self.assertEqual(reference.solve("INC-CAPSTONE", changed)["release"], "blocked", mutation)


if __name__ == "__main__":
    unittest.main()
