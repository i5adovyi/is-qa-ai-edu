import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from lab.practicum import retrieval, review_queue as queue, workers


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(retrieval.CORPUS.read_text())

    def test_version_filter_blocks_obsolete_policy(self):
        ids = retrieval.retrieve("export size policy", self.data["records"], "hybrid", "2.4", 10)
        self.assertNotIn("EXPORT-OLD", ids)
        self.assertIn("EXPORT-CURRENT", ids)

    def test_hybrid_can_find_paraphrase_baseline_misses(self):
        base = retrieval.retrieve("huge download", self.data["records"], "lexical", "2.4")
        improved = retrieval.retrieve("huge download", self.data["records"], "hybrid", "2.4")
        self.assertNotIn("EXPORT-CURRENT", base)
        self.assertIn("EXPORT-CURRENT", improved)

    def test_empty_and_unanswerable_separate_from_recall(self):
        report = retrieval.evaluate(self.data, "hybrid")
        rows = {x["id"]: x for x in report["cases"]}
        self.assertIsNone(rows["R07"]["recall_at_k"])
        self.assertFalse(rows["R07"]["no_answer_has_matches"])
        self.assertTrue(rows["R12"]["no_answer_has_matches"])
        self.assertEqual(report["answerable_count"], 10)

    def test_citation_membership_is_not_entailment(self):
        claims = [{"source_id": "EXPORT-CURRENT", "claim_id": "refund-complete"},
                  {"source_id": "EXPORT-CURRENT", "claim_id": "instant-large"},
                  {"source_id": "EXPORT-CURRENT", "claim_id": "limit-100-v24"}]
        labels = retrieval.claim_support(claims, ["EXPORT-CURRENT"], self.data["records"])
        self.assertEqual([x["verdict"] for x in labels], ["not_established", "contradicted", "supported"])

    def test_ties_are_stable_and_duplicate_ids_fail(self):
        records = [{"id": "Z", "version": "all", "title": "x", "text": ""},
                   {"id": "A", "version": "all", "title": "x", "text": ""}]
        self.assertEqual(retrieval.retrieve("x", records), ["A", "Z"])
        with self.assertRaises(ValueError):
            retrieval.retrieve("x", records + [records[0]])

    def test_labels_are_not_retriever_inputs(self):
        before = retrieval.evaluate(self.data, "lexical")["cases"][0]["retrieved"]
        self.data["cases"][0]["required"] = ["IMPOSSIBLE-LABEL"]
        after = retrieval.evaluate(self.data, "lexical")["cases"][0]["retrieved"]
        self.assertEqual(before, after)


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [workers.assignment(role, workers.PACKET) for role in ["evidence", "completeness"]]
        self.good = [{"task_id": t["task_id"], "input_hash": t["input_hash"],
                      "status": "complete", "result": workers.scripted(t)} for t in self.tasks]

    def test_integration_faults(self):
        checks = workers.fault_checks(self.tasks, self.good)
        self.assertEqual(len(checks), 8)
        self.assertTrue(all(checks.values()), checks)

    def test_fault_mutants_change_both_size_outcomes(self):
        for packet in workers.packets():
            tasks = [workers.assignment(role, packet) for role in ["evidence", "completeness"]]
            good = [{"task_id": t["task_id"], "input_hash": t["input_hash"],
                     "status": "complete", "result": workers.scripted(t)} for t in tasks]
            self.assertTrue(all(workers.fault_checks(tasks, good).values()))

    def test_policy_change_invalidates_only_dependent_worker(self):
        changed = copy.deepcopy(workers.PACKET)
        changed["version"] = "policy-v3"
        changed["sources"][0]["limit_mb"] = 75
        self.assertNotEqual(workers.assignment("evidence", changed)["input_hash"], self.tasks[0]["input_hash"])
        self.assertEqual(workers.assignment("completeness", changed)["input_hash"], self.tasks[1]["input_hash"])

    def test_mismatching_claims_block_integration(self):
        extra = copy.deepcopy(self.good)
        extra[0]["result"]["claims"] += ["size_above_documented_limit"]
        with self.assertRaises(ValueError):
            workers.integrate(extra, self.tasks)

    def test_out_of_scope_worker_fails(self):
        self.good[1]["result"]["claims"] = ["size_within_documented_limit"]
        with self.assertRaises(ValueError):
            workers.integrate(self.good, self.tasks)

    def test_unordered_lists_do_not_create_false_worker_conflicts(self):
        duplicate = copy.deepcopy(self.good[1])
        duplicate["result"]["missing_facts"].reverse()
        self.assertEqual(workers.integrate(self.good + [duplicate], self.tasks),
                         workers.integrate(self.good, self.tasks))
        reversed_single = workers.scripted(workers.assignment("single", workers.PACKET))
        reversed_single["missing_facts"].reverse()
        self.assertEqual(workers.canonical_result(reversed_single),
                         workers.canonical_result(workers.scripted(workers.assignment("single", workers.PACKET))))

    def test_duplicate_response_fields_are_not_silently_accepted(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            workers.strict_result_json('{"claims":[],"claims":["size_above_documented_limit"]}')

    def test_actual_subprocess_writes_separate_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = workers.worker_process(self.tasks[0], Path(tmp) / "worker", "scripted", timeout=5)
            self.assertEqual(result["result"], self.good[0]["result"])
            self.assertTrue((Path(tmp) / "worker/result.json").is_file())
            with self.assertRaises(FileExistsError):
                workers.worker_process(self.tasks[0], Path(tmp) / "worker", "scripted")

    def test_worker_failure_preserves_assignment_without_success_envelope(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "worker"
            with patch.object(workers.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "")):
                with self.assertRaisesRegex(ValueError, "worker process failed"):
                    workers.worker_process(self.tasks[0], folder, "scripted")
            self.assertTrue((folder / "assignment.json").exists())
            self.assertFalse((folder / "result.json").exists())

    def test_timeout_records_incomplete_experiment(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "experiment"
            with patch.object(workers, "run_case", side_effect=subprocess.TimeoutExpired("synthetic", 1)):
                with self.assertRaises(subprocess.TimeoutExpired):
                    workers.main(["--out", str(folder), "--cases", "1"])
            result = json.loads((folder / "interruption.json").read_text())
            self.assertFalse(result["complete"])
            self.assertFalse((folder / "report.json").exists())

    def test_live_worker_rejects_actual_host_tool_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "worker"
            def fake_run(command, **kwargs):
                response = Path(command[command.index("--output-last-message") + 1])
                response.write_text(json.dumps(workers.scripted(self.tasks[0])))
                return subprocess.CompletedProcess(command, 0, json.dumps({
                    "type": "item.completed", "item": {"type": "command_execution"}}), "")
            with patch.object(workers.shutil, "which", return_value="/synthetic/codex"), \
                 patch.object(workers.subprocess, "run", side_effect=fake_run):
                with self.assertRaisesRegex(ValueError, "unexpectedly used"):
                    workers.worker_process(self.tasks[0], folder, "codex", model="explicit-model")
            self.assertTrue((folder / "host-events.json").exists())
            self.assertFalse((folder / "result.json").exists())

    def test_comparison_accepts_correct_results_in_different_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            def fake_worker(task, *args, **kwargs):
                result = workers.scripted(task)
                result["missing_facts"].reverse()
                return {"task_id": task["task_id"], "input_hash": task["input_hash"],
                        "status": "complete", "result": result, "elapsed_seconds": 0.01}
            with patch.object(workers, "worker_process", side_effect=fake_worker):
                report = workers.run_case(Path(tmp) / "case", workers.PACKET, "scripted", None, None, 1)
            self.assertTrue(report["baseline_correct"])
            self.assertTrue(report["team_correct"])
            self.assertTrue(report["passed"])


class ReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name) / "queue"
        self.initial = queue.init(self.folder)
        self.rev = self.initial["item"]["revision"]

    def tearDown(self):
        self.temp.cleanup()

    def test_cannot_apply_without_specific_approval(self):
        with self.assertRaises(ValueError):
            queue.apply(self.folder, self.rev)
        self.assertEqual(queue.read(self.folder)["effects"], [])

    def test_stale_approval_after_revision(self):
        queue.review(self.folder, self.rev, "approved", "learner")
        revised = queue.revise(self.folder, "Please share your browser.")
        with self.assertRaises(ValueError):
            queue.apply(self.folder, self.rev)
        with self.assertRaises(ValueError):
            queue.apply(self.folder, revised["item"]["revision"])
        self.assertEqual(queue.read(self.folder)["effects"], [])

    def test_rejection_and_correction_paths(self):
        for verdict in ["rejected", "changes_requested"]:
            queue.review(self.folder, self.rev, verdict, "learner")
            with self.assertRaises(ValueError):
                queue.apply(self.folder, self.rev)
        self.assertEqual(len(queue.read(self.folder)["history"]), 3)

    def test_effect_replay_is_one_effect_after_new_process(self):
        queue.review(self.folder, self.rev, "approved", "learner")
        cmd = [sys.executable, "-m", "lab.practicum.review_queue", "apply",
               "--out", str(self.folder), "--revision", self.rev]
        for _ in range(2):
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(queue.read(self.folder)["effects"]), 1)

    def test_release_mismatch_leaves_state_unchanged(self):
        with self.assertRaises(ValueError):
            queue.release(self.folder, "v2", "v2", "v1")
        self.assertEqual(queue.read(self.folder), self.initial)

    def test_rollback_preserves_pending_work_and_revokes_approval(self):
        queue.review(self.folder, self.rev, "approved", "learner")
        queue.release(self.folder, "v2", "v2", "v2")
        data = queue.rollback(self.folder, "v1")
        self.assertEqual(data["item"]["body"], self.initial["item"]["body"])
        self.assertEqual(data["item"]["status"], "pending")
        with self.assertRaises(ValueError):
            queue.apply(self.folder, self.rev)

    def test_direct_reactivation_does_not_revive_approval(self):
        queue.review(self.folder, self.rev, "approved", "learner")
        queue.release(self.folder, "v2", "v2", "v2")
        queue.release(self.folder, "v1", "v1", "v1")
        with self.assertRaises(ValueError):
            queue.apply(self.folder, self.rev)

    def test_modified_file_is_detected(self):
        data = queue.read(self.folder)
        data["item"]["body"] = "tampered"
        queue.save(self.folder, data)
        with self.assertRaisesRegex(ValueError, "integrity"):
            queue.read(self.folder)

    def test_rehearsal_runs_all_gates(self):
        result = queue.rehearse(Path(self.temp.name) / "rehearsal")
        self.assertTrue(result["passed"])

    def test_failed_rehearsal_is_a_failed_cli_gate(self):
        with patch.object(queue, "rehearse", return_value={"passed": False, "checks": {}}), \
             patch("builtins.print"):
            self.assertEqual(queue.main(["rehearse", "--out", str(self.folder)]), 1)


if __name__ == "__main__":
    unittest.main()
