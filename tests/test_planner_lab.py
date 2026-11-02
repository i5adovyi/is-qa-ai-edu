"""Offline failure contracts; optional real SDK tests never make provider calls."""
import asyncio
from copy import deepcopy
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
import urllib.error
from unittest.mock import patch
from tests.link_fixtures import directory_link

from lab.contracts import HarnessError
from lab.planner_lab.__main__ import scenario_actions
from lab.planner_lab.adapters import MCPLookup, ResponsesPlanner, child_output
from lab.planner_lab.runtime import (
    INSTRUCTIONS, CATALOG, ROOT, TASK, Limits, OfflineLookup, ScriptedPlanner,
    bounded, completion, run, strict_json, supported_decision, tool_proposal,
)


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "run"

    def run_loop(self, planner=None, lookup=None, **kwargs):
        return asyncio.run(run(planner or ScriptedPlanner(), lookup or OfflineLookup(), self.out, **kwargs))

    def test_observation_reaches_next_decision_and_local_draft(self):
        planner = ScriptedPlanner()
        report = self.run_loop(planner)
        self.assertEqual(report["status"], "drafted")
        self.assertEqual(planner.requests[0]["observations"], [])
        self.assertEqual(planner.requests[1]["observations"][0]["record"]["id"], "KB-EXPORT-2")
        events = [json.loads(line) for line in (self.out / "trace.jsonl").read_text().splitlines()]
        self.assertEqual([event["kind"] for event in events],
                         ["request", "planner_response", "validated_tool_call", "observation",
                          "request", "planner_response", "validated_completion"])
        self.assertEqual(json.loads((self.out / "draft.json").read_text())["citations"], ["KB-EXPORT-2"])
        self.assertIsNone(report["cost_usd"])

    def test_fault_fixtures(self):
        fixtures = json.loads((ROOT / "lab/planner_lab/fault-fixtures.json").read_text())
        for index, fixture in enumerate(fixtures):
            with self.subTest(fixture=fixture["scenario"]):
                self.out = Path(self.temp.name) / str(index)
                result = self.run_loop(ScriptedPlanner(scenario_actions(fixture["scenario"])))
                for key in ("status", "error", "tool_executions"):
                    self.assertEqual(result[key], fixture["expected_" + key])

    def test_unknown_mutation_never_dispatches(self):
        proposal = tool_proposal()
        proposal["name"] = "delete_account"
        result = self.run_loop(ScriptedPlanner([proposal]))
        self.assertEqual(result["error"], "unknown_tool")
        self.assertEqual(result["tool_executions"], 0)
        self.assertFalse((self.out / "draft.json").exists())

    def test_extra_arguments_rejected(self):
        proposal = tool_proposal()
        proposal["arguments"]["grant"] = "write"
        self.assertEqual(self.run_loop(ScriptedPlanner([proposal]))["error"], "invalid_arguments")

    def test_invalid_evidence_rejected(self):
        class WrongRecord(OfflineLookup):
            async def lookup(self, record_id):
                return await super().lookup("KB-RESET")
        result = self.run_loop(lookup=WrongRecord())
        self.assertEqual(result["error"], "invalid_observation")

    def test_stale_version_rejected(self):
        lookup = OfflineLookup()
        lookup.records["KB-EXPORT-2"]["product_version"] = "2.3"
        self.assertEqual(self.run_loop(lookup=lookup)["error"], "wrong_task_evidence")

    def test_evidence_cannot_expand_tool_authority(self):
        forbidden = tool_proposal()
        forbidden["name"] = "delete_account"
        result = self.run_loop(ScriptedPlanner([tool_proposal("KB-INJECTION"), forbidden]))
        self.assertEqual(result["error"], "unknown_tool")
        self.assertEqual(result["tool_executions"], 1)

    def test_selected_unsupported_claim_rejected(self):
        answer = supported_decision()
        answer["reply"] += " The outage is resolved."
        result = self.run_loop(ScriptedPlanner([tool_proposal(), completion(answer)]))
        self.assertEqual(result["error"], "unsupported_claim")

    def test_schema_success_does_not_prove_semantics(self):
        answer = supported_decision()
        answer["reply"] = "You are guaranteed an unlimited refund."
        result = self.run_loop(ScriptedPlanner([tool_proposal(), completion(answer)]))
        self.assertEqual(result["status"], "drafted")
        self.assertEqual(result["semantic_grounding"], "human_review_required")

    def test_escalation_is_safe_but_does_not_pass_supported_task(self):
        answer = {"action": "escalate", "category": "unknown", "reply": "", "citations": [],
                  "reason": "Insufficient evidence."}
        report = self.run_loop(ScriptedPlanner([completion(answer)]))
        self.assertEqual(report["status"], "escalated")
        self.assertFalse(report["task_acceptance"])
        self.assertFalse((self.out / "draft.json").exists())

    def test_retry_is_bounded_and_accounted(self):
        planner = ScriptedPlanner([HarnessError("rate_limit", "secret"),
                                   HarnessError("rate_limit", "secret")])
        report = self.run_loop(planner)
        self.assertEqual(report["attempts"], 2)
        self.assertEqual(report["error"], "rate_limit")
        self.assertNotIn("secret", (self.out / "trace.jsonl").read_text())

    def test_provider_timeout_can_retry(self):
        planner = ScriptedPlanner([HarnessError("provider_timeout", "synthetic"),
                                   tool_proposal(), completion(supported_decision())])
        self.assertEqual(self.run_loop(planner)["attempts"], 3)

    def test_deadline_cancels_adapter(self):
        class Slow(ScriptedPlanner):
            stopped = False
            async def propose(self, request, timeout):
                try:
                    await asyncio.sleep(5)
                finally:
                    self.stopped = True
        planner = Slow()
        before = time.monotonic()
        result = self.run_loop(planner, limits=Limits(deadline_seconds=0.05))
        self.assertEqual(result["error"], "deadline")
        self.assertTrue(planner.stopped)
        self.assertLess(time.monotonic() - before, 1)

    def test_cancel_during_work(self):
        class Slow(ScriptedPlanner):
            async def propose(self, request, timeout):
                await asyncio.sleep(5)
        start = time.monotonic()
        result = self.run_loop(Slow(), cancelled=lambda: time.monotonic() - start > 0.05)
        self.assertEqual(result["status"], "cancelled")

    def test_precancelled_run_makes_no_request(self):
        result = self.run_loop(cancelled=lambda: True)
        self.assertEqual(result["attempts"], 0)
        self.assertEqual(result["status"], "cancelled")

    def test_limits_and_context(self):
        for index, (limits, expected) in enumerate([
            (Limits(max_attempts=1), "attempt_budget"),
            (Limits(max_decisions=1), "decision_budget"),
            (Limits(max_context_chars=1), "context_budget"),
        ]):
            with self.subTest(error=expected):
                self.out = Path(self.temp.name) / str(index)
                self.assertEqual(self.run_loop(limits=limits)["error"], expected)

    def test_fresh_directory_required(self):
        self.run_loop()
        with self.assertRaises(ValueError):
            self.run_loop()

    def test_strict_parser(self):
        for raw in ['{"a":1,"a":2}', '{"a":NaN}', '```json\n{}\n```', "x" * 65537]:
            with self.subTest(raw=raw[:20]), self.assertRaises(HarnessError):
                strict_json(raw)

    def test_subprocess_stopped_on_deadline(self):
        async def execute():
            return await bounded(child_output([sys.executable, "-c", "import time; time.sleep(20)"], ""),
                                 0.05, lambda: False)
        start = time.monotonic()
        with self.assertRaises(HarnessError) as caught:
            asyncio.run(execute())
        self.assertEqual(caught.exception.code, "deadline")
        self.assertLess(time.monotonic() - start, 3)

    @unittest.skipUnless(importlib.util.find_spec("mcp"), "Optional MCP environment required")
    def test_actual_mcp_lookup_with_planner_loop(self):
        result = self.run_loop(lookup=MCPLookup(self.out))
        self.assertEqual(result["status"], "drafted")
        self.assertEqual(result["lookup_evidence"], "real_mcp_sdk_stdio")
        messages = [json.loads(line)["message"] for line in (self.out / "mcp-messages.jsonl").read_text().splitlines()
                    if "message" in json.loads(line)]
        self.assertTrue(any(item.get("method") == "tools/call" for item in messages))


