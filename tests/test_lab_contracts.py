import json
from pathlib import Path
from unittest.mock import patch
import tempfile
import unittest

from lab.contracts import Budget, HarnessError, Usage, validate_arguments
from lab.engine import get_case
from lab.policy import decide, validate_decision
from lab.storage import Store, Trace, read_trace
from lab.tools import Dispatcher, load_knowledge


class ContractsTest(unittest.TestCase):
    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(HarnessError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_schema_rejects_extra_fields(self):
        self.assert_code("invalid_arguments", validate_arguments, "read_ticket",
                         {"ticket_id": "T-001", "admin": True})

    def test_schema_rejects_nonobject(self):
        self.assert_code("invalid_arguments", validate_arguments, "read_ticket", [])

    def test_schema_rejects_numeric_ticket(self):
        self.assert_code("invalid_arguments", validate_arguments, "read_ticket", {"ticket_id": 1})

    def test_schema_rejects_unknown_tool(self):
        self.assert_code("unknown_tool", validate_arguments, "run_shell", {})

    def test_schema_rejects_duplicate_citations(self):
        self.assert_code("invalid_arguments", validate_arguments, "save_draft",
                         {"ticket_id": "T-001", "reply": "a", "citations": ["a", "a"]})

    def test_budget_rejects_boolean_and_zero_limits(self):
        for value in (False, 0, -1, 1.2):
            with self.assertRaises(ValueError):
                Budget(max_steps=value)

    def test_budget_boundary_and_failed_attempt_charge(self):
        usage, budget = Usage(), Budget(max_tool_calls=1)
        usage.consume(budget, "tool_calls")
        self.assert_code("budget_exhausted", usage.consume, budget, "tool_calls")
        self.assertEqual(usage.tool_calls, 2)

    def test_negative_consumption_cannot_restore_budget(self):
        with self.assertRaises(ValueError):
            Usage().consume(Budget(), "steps", -1)

    def test_restored_usage_rejects_negative_or_noninteger_values(self):
        for value in (-1, True, 1.5):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Usage(tool_calls=value)

    def test_decision_rejects_hallucinated_citation(self):
        article = load_knowledge()[0]
        decision = decide(get_case("train-01")["ticket"], [article])
        decision["citations"] = ["KB-DOES-NOT-EXIST"]
        self.assert_code("unsupported_citation", validate_decision, decision, [article])

    def test_decision_rejects_unknown_category_type(self):
        decision = decide(get_case("train-01")["ticket"], load_knowledge()[:1])
        decision["category"] = []
        self.assert_code("invalid_decision", validate_decision, decision, load_knowledge())


class DispatcherTest(unittest.TestCase):
    assert_code = ContractsTest.assert_code

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.store = Store(root / "store.json", get_case("train-01")["ticket"])
        self.trace = Trace(root / "trace.jsonl", "test-run")
        self.usage = Usage()
        self.dispatcher = Dispatcher(self.store, self.trace, Budget(), self.usage, "T-001")

    def tearDown(self):
        self.temporary.cleanup()

    def draft_args(self):
        return {"ticket_id": "T-001", "reply": "A local draft", "citations": ["KB-BILL-01"]}

    def test_tool_allowlist_is_external_to_model(self):
        self.assert_code("tool_denied", self.dispatcher.call, "run_shell", {"command": "ls"})
        self.assertEqual(self.store.data["writes"], 0)
        self.assertEqual(self.usage.tool_calls, 1)

    def test_allowlist_can_remove_an_existing_tool(self):
        self.dispatcher.allowlist = frozenset()
        self.assert_code("tool_denied", self.dispatcher.call, "read_ticket", {"ticket_id": "T-001"})

    def test_cross_ticket_read_denied(self):
        self.assert_code("scope_denied", self.dispatcher.call, "read_ticket", {"ticket_id": "T-002"})

    def test_unapproved_tag_denied(self):
        self.assert_code("approval_required", self.dispatcher.call, "add_tag",
                         {"ticket_id": "T-001", "tag": "triaged"}, key="tag-1")
        self.assertEqual(self.store.data["tags"], [])

    def test_approval_does_not_cross_ticket_scope(self):
        self.dispatcher.approvals = frozenset({"tag:T-002"})
        self.assert_code("approval_required", self.dispatcher.call, "add_tag",
                         {"ticket_id": "T-001", "tag": "triaged"}, key="tag-1")

    def test_approved_tag_can_commit(self):
        self.dispatcher.approvals = frozenset({"tag:T-001"})
        result = self.dispatcher.call("add_tag", {"ticket_id": "T-001", "tag": "triaged"}, key="k")
        self.assertTrue(result["saved"])
        self.assertEqual(self.store.data["tags"], ["triaged"])

    def test_citation_must_have_been_retrieved(self):
        self.assert_code("unsupported_citation", self.dispatcher.call,
                         "save_draft", self.draft_args(), key="k")

    def test_mutation_requires_idempotency_key(self):
        self.dispatcher.call("search_kb", {"topic": "billing"})
        self.assert_code("idempotency_required", self.dispatcher.call,
                         "save_draft", self.draft_args())

    def test_replay_does_not_repeat_mutation(self):
        self.dispatcher.call("search_kb", {"topic": "billing"})
        first = self.dispatcher.call("save_draft", self.draft_args(), key="k")
        second = self.dispatcher.call("save_draft", self.draft_args(), key="k")
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(self.store.data["writes"], 1)
        self.assertEqual(len(self.store.data["drafts"]), 1)

    def test_reused_key_with_changed_payload_conflicts(self):
        self.dispatcher.call("search_kb", {"topic": "billing"})
        self.dispatcher.call("save_draft", self.draft_args(), key="k")
        changed = {**self.draft_args(), "reply": "different"}
        self.assert_code("idempotency_conflict", self.dispatcher.call, "save_draft", changed, key="k")
        self.assertEqual(self.store.data["writes"], 1)

    def test_context_budget_blocks_oversized_result(self):
        self.dispatcher.budget = Budget(max_context_chars=1)
        self.assert_code("budget_exhausted", self.dispatcher.call, "read_ticket",
                         {"ticket_id": "T-001"})

    def test_trace_does_not_contain_ticket_body(self):
        self.dispatcher.call("read_ticket", {"ticket_id": "T-001"})
        trace = self.trace.path.read_text()
        self.assertNotIn(self.store.data["ticket"]["body"], trace)
        self.assertIn("request_hash", trace)

    def test_dispatcher_rejects_a_store_from_another_ticket(self):
        self.assert_code("scope_denied", Dispatcher, self.store, self.trace,
                         Budget(), Usage(), "T-002")

    def test_output_budget_failure_records_the_committed_effect(self):
        self.dispatcher.call("search_kb", {"topic": "billing"})
        self.dispatcher.budget.max_context_chars = self.usage.context_chars + 1
        self.assert_code("budget_exhausted", self.dispatcher.call,
                         "save_draft", self.draft_args(), key="budget-save")
        self.assertEqual(self.store.data["writes"], 1)
        events = read_trace(self.trace.path)
        self.assertEqual(events[-2]["event"], "mutation_committed")
        self.assertEqual(events[-1]["event"], "tool_rejected")

    def test_failed_persistence_does_not_create_a_false_replay(self):
        arguments = self.draft_args()
        with patch("lab.storage.atomic_json", side_effect=OSError("simulated disk failure")):
            with self.assertRaises(OSError):
                self.store.mutate("save_draft", arguments, "disk-key")
        self.assertEqual(self.store.data["writes"], 0)
        self.assertEqual(self.store.data["drafts"], [])
        self.assertEqual(self.store.data["idempotency"], {})
        result = self.store.mutate("save_draft", arguments, "disk-key")
        self.assertFalse(result["replayed"])
        self.assertEqual(Store(self.store.path).data["writes"], 1)
