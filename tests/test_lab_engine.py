import importlib.util
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from lab.cli import main
from lab.contracts import Budget, HarnessError, SimulatedCrash
from lab.engine import Runner, get_case, load_cases
from lab.evaluation import evaluate
from lab.practice import check_lesson
from lab.storage import digest, read_trace


class EngineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_scenario(self, scenario):
        runner = Runner(self.root / scenario, scenario=scenario)
        return runner, runner.run()

    def test_normal_run_creates_grounded_local_draft(self):
        runner, result = self.run_scenario("normal")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["decision"]["citations"], ["KB-BILL-01"])
        self.assertEqual(runner.store.data["writes"], 1)

    def test_instruction_attack_escalates_without_write(self):
        runner, result = self.run_scenario("injection")
        self.assertEqual(result["status"], "escalated")
        self.assertEqual(runner.store.data["writes"], 0)

    def test_timeout_once_retries_successfully(self):
        runner, result = self.run_scenario("timeout-once")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(runner.state["retries"], 1)
        self.assertEqual(result["usage"]["tool_calls"], 4)

    def test_repeated_timeouts_stop_after_one_retry(self):
        runner, result = self.run_scenario("timeout-always")
        self.assertEqual(result["error"], "tool_timeout")
        self.assertEqual(runner.state["retries"], 1)
        self.assertEqual(result["usage"]["tool_calls"], 3)
        self.assertEqual(result["draft_count"], 0)

    def test_no_unbounded_tool_loop(self):
        runner, result = self.run_scenario("budget")
        self.assertEqual(result["error"], "budget_exhausted")
        self.assertEqual(result["usage"]["tool_calls"], 2)
        self.assertEqual(result["draft_count"], 0)

    def test_virtual_deadline_includes_timeout_cost(self):
        runner = Runner(self.root / "deadline", scenario="timeout-once",
                        budget=Budget(max_virtual_ms=80))
        result = runner.run()
        self.assertEqual(result["error"], "budget_exhausted")
        self.assertEqual(runner.state["retries"], 0)

    def test_recovery_replays_committed_write_and_preserves_usage(self):
        path = self.root / "crash"
        runner = Runner(path, scenario="crash-after-write")
        with self.assertRaises(SimulatedCrash):
            runner.run()
        self.assertEqual(runner.store.data["writes"], 1)
        used_before = runner.usage.tool_calls
        resumed = Runner(path, resume=True)
        result = resumed.run()
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["writes"], 1)
        self.assertEqual(result["draft_count"], 1)
        self.assertEqual(result["usage"]["tool_calls"], used_before + 1)
        self.assertTrue(any(event.get("replayed") for event in read_trace(path / "trace.jsonl")))

    def test_done_checkpoint_does_not_mutate_again(self):
        runner, before = self.run_scenario("normal")
        trace_before = runner.trace.path.read_text()
        after = Runner(runner.run_dir, resume=True).run()
        self.assertEqual(before, after)
        self.assertEqual(runner.store.data["writes"], 1)
        self.assertEqual(runner.trace.path.read_text(), trace_before)

    def test_duplicate_scenario_has_one_write(self):
        runner, result = self.run_scenario("duplicate")
        self.assertEqual(result["writes"], 1)
        self.assertEqual(result["usage"]["tool_calls"], 4)

    def test_denied_tag_does_not_undo_existing_draft(self):
        runner, result = self.run_scenario("denied-tag")
        self.assertEqual(result["error"], "approval_required")
        self.assertEqual(result["draft_count"], 1)
        self.assertEqual(runner.store.data["tags"], [])

    def test_corrupt_checkpoint_rejected(self):
        runner, _ = self.run_scenario("normal")
        path = runner.checkpoint_path
        data = json.loads(path.read_text())
        data["payload"]["state"]["phase"] = "save"
        path.write_text(json.dumps(data))
        with self.assertRaises(HarnessError) as caught:
            Runner(runner.run_dir, resume=True)
        self.assertEqual(caught.exception.code, "checkpoint_corrupt")

    def test_existing_run_is_not_overwritten(self):
        runner, _ = self.run_scenario("normal")
        with self.assertRaises(HarnessError) as caught:
            Runner(runner.run_dir)
        self.assertEqual(caught.exception.code, "run_exists")

    def test_invalid_policy_is_recorded_as_failure(self):
        runner = Runner(self.root / "invalid", policy=lambda ticket, articles: {"send": True})
        self.assertEqual(runner.run()["error"], "invalid_decision")
        self.assertEqual(runner.store.data["writes"], 0)

    def test_raising_policy_is_recorded_as_failure(self):
        def broken(ticket, articles):
            raise RuntimeError("untrusted payload")
        runner = Runner(self.root / "broken", policy=broken)
        self.assertEqual(runner.run()["error"], "policy_error")
        self.assertNotIn("untrusted payload", runner.trace.path.read_text())

    def test_malformed_trace_fails_loudly(self):
        path = self.root / "bad.jsonl"
        path.write_text('{"sequence":1,"run_id":"x"}\n{')
        with self.assertRaises(HarnessError) as caught:
            read_trace(path)
        self.assertEqual(caught.exception.code, "invalid_trace")

    def test_resume_does_not_reset_an_exhausted_tool_budget(self):
        path = self.root / "bounded-recovery"
        runner = Runner(path, scenario="crash-after-write", budget=Budget(max_tool_calls=3))
        with self.assertRaises(SimulatedCrash):
            runner.run()
        self.assertEqual(runner.usage.tool_calls, 3)
        resumed = Runner(path, resume=True)
        result = resumed.run()
        self.assertEqual(result["error"], "budget_exhausted")
        self.assertEqual(result["usage"]["tool_calls"], 4)
        self.assertEqual(result["writes"], 1)
        self.assertEqual(result["draft_count"], 1)

    def test_resume_does_not_reset_an_exhausted_step_budget(self):
        path = self.root / "bounded-steps"
        runner = Runner(path, scenario="crash-after-write", budget=Budget(max_steps=4))
        with self.assertRaises(SimulatedCrash):
            runner.run()
        result = Runner(path, resume=True).run()
        self.assertEqual(result["error"], "budget_exhausted")
        self.assertEqual(result["usage"]["steps"], 5)
        self.assertEqual(result["writes"], 1)

    def test_resume_rejects_swapped_store_even_for_the_same_ticket(self):
        first = Runner(self.root / "first")
        second = Runner(self.root / "second")
        first.store.path.write_text(second.store.path.read_text())
        with self.assertRaises(HarnessError) as caught:
            Runner(first.run_dir, resume=True)
        self.assertEqual(caught.exception.code, "store_scope")

    def test_resume_rejects_swapped_trace_without_appending(self):
        first = Runner(self.root / "first")
        second = Runner(self.root / "second")
        wrong_trace = second.trace.path.read_text()
        first.trace.path.write_text(wrong_trace)
        with self.assertRaises(HarnessError) as caught:
            Runner(first.run_dir, resume=True)
        self.assertEqual(caught.exception.code, "trace_scope")
        self.assertEqual(first.trace.path.read_text(), wrong_trace)

    def test_matching_checksum_does_not_replace_checkpoint_shape_validation(self):
        runner = Runner(self.root / "shape")
        original = json.loads(runner.checkpoint_path.read_text())["payload"]
        for broken_state in (None, [], {}, {**original["state"], "articles": [None]},
                             {**original["state"], "faults": {"timeouts_remaining": -1}}):
            with self.subTest(state=broken_state):
                payload = {**original, "state": broken_state}
                runner.checkpoint_path.write_text(json.dumps({
                    "payload": payload, "sha256": digest(payload)}))
                with self.assertRaises(HarnessError) as caught:
                    Runner(runner.run_dir, resume=True)
                self.assertEqual(caught.exception.code, "checkpoint_corrupt")

    def test_malformed_store_has_a_typed_error(self):
        runner = Runner(self.root / "bad-store")
        runner.store.path.write_text("[]")
        with self.assertRaises(HarnessError) as caught:
            Runner(runner.run_dir, resume=True)
        self.assertEqual(caught.exception.code, "store_corrupt")

    def test_unexpected_student_output_fails_without_writing(self):
        for index, bad in enumerate((None, [], "send it", 1, {"action": []})):
            with self.subTest(output=bad):
                runner = Runner(self.root / f"bad-policy-{index}",
                                policy=lambda ticket, articles, value=bad: value)
                self.assertEqual(runner.run()["error"], "invalid_decision")
                self.assertEqual(runner.store.data["writes"], 0)

    def test_student_cannot_accidentally_mutate_authoritative_observations(self):
        from lab.policy import decide
        def modifies_inputs(ticket, articles):
            result = decide(ticket, articles)
            ticket["id"] = "T-999"
            articles.clear()
            return result
        runner = Runner(self.root / "mutating-policy", policy=modifies_inputs)
        result = runner.run()
        self.assertEqual(result["status"], "completed")
        self.assertEqual(runner.state["ticket"]["id"], "T-001")
        self.assertEqual(len(runner.state["articles"]), 1)