class ResponsesAdapterTests(unittest.TestCase):
    def request(self):
        return {"instructions": INSTRUCTIONS, "ticket": deepcopy(TASK), "catalog": deepcopy(CATALOG), "observations": []}

    def envelope(self, name="lookup_article", arguments=None):
        return {"id": "synthetic-response", "model": "synthetic-model", "status": "completed",
                "usage": {"input_tokens": 12, "output_tokens": 8},
                "output": [{"type": "function_call", "call_id": "synthetic-call",
                            "name": name, "arguments": json.dumps(arguments or {"record_id": "KB-EXPORT-2"})}]}

    def test_actual_payload_and_correlation_with_fake_transport(self):
        captured = []
        async def transport(payload, timeout):
            captured.append(deepcopy(payload))
            return self.envelope() if len(captured) == 1 else self.envelope("complete", supported_decision())
        async def exercise():
            planner = ResponsesPlanner("explicit-model", transport=transport)
            first = await planner.propose(self.request(), 1)
            self.assertEqual(first["proposal"], tool_proposal())
            request = self.request()
            request["observations"] = [await OfflineLookup().lookup("KB-EXPORT-2")]
            second = await planner.propose(request, 1)
            self.assertEqual(second["proposal"]["kind"], "complete")
        asyncio.run(exercise())
        self.assertEqual(captured[0]["model"], "explicit-model")
        self.assertFalse(captured[0]["store"])
        self.assertFalse(captured[0]["parallel_tool_calls"])
        self.assertEqual(captured[1]["input"][-1]["type"], "function_call_output")
        self.assertEqual(captured[1]["input"][-1]["call_id"], "synthetic-call")
        self.assertTrue(all(tool["strict"] for tool in captured[0]["tools"]))

    def test_refusal_incomplete_invalid_json_multiple_calls(self):
        fixtures = []
        response = self.envelope()
        response["output"] = [{"type": "message", "content": [{"type": "refusal", "refusal": "No."}]}]
        fixtures.append((response, "refusal"))
        response = self.envelope()
        response["status"] = "incomplete"
        fixtures.append((response, "incomplete_response"))
        response = self.envelope()
        response["output"][0]["arguments"] = "{bad"
        fixtures.append((response, "malformed_output"))
        response = self.envelope()
        response["output"] *= 2
        fixtures.append((response, "malformed_output"))
        for response, expected in fixtures:
            with self.subTest(expected=expected):
                async def transport(payload, timeout):
                    return response
                with self.assertRaises(HarnessError) as caught:
                    asyncio.run(ResponsesPlanner("explicit", transport=transport).propose(self.request(), 1))
                self.assertEqual(caught.exception.code, expected)

    def test_missing_key_worker_does_not_need_network(self):
        from lab.planner_lab.http_worker import main
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(main(), {"error": "missing_api_key"})

    def test_http_status_classification_never_exposes_body_or_key(self):
        from lab.planner_lab.http_worker import main
        for status, expected in [(429, "rate_limit"), (408, "provider_timeout"),
                                 (504, "provider_timeout"), (503, "provider_unavailable"),
                                 (401, "provider_http_error")]:
            with self.subTest(status=status):
                error = urllib.error.HTTPError("https://api.openai.com/v1/responses", status,
                                               "synthetic-secret-in-error", {}, None)
                with patch.dict("os.environ", {"OPENAI_API_KEY": "synthetic-key"}, clear=True), \
                     patch("sys.stdin", io.StringIO('{"payload": {}, "timeout": 1}')), \
                     patch("urllib.request.urlopen", side_effect=error):
                    self.assertEqual(main(), {"error": expected})

    def test_host_invocation_retains_venv_path_and_records_actual_call(self):
        from lab.planner_lab.host import exercise
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            directory_link(root / "venv-bin", Path(sys.executable).parent)
            python = root / "venv-bin" / Path(sys.executable).name
            captured = []
            async def transport(command, data):
                captured.extend(command)
                target = Path(command[command.index("--output-last-message") + 1])
                target.write_text(json.dumps(supported_decision()))
                observation = await OfflineLookup().lookup("KB-EXPORT-2")
                return json.dumps({"type": "item.completed", "item": {
                    "type": "mcp_tool_call", "server": "signal_desk", "tool": "lookup_article",
                    "status": "completed", "arguments": {"record_id": "KB-EXPORT-2"},
                    "result": {"structured_content": observation},
                    "error": None,
                }}) + "\n"
            with patch("lab.planner_lab.host.shutil.which", return_value="/synthetic/codex"), \
                 patch("lab.planner_lab.host.child_output", side_effect=transport):
                result = asyncio.run(exercise("explicit-model", python, root / "out"))
            self.assertTrue(result["model_selected_tool_observed"])
            self.assertTrue(result["structural_completion"])
            setting = next(arg for arg in captured if arg.startswith("mcp_servers.signal_desk.command="))
            self.assertEqual(json.loads(setting.split("=", 1)[1]), str(python.absolute()))
            self.assertNotEqual(python.absolute(), python.resolve())
            self.assertIn("--ignore-user-config", captured)


if __name__ == "__main__":
    unittest.main()
