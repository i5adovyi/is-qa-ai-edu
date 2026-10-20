"""Executable public acceptance criteria for eight student extensions."""

import importlib

from .contracts import HarnessError
from .engine import get_case
from .policy import validate_decision
from .tools import load_knowledge


def load_student():
    """Load learner code only when requested, leaving the reference usable."""
    try:
        return importlib.import_module("lab.student")
    except (ImportError, SyntaxError) as exc:
        raise HarnessError(
            "student_import",
            f"Cannot load lab/student.py: {exc}. Fix its syntax or imports, then retry."
        ) from exc


def check_lesson(number, module=None):
    if module is None:
        module = load_student()
    checks = []

    def check(name, predicate):
        try:
            passed = bool(predicate())
            detail = "" if passed else "Returned an unexpected value."
        except Exception as exc:
            passed, detail = False, f"{type(exc).__name__}: {exc}"
        checks.append({"name": name, "passed": passed, "detail": detail})

    def rejects(fn, *args):
        try:
            fn(*args)
        except ValueError:
            return True
        return False

    if number == "01":
        f = module.redact_sensitive
        check("email_and_key", lambda: f("Email me at ada@example.test; key sk-demo-abc123.")
              == "Email me at [EMAIL]; key [KEY].")
        check("preserve_context", lambda: f("Error 503 at 12:00, ticket T-001.") ==
              "Error 503 at 12:00, ticket T-001.")
        check("multiple_values", lambda: f("a+b@work.test c@team.test sk-demo-XYZ_9")
              == "[EMAIL] [EMAIL] [KEY]")
        check("idempotent", lambda: f(f("a@b.test sk-demo-A")) == "[EMAIL] [KEY]")
    elif number == "02":
        f = module.pack_context
        articles = [{"id": "B", "text": "12345", "relevance": 0.7},
                    {"id": "A", "text": "12345678", "relevance": 0.9},
                    {"id": "C", "text": "12", "relevance": 0.7}]
        check("rank_then_fit", lambda: f(articles, 10) == ["A", "C"])
        check("skip_oversized", lambda: f(articles, 5) == ["B"])
        check("zero_budget", lambda: f(articles, 0) == [])
        check("duplicate_ids", lambda: f(articles + [articles[0]], 20) == ["A", "B", "C"])
        check("negative_budget", lambda: rejects(f, articles, -1))
        tied = [{"id": "C", "text": "123", "relevance": 1},
                {"id": "B", "text": "123", "relevance": 1}]
        check("tie_order_independent", lambda: f(tied, 3) == f(list(reversed(tied)), 3) == ["B"])
        check("first_duplicate_is_canonical", lambda: f([
            {"id": "A", "text": "too large", "relevance": 1},
            {"id": "A", "text": "x", "relevance": 0},
        ], 1) == [])
    elif number == "03":
        f = module.tool_allowed
        check("valid_read", lambda: f("read_ticket", {"ticket_id": "T-001"},
                                     {"read_ticket"}, "T-001") is True)
        check("scope_denied", lambda: f("read_ticket", {"ticket_id": "T-002"},
                                       {"read_ticket"}, "T-001") is False)
        check("unknown_tool", lambda: f("run_shell", {"ticket_id": "T-001"},
                                       {"run_shell"}, "T-001") is False)
        check("extra_arguments", lambda: f("read_ticket", {"ticket_id": "T-001", "admin": True},
                                          {"read_ticket"}, "T-001") is False)
        check("bad_type", lambda: f("read_ticket", [], {"read_ticket"}, "T-001") is False)
        check("allowlist_denied", lambda: f("read_ticket", {"ticket_id": "T-001"}, set(), "T-001")
              is False)
    elif number == "04":
        f = module.retry_delay_ms
        check("exponential", lambda: [f(i, 100, 1000) for i in range(5)] ==
              [100, 200, 400, 800, 1000])
        check("zero_base", lambda: f(3, 0, 100) == 0)
        check("bounded_huge_attempt", lambda: f(100000, 10, 1000) == 1000)
        check("negative_rejected", lambda: rejects(f, -1, 10, 100))
        check("boolean_rejected", lambda: rejects(f, True, 10, 100))
        check("zero_cap", lambda: f(3, 100, 0) == 0)
        check("all_inputs_validated", lambda: all(
            rejects(f, *values) for values in (
                (1.5, 10, 100), (1, -10, 100), (1, 10, -100),
                (1, True, 100), (1, 10, False), (1, 1.5, 100), (1, 10, 100.5))))
    elif number == "05":
        f = module.operation_key
        check("stable", lambda: f("run1", "T-001", "draft") == f("run1", "T-001", "draft"))
        check("action_specific", lambda: f("r", "T-001", "draft") != f("r", "T-001", "tag"))
        check("run_specific", lambda: f("r1", "T-001", "draft") != f("r2", "T-001", "draft"))
        check("ticket_specific", lambda: f("r", "T-001", "draft") != f("r", "T-002", "draft"))
        check("delimiter_collision", lambda: f("a:b", "c", "d") != f("a", "b:c", "d"))
        check("bounded", lambda: isinstance(f("x" * 300, "T-001", "draft"), str)
              and 0 < len(f("x" * 300, "T-001", "draft")) <= 160)
    elif number == "06":
        f = module.citations_valid
        check("valid", lambda: f(["KB-A"], ["KB-A", "KB-B"]) is True)
        check("hallucinated", lambda: f(["KB-Z"], ["KB-A"]) is False)
        check("empty", lambda: f([], ["KB-A"]) is False)
        check("duplicates", lambda: f(["KB-A", "KB-A"], ["KB-A"]) is False)
        check("wrong_type", lambda: f("KB-A", ["KB-A"]) is False)
        check("nested_values", lambda: f([["KB-A"]], ["KB-A"]) is False)
        check("multiple_valid", lambda: f(["KB-A", "KB-B"], ["KB-A", "KB-B"]) is True)
        check("empty_id", lambda: f([""], [""]) is False)
    elif number == "07":
        f = module.summarize_trace
        events = [{"event": "run_started"}, {"event": "tool_attempt"},
                  {"event": "tool_rejected", "code": "tool_timeout"},
                  {"event": "retry_scheduled"}, {"event": "tool_attempt"},
                  {"event": "tool_result", "replayed": True},
                  {"event": "run_completed"}]
        check("counts", lambda: f(events) == {
            "tool_attempts": 2, "rejections": 1, "retries": 1, "replay_hits": 1})
        check("empty", lambda: f([]) == {
            "tool_attempts": 0, "rejections": 0, "retries": 0, "replay_hits": 0})
        check("strict_replay_boolean", lambda: f([{"event": "tool_result", "replayed": "false"}])
              ["replay_hits"] == 0)
        check("replay_requires_result_event", lambda: f([
            {"event": "mutation_committed", "replayed": True}])["replay_hits"] == 0)
    elif number == "08":
        f = module.build_decision
        article = load_knowledge()[0]
        ticket = get_case("train-01")["ticket"]

        def valid_grounded():
            value = f(ticket, [article])
            validate_decision(value, [article])
            return value["action"] == "draft" and value["reply"] == article["answer"]

        check("grounded_draft", valid_grounded)
        def valid_escalation(subject, evidence):
            value = f(subject, evidence)
            validate_decision(value, evidence)
            return value["action"] == "escalate"

        check("missing_evidence", lambda: valid_escalation(ticket, []))
        check("wrong_evidence", lambda: valid_escalation(ticket, [load_knowledge()[1]]))
        check("instruction_attack", lambda: valid_escalation(
            get_case("train-13")["ticket"], [article]))
        check("ambiguous_request", lambda: valid_escalation(
            get_case("train-11")["ticket"], [article]))
        conflict = {**article, "id": article["id"] + "-CONFLICT",
                    "answer": "This deliberately conflicts with the approved answer."}
        check("conflicting_evidence", lambda: valid_escalation(ticket, [article, conflict]))

        def filter_irrelevant():
            evidence = [load_knowledge()[1], article]
            value = f(ticket, evidence)
            validate_decision(value, evidence)
            return value["action"] == "draft" and value["reply"] == article["answer"]

        check("filter_irrelevant_evidence", filter_irrelevant)
    else:
        raise ValueError("Lesson must be 01 through 08.")
    return {"lab": number, "passed": all(item["passed"] for item in checks), "checks": checks}