class EvaluationTest(unittest.TestCase):
    def test_train_holdout_are_disjoint_and_have_expected_size(self):
        train, holdout = load_cases("train"), load_cases("holdout")
        self.assertEqual(len(train), 18)
        self.assertEqual(len(holdout), 10)
        self.assertFalse({case["id"] for case in train} & {case["id"] for case in holdout})
        self.assertFalse({case["ticket"]["id"] for case in train}
                         & {case["ticket"]["id"] for case in holdout})

    def test_reference_passes_all_behavioral_and_fault_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            report = evaluate(Path(temp) / "eval", "all")
            self.assertTrue(report["passed"])
            self.assertEqual(report["cases_passed"], 28)
            self.assertEqual(report["scenarios_passed"], 11)

    def test_all_escalation_policy_cannot_game_gate(self):
        def always_escalate(ticket, articles):
            return {"action": "escalate", "category": "unknown", "reply": "",
                    "citations": [], "reason": "avoid every request"}
        with tempfile.TemporaryDirectory() as temp:
            report = evaluate(Path(temp) / "eval", "holdout", always_escalate, False)
            self.assertFalse(report["passed"])
            self.assertLess(report["cases_passed"], report["case_count"])
            self.assertGreater(report["failed_checks"]["action"], 0)

    def test_student_regression_returns_nonzero_cli_exit(self):
        from unittest.mock import patch
        def broken_policy(ticket, articles):
            return {"action": "escalate", "category": "unknown", "reply": "",
                    "citations": [], "reason": "regression"}
        with tempfile.TemporaryDirectory() as temp:
            with patch("lab.student.build_decision", broken_policy):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = main(["evaluate", "--policy", "student", "--no-scenarios",
                                 "--out", str(Path(temp) / "eval")])
        self.assertEqual(code, 1)

    def test_reference_solutions_satisfy_public_practice_checks(self):
        path = Path(__file__).parents[1] / "content/labs/solutions/reference.py"
        spec = importlib.util.spec_from_file_location("lab_solutions", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for number in range(1, 9):
            with self.subTest(lab=number):
                report = check_lesson(f"{number:02}", module)
                self.assertTrue(report["passed"], report)


if __name__ == "__main__":
    unittest.main()
