"""Optional integration tests. Core Python suite skips without the pinned SDK."""
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import shutil

try:
    HAS_SDK = importlib.metadata.version("mcp") == "1.30.0"
except importlib.metadata.PackageNotFoundError:
    HAS_SDK = False


@unittest.skipUnless(HAS_SDK, "Optional: install lab/mcp_lab/requirements.lock.txt in Python 3.12 venv")
class MCPIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "real"
        began = time.monotonic()
        result = subprocess.run(
            [sys.executable, "-m", "lab.mcp_lab", "--out", str(cls.output)],
            capture_output=True, text=True, timeout=25,
        )
        cls.elapsed = time.monotonic() - began
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.report = json.loads((cls.output / "report.json").read_text())
        cls.checks = {c["name"]: c for c in cls.report["checks"]}
        cls.messages = [json.loads(line) for line in (cls.output / "messages.jsonl").read_text().splitlines()]

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_real_lifecycle_and_request_correlation(self):
        normal = [e["message"] for e in self.messages if e["connection"] == "normal"]
        methods = [m["method"] for m in normal if "method" in m]
        self.assertEqual(methods[:3], ["initialize", "notifications/initialized", "tools/list"])
        self.assertTrue(self.checks["request_id_correlation"]["passed"])
        self.assertTrue(self.checks["initialize_capabilities"]["evidence"]["protocolVersion"])

    def test_discovery_and_structured_output(self):
        tool = self.checks["discovery_schemas"]["evidence"]["tools"][0]
        self.assertFalse(tool["inputSchema"]["additionalProperties"])
        self.assertIn("record", tool["outputSchema"]["properties"])
        result = self.checks["valid_lookup"]["evidence"]
        self.assertEqual(result["structuredContent"]["record"]["product_version"], "2.4")
        self.assertFalse(result["isError"])

    def test_server_rejects_bad_calls_and_unknown_record(self):
        for name in ("malformed_arguments", "extra_argument_denied", "unknown_tool", "unknown_record"):
            with self.subTest(name=name):
                self.assertTrue(self.checks[name]["passed"])
                self.assertTrue(self.checks[name]["evidence"]["isError"])

    def test_injected_text_cannot_create_tool_authority(self):
        evidence = self.checks["untrusted_evidence_no_authority"]["evidence"]
        self.assertIn("delete_account", evidence["result"]["structuredContent"]["record"]["excerpt"])
        self.assertEqual(evidence["result"]["structuredContent"]["trust"], "untrusted_evidence")
        self.assertTrue(self.checks["untrusted_evidence_no_authority"]["passed"])
        self.assertTrue(self.checks["unknown_tool"]["passed"])

    def test_disconnect_and_timeout_are_bounded_without_retry(self):
        for fault in ("timeout", "disconnect"):
            check = self.checks["bounded_" + fault]
            self.assertTrue(check["passed"])
            self.assertEqual(check["evidence"]["retry_count"], 0)
            calls = [e for e in self.messages if e["connection"] == fault
                     and e.get("message", {}).get("method") == "tools/call"]
            self.assertEqual(len(calls), 1)
        self.assertLess(self.elapsed, 20, "Subprocess cleanup or deadline enforcement hung")

    def test_stdout_corruption_is_detected_and_stderr_separate(self):
        self.assertTrue(self.checks["stderr_separated"]["passed"])
        self.assertTrue(self.checks["stdout_noise_detected"]["passed"])
        self.assertIn("Failed to parse JSONRPC", (self.output / "client.stderr.txt").read_text())
        self.assertIn("server ready", (self.output / "normal.stderr.txt").read_text())

    def test_importing_server_starts_no_protocol_or_side_effect(self):
        completed = subprocess.run(
            [sys.executable, "-c", "import lab.mcp_lab.server; print('import-only')"],
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "import-only\n")
        self.assertEqual(completed.stderr, "")

    def test_evidence_directory_is_not_overwritten(self):
        completed = subprocess.run(
            [sys.executable, "-m", "lab.mcp_lab", "--out", str(self.output)],
            capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("must be empty", completed.stderr)
        self.assertEqual(json.loads((self.output / "report.json").read_text()), self.report)

    def run_broken_copy(self, label, transform):
        path = Path(self.temp.name) / label
        path.mkdir()
        original = Path("lab/mcp_lab/server.py").read_text()
        (path / "server.py").write_text(transform(original))
        shutil.copyfile("lab/mcp_lab/corpus.json", path / "corpus.json")
        out = path / "evidence"
        completed = subprocess.run(
            [sys.executable, "-m", "lab.mcp_lab", "--server-file", str(path / "server.py"), "--out", str(out)],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertTrue((out / "messages.jsonl").read_text())
        return json.loads((out / "report.json").read_text())

    def test_learner_text_only_success_is_failed_without_losing_evidence(self):
        def break_output(source):
            return source.replace("outputSchema=OUTPUT_SCHEMA,", "outputSchema=None,").replace(
                'return {"record": dict(record), "trust": "untrusted_evidence"}',
                'return types.CallToolResult(content=[types.TextContent(type="text", text="no structure")])',
            )
        report = self.run_broken_copy("text-only", break_output)
        self.assertFalse(report["aborted"])
        checks = {c["name"]: c for c in report["checks"]}
        self.assertFalse(checks["valid_lookup"]["passed"])
        self.assertFalse(checks["discovery_schemas"]["passed"])

    def test_sdk_output_schema_exception_preserves_partial_evidence(self):
        report = self.run_broken_copy(
            "invalid-output",
            lambda source: source.replace(
                'return {"record": dict(record), "trust": "untrusted_evidence"}',
                'return types.CallToolResult(content=[], structuredContent={"wrong": True})',
            ),
        )
        self.assertTrue(report["aborted"])
        self.assertEqual(report["checks"][-1]["name"], "integration_aborted")
        self.assertFalse(report["checks"][-1]["passed"])
        self.assertIn("Invalid structured content", str(report["checks"][-1]["evidence"]))


if __name__ == "__main__":
    unittest.main()
