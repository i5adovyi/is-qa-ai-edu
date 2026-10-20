import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from lab.contracts import HarnessError
from lab.engine import get_case
from lab.model_bridge import export_request, load_response, main, replay_response
from lab.policy import classify
from lab.storage import read_trace
from lab.tools import load_knowledge


class ModelBridgeTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def export(self, case="train-01"):
        export_request(case, self.root / "export")
        return self.root / "export" / "mock-response.json"

    def test_export_contains_actual_evidence_but_no_answer_labels(self):
        self.export()
        request = json.loads((self.root / "export/request.json").read_text())
        case = get_case("train-01")
        self.assertEqual(request["ticket"], case["ticket"])
        self.assertEqual(request["articles"], [a for a in load_knowledge()
                                              if a["topic"] == classify(case["ticket"])])
        self.assertEqual(set(request), {
            "schema_version", "case_id", "ticket", "articles", "decision_contract"})
        prompt = (self.root / "export/prompt.md").read_text()
        for label in ("must_include", "must_not_include", '"expected"'):
            self.assertNotIn(label, prompt)
        self.assertIn("not by an AI model", (self.root / "export/README.md").read_text())

    def test_mock_replay_has_one_write_and_discloses_provenance(self):
        response = self.export()
        original = response.read_bytes()
        result, report = replay_response("train-01", response, self.root / "run")
        self.assertTrue(report["passed"])
        self.assertEqual(result["writes"], 1)
        self.assertEqual(response.read_bytes(), original)
        provenance = json.loads((self.root / "run/provenance.json").read_text())
        self.assertFalse(provenance["model_authorship_verified"])
        self.assertEqual(provenance["provider_calls"], 0)
        events = read_trace(self.root / "run/trace.jsonl")
        self.assertTrue(any(e["event"] == "mutation_committed" for e in events))

    def test_malformed_json_and_duplicates_fail_before_run_creation(self):
        response = self.root / "response.json"
        for index, text in enumerate((
            "```json\n{}\n```", "{", '{"action":"draft","action":"escalate"}',
            '{"score":NaN}', "[" * 2000,
        )):
            with self.subTest(text=text[:30]):
                response.write_text(text)
                destination = self.root / f"bad-{index}"
                with self.assertRaises(HarnessError) as caught:
                    replay_response("train-01", response, destination)
                self.assertEqual(caught.exception.code, "invalid_response")
                self.assertFalse(destination.exists())

    def test_extra_fields_and_unknown_citations_are_rejected_by_runner(self):
        baseline = json.loads(self.export().read_text())
        variants = [
            ({**baseline, "execute": "untrusted command text"}, "invalid_decision"),
            ({**baseline, "citations": ["KB-NOT-RETRIEVED"]}, "unsupported_citation"),
            ([], "invalid_decision"),
        ]
        for index, (value, code) in enumerate(variants):
            response = self.root / f"response-{index}.json"
            response.write_text(json.dumps(value))
            destination = self.root / f"run-{index}"
            result, report = replay_response("train-01", response, destination)
            self.assertEqual(result["error"], code)
            self.assertFalse(report["passed"])
            self.assertEqual(result["writes"], 0)
            self.assertFalse(any(e["event"] == "mutation_committed"
                                 for e in read_trace(destination / "trace.jsonl")))

    def test_response_size_is_bounded(self):
        response = self.root / "large.json"
        response.write_text(" " * 65537)
        with self.assertRaises(HarnessError) as caught:
            load_response(response)
        self.assertEqual(caught.exception.code, "invalid_response")

    def test_import_is_read_only_and_does_not_start_cli(self):
        project = str(Path(__file__).resolve().parents[1])
        environment = {**os.environ, "PYTHONPATH": project, "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(
            [sys.executable, "-c", "import lab.model_bridge; print('imported')"],
            cwd=self.root, env=environment, capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout, "imported\n")
        self.assertEqual(result.stderr, "")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_export_and_replay_refuse_to_overwrite(self):
        response = self.export()
        with self.assertRaises(HarnessError):
            export_request("train-01", self.root / "export")
        replay_response("train-01", response, self.root / "run")
        before = (self.root / "run/store.json").read_bytes()
        with self.assertRaises(HarnessError):
            replay_response("train-01", response, self.root / "run")
        self.assertEqual((self.root / "run/store.json").read_bytes(), before)

    def test_model_escalation_of_answerable_case_fails_acceptance(self):
        response = self.root / "response.json"
        response.write_text(json.dumps({
            "action": "escalate", "category": "billing", "reply": "",
            "citations": [], "reason": "Decline every task.",
        }))
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["run", "--response", str(response), "--out", str(self.root / "run")])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads((self.root / "run/store.json").read_text())["writes"], 0)


if __name__ == "__main__":
    unittest.main()
