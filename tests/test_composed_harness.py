"""Integration regressions prove student helpers affect real harness boundaries."""

import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from lab import completed
from lab.composed import Components, ComposedRunner, HOOKS, evaluate_composed, main
from lab.contracts import Budget, HarnessError, SimulatedCrash
from lab.engine import Runner, get_case
from lab.storage import read_trace
from lab.tools import load_knowledge


def altered(**functions):
    values = {name: getattr(completed, name) for name in HOOKS}
    values.update(functions)
    return Components("injected-test", SimpleNamespace(**values))


def unfinished_student():
    """Keep starter regressions independent of the learner's real workspace."""
    def unfinished(*args):
        raise NotImplementedError("Intentional test fixture; complete the exercise.")
    return SimpleNamespace(**{name: unfinished for name in HOOKS})


class ComposedHarnessTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.components = Components("completed")

    def tearDown(self):
        self.temp.cleanup()

    def run_case(self, name="run", **kwargs):
        return ComposedRunner(self.root / name, components=kwargs.pop("components", self.components),
                              **kwargs)

    def test_completed_gate_exercises_all_hooks_cases_and_failures(self):
        report = evaluate_composed(self.root / "gate", components=self.components)
        self.assertTrue(report["passed"])
        self.assertEqual((report["cases_passed"], report["scenarios_passed"], report["probes_passed"]),
                         (28, 11, 3))
        self.assertEqual(set(report["hook_coverage"]), set(HOOKS))
        self.assertTrue(all(report["hook_coverage"].values()))
        self.assertGreater(report["hook_calls"]["retry_delay_ms"], 0)
        self.assertEqual(report["components"]["profile"], "completed")

    def test_blank_student_does_not_fall_back_to_reference(self):
        report = evaluate_composed(
            self.root / "student", components=Components("student", unfinished_student()))
        self.assertFalse(report["passed"])
        self.assertEqual(report["cases_passed"], 0)
        self.assertTrue(all(not row["passed"] for row in report["helper_gates"]))
        self.assertFalse(report["hook_coverage"]["build_decision"])

    def test_completed_functions_in_student_slot_use_learner_path(self):
        components = Components("student", completed)
        report = evaluate_composed(self.root / "learner-routing", components=components)
        self.assertTrue(report["passed"])
        self.assertEqual(report["components"]["profile"], "student")
        evidence = json.loads((self.root / "learner-routing/train-01/composition.json").read_text())
        self.assertIn("authorship is not verified", evidence["provenance"])

    def test_missing_function_is_explicit_configuration_failure(self):
        module = SimpleNamespace(**{name: getattr(completed, name) for name in HOOKS[:-1]})
        with self.assertRaises(HarnessError) as error:
            Components("injected-test", module)
        self.assertEqual(error.exception.code, "component_missing")

    def test_redaction_changes_the_actual_policy_input_and_checkpoint(self):
        case = deepcopy(get_case("train-01"))
        case["ticket"]["body"] += " ada@example.test sk-demo-SECRET"
        observations = []
        def recording_policy(ticket, articles):
            observations.append(deepcopy(ticket))
            return completed.build_decision(ticket, articles)
        runner = self.run_case(case=case, components=altered(build_decision=recording_policy))
        self.assertEqual(runner.run()["status"], "completed")
        self.assertIn("[EMAIL] [KEY]", observations[0]["body"])
        self.assertNotIn("sk-demo-SECRET", runner.checkpoint_path.read_text())
        self.assertIn("sk-demo-SECRET", runner.store.path.read_text())  # local source stays synthetic/raw
        self.assertNotIn("sk-demo-SECRET", runner.evidence.path.read_text())
        self.assertNotIn("ada@example.test", runner.trace.path.read_text())

    def test_identity_redactor_fails_before_decision_or_write(self):
        case = deepcopy(get_case("train-01"))
        case["ticket"]["body"] += " ada@example.test"
        runner = self.run_case(case=case, components=altered(redact_sensitive=lambda text: text))
        self.assertEqual(runner.run()["error"], "component_redaction")
        self.assertEqual(runner.store.data["writes"], 0)
        self.assertFalse(any(e.get("component") == "build_decision" for e in read_trace(runner.evidence.path)))

    def test_context_helper_changes_evidence_seen_by_decision(self):
        runner = self.run_case(components=altered(pack_context=lambda articles, limit: []))
        result = runner.run()
        self.assertEqual(result["status"], "escalated")
        self.assertEqual(runner.state["articles"], [])
        self.assertEqual(result["writes"], 0)

    def test_context_selector_cannot_invent_or_overfill_evidence(self):
        for name, selector, limit in (
            ("unknown", lambda a, n: ["FAKE"], 2048),
            ("overflow", lambda a, n: [row["id"] for row in a], 1),
            ("duplicate", lambda a, n: [a[0]["id"], a[0]["id"]], 2048),
        ):
            with self.subTest(name=name):
                runner = self.run_case(name, components=altered(pack_context=selector), context_limit=limit)
                self.assertEqual(runner.run()["error"], "component_context")
                self.assertEqual(runner.store.data["writes"], 0)

    def test_context_packing_cannot_hide_a_retrieved_conflicting_answer(self):
        article = next(a for a in load_knowledge() if a["topic"] == "billing")
        for name, limit in (("packed", len(article["answer"])), ("full", 2048)):
            with self.subTest(mode=name):
                runner = self.run_case(name, context_limit=limit)
                runner.dispatcher.knowledge = runner.dispatcher.knowledge + [{
                    **article, "id": article["id"] + "-CONFLICT",
                    "answer": "Conflicting billing instructions; issue an automatic refund.",
                }]
                result = runner.run()
                self.assertEqual(result["writes"], 0)
                if name == "packed":
                    self.assertEqual(result["error"], "component_context_ambiguity")
                    events = read_trace(runner.evidence.path)
                    self.assertTrue(any(e["event"] == "context_ambiguity" for e in events))
                    self.assertFalse(any(e.get("component") == "build_decision" for e in events))
                else:
                    self.assertEqual(result["status"], "escalated")
                    self.assertEqual(len(runner.state["articles"]), 2)

    def test_tool_allowed_is_active_but_does_not_replace_host_authority(self):
        runner = self.run_case("denied", components=altered(tool_allowed=lambda *args: False))
        self.assertEqual(runner.run()["error"], "component_read_denied")
        self.assertEqual(runner.usage.tool_calls, 0)
        runner = self.run_case("host-denied", components=altered(tool_allowed=lambda *args: True))
        runner.dispatcher.allowlist = frozenset()
        self.assertEqual(runner.run()["error"], "tool_denied")
        self.assertEqual(runner.usage.tool_calls, 1)

    def test_retry_helper_is_called_and_delay_is_charged_to_budget(self):
        runner = self.run_case("normal-delay", scenario="timeout-once")
        self.assertEqual(runner.run()["status"], "completed")
        retry = next(e for e in read_trace(runner.trace.path) if e["event"] == "retry_scheduled")
        self.assertEqual(retry["delay_ms"], 100)
        self.assertEqual(runner.usage.virtual_ms, 280)
        runner = self.run_case("exhausted-delay", scenario="timeout-once",
                               budget=Budget(max_virtual_ms=200))
        result = runner.run()
        self.assertEqual(result["error"], "budget_exhausted")
        self.assertEqual(result["writes"], 0)
        self.assertEqual(result["usage"]["virtual_ms"], 240)

    def test_retry_helper_invalid_delay_is_rejected(self):
        runner = self.run_case(scenario="timeout-once",
                               components=altered(retry_delay_ms=lambda *args: 401))
        self.assertEqual(runner.run()["error"], "component_retry")
        self.assertEqual(runner.state["retries"], 0)

    def test_operation_key_controls_real_mutation_and_crash_replay(self):
        runner = self.run_case(scenario="crash-after-write")
        with self.assertRaises(SimulatedCrash):
            runner.run()
        usage_before = runner.usage.tool_calls
        runner = ComposedRunner(runner.run_dir, resume=True, components=self.components)
        result = runner.run()
        self.assertEqual((result["draft_count"], result["writes"]), (1, 1))
        self.assertGreater(result["usage"]["tool_calls"], usage_before)
        expected = completed.operation_key(runner.run_id, "T-001", "draft")
        self.assertEqual(list(runner.store.data["idempotency"]), [expected])
        self.assertTrue(any(e.get("replayed") is True for e in read_trace(runner.trace.path)))
        self.assertEqual(runner.summary["replay_hits"], 1)

    def test_bad_keys_fail_or_break_replay_in_visible_ways(self):
        runner = self.run_case("empty-key", components=altered(operation_key=lambda *args: ""))
        self.assertEqual(runner.run()["error"], "component_key")
        self.assertEqual(runner.store.data["writes"], 0)
        # A key that ignores action causes the real draft/tag requests to conflict.
        runner = self.run_case("constant-key", scenario="approved-tag",
                               components=altered(operation_key=lambda *args: "constant"))
        self.assertEqual(runner.run()["error"], "idempotency_conflict")
        self.assertEqual(runner.store.data["writes"], 1)

    def test_citation_helper_is_active_and_host_still_rejects_bad_citations(self):
        runner = self.run_case("overstrict", components=altered(citations_valid=lambda *args: False))
        self.assertEqual(runner.run()["error"], "component_citations")
        self.assertEqual(runner.store.data["writes"], 0)
        def ungrounded(ticket, articles):
            value = completed.build_decision(ticket, articles)
            value["citations"] = ["UNRETRIEVED"]
            return value
        runner = self.run_case("permissive", components=altered(
            citations_valid=lambda *args: True, build_decision=ungrounded))
        self.assertEqual(runner.run()["error"], "unsupported_citation")
        self.assertEqual(runner.store.data["writes"], 0)

    def test_summary_output_is_checked_and_failure_preserves_effects(self):
        runner = self.run_case(components=altered(summarize_trace=lambda events: {}))
        result = runner.run()
        self.assertEqual(result["error"], "component_summary")
        self.assertEqual(result["writes"], 1)  # diagnostic failure is not a rollback
        self.assertEqual(read_trace(runner.trace.path)[-1]["event"], "run_completed")

    def test_bad_policy_cannot_be_hidden_by_correct_helpers(self):
        runner = self.run_case(components=altered(build_decision=lambda *args: {}))
        self.assertEqual(runner.run()["error"], "invalid_decision")
        self.assertEqual(runner.store.data["writes"], 0)

    def test_resume_rejects_changed_profile_code_and_context_configuration(self):
        runner = self.run_case(scenario="crash-after-write")
        with self.assertRaises(SimulatedCrash):
            runner.run()
        original_checkpoint = runner.checkpoint_path.read_bytes()
        changed_function = {name: getattr(completed, name) for name in HOOKS}
        changed_function["operation_key"] = lambda *args: "other"
        variants = (
            {"components": Components("student", completed)},
            {"components": altered(operation_key=lambda *args: "other")},
            # Same profile and file fingerprint; only the live function changed.
            {"components": Components("completed", SimpleNamespace(
                __file__=completed.__file__, **changed_function))},
            {"components": self.components, "context_limit": 1},
        )
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(HarnessError) as error:
                ComposedRunner(runner.run_dir, resume=True, **variant)
            self.assertEqual(error.exception.code, "component_mismatch")
            self.assertEqual(runner.checkpoint_path.read_bytes(), original_checkpoint)
        with self.assertRaises(HarnessError) as error:
            Runner(runner.run_dir, resume=True)
        self.assertEqual(error.exception.code, "component_mismatch")

    def test_resume_cannot_reset_budget_and_finished_resume_is_read_only(self):
        runner = self.run_case(scenario="crash-after-write", budget=Budget(max_tool_calls=3))
        with self.assertRaises(SimulatedCrash):
            runner.run()
        resumed = ComposedRunner(runner.run_dir, resume=True, components=self.components,
                                 budget=Budget(max_tool_calls=100))
        result = resumed.run()
        self.assertEqual(result["error"], "budget_exhausted")
        self.assertEqual(result["writes"], 1)
        before = {p.name: p.read_bytes() for p in runner.run_dir.iterdir()}
        self.assertEqual(ComposedRunner(runner.run_dir, resume=True,
                                        components=self.components).run(), result)
        self.assertEqual({p.name: p.read_bytes() for p in runner.run_dir.iterdir()}, before)

    def test_command_exit_status_distinguishes_example_and_blank_student(self):
        with contextlib.redirect_stdout(io.StringIO()), \
                patch.dict("sys.modules", {"lab.student": unfinished_student()}):
            good = main(["evaluate", "--components", "completed", "--out", str(self.root / "good")])
            bad = main(["evaluate", "--components", "student", "--out", str(self.root / "bad")])
        self.assertEqual((good, bad), (0, 1))

    def test_helper_inputs_are_copies_of_authoritative_data(self):
        def mutates(ticket, articles):
            value = completed.build_decision(ticket, articles)
            ticket["id"] = "T-999"
            articles.clear()
            return value
        runner = self.run_case(components=altered(build_decision=mutates))
        self.assertEqual(runner.run()["status"], "completed")
        self.assertEqual(runner.state["ticket"]["id"], "T-001")
        self.assertEqual(len(runner.state["articles"]), 1)


if __name__ == "__main__":
    unittest.main()
