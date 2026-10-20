"""Explicit, evidence-producing composition of all eight learner functions.

Python extensions are trusted local code, not sandboxed plugins. The completed
profile is an instructor example, while student loads the learner's own TODOs.
"""

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib
import json
import marshal
from pathlib import Path
import re
import uuid

from .contracts import Budget, HarnessError, SimulatedCrash
from .engine import Runner, get_case, load_cases
from .evaluation import assess, SCENARIO_EXPECTATIONS
from .policy import classify, validate_decision
from .practice import check_lesson
from .storage import Trace, atomic_json, digest, read_trace
from .tools import load_knowledge


HOOKS = (
    "redact_sensitive", "pack_context", "tool_allowed", "retry_delay_ms",
    "operation_key", "citations_valid", "summarize_trace", "build_decision",
)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
DEMO_KEY = re.compile(r"\bsk-demo-[A-Za-z0-9_-]+")


def trace_counts(events):
    """Independent acceptance oracle; never substituted for the student output."""
    return {
        "tool_attempts": sum(e.get("event") == "tool_attempt" for e in events),
        "rejections": sum(e.get("event") == "tool_rejected" for e in events),
        "retries": sum(e.get("event") == "retry_scheduled" for e in events),
        "replay_hits": sum(e.get("event") == "tool_result" and e.get("replayed") is True
                           for e in events),
    }


class Components:
    def __init__(self, profile="student", module=None):
        if profile not in {"student", "completed", "injected-test"}:
            raise ValueError("Components must be student or completed.")
        self.profile = profile
        self.module = module or importlib.import_module("lab." + profile)
        self.functions = {}
        hashes = {}
        for name in HOOKS:
            fn = getattr(self.module, name, None)
            if not callable(fn) or not hasattr(fn, "__code__"):
                raise HarnessError("component_missing", f"Missing Python function: {name}.")
            self.functions[name] = fn
            hashes[name] = hashlib.sha256(marshal.dumps(fn.__code__)).hexdigest()
        path = getattr(self.module, "__file__", None)
        source_hash = hashlib.sha256(Path(path).read_bytes()).hexdigest() if path else None
        self.identity = {"profile": profile, "source_sha256": source_hash,
                         "function_sha256": hashes}
        self.identity["fingerprint"] = digest(self.identity)

    def invoke(self, evidence, name, *args):
        # Inputs are copied so a helper cannot accidentally change host observations.
        # Hashes expose wiring and equality without recording ticket/secret text.
        evidence.emit("component_called", component=name, input_hash=digest(args))
        try:
            result = self.functions[name](*deepcopy(args))
            result_hash = digest(result)
        except Exception as exc:
            evidence.emit("component_failed", component=name, error_type=type(exc).__name__)
            raise HarnessError("component_error", f"{name} raised {type(exc).__name__}.") from exc
        evidence.emit("component_returned", component=name, output_hash=result_hash)
        return result


class ComposedRunner(Runner):
    def __init__(self, run_dir, case=None, scenario="normal", resume=False,
                 components=None, context_limit=2048, budget=None):
        if type(context_limit) is not int or context_limit < 0:
            raise ValueError("Context selection limit must be a nonnegative integer.")
        self.components = components or Components("student")
        self.context_limit = context_limit
        binding = {"kind": "composed-v1", "components": self.components.identity,
                   "selected_context_chars": context_limit}
        super().__init__(run_dir, case=case, scenario=scenario, resume=resume,
                         policy=self._decision, budget=budget, binding=binding)
        self.evidence = Trace(self.run_dir / "components.jsonl", self.run_id)
        self.summary = None

    def call_component(self, name, *args):
        return self.components.invoke(self.evidence, name, *args)

    def _read_ticket(self):
        arguments = {"ticket_id": self.state["ticket_id"]}
        allowed = self.call_component("tool_allowed", "read_ticket", arguments,
                                      ["read_ticket"], self.state["ticket_id"])
        if type(allowed) is not bool or not allowed:
            raise HarnessError("component_read_denied", "Learner read gate denied the request.")
        ticket = super()._read_ticket()  # Mandatory host schema/scope checks still run.
        for field in ("subject", "body"):
            value = self.call_component("redact_sensitive", ticket[field])
            if type(value) is not str or EMAIL.search(value) or DEMO_KEY.search(value):
                raise HarnessError("component_redaction", "Redaction output violates the teaching contract.")
            ticket[field] = value
        return ticket

    def _prepare_articles(self, articles):
        candidates = [{"id": a["id"], "text": a["answer"], "relevance": 1.0}
                      for a in articles]
        ids = self.call_component("pack_context", candidates, self.context_limit)
        known = {a["id"]: a for a in articles}
        if (type(ids) is not list or any(type(i) is not str for i in ids)
                or len(ids) != len(set(ids)) or not set(ids) <= set(known)):
            raise HarnessError("component_context", "Selector returned invalid or unretrieved IDs.")
        selected = [known[i] for i in ids]
        if sum(len(a["answer"]) for a in selected) > self.context_limit:
            raise HarnessError("component_context", "Selected context exceeds its limit.")
        self.evidence.emit("context_selected", count=len(ids), selected_ids=ids,
                           answer_chars=sum(len(a["answer"]) for a in selected),
                           limit_chars=self.context_limit)
        # Packing must not turn known contradictory evidence into false certainty.
        # Compare the relevant answers BEFORE dropping any retrieved candidates.
        topic = classify(self.state["ticket"])
        observed_answers = {a["answer"] for a in articles if a["topic"] == topic}
        selected_answers = {a["answer"] for a in selected if a["topic"] == topic}
        if len(observed_answers) > 1 and not observed_answers <= selected_answers:
            self.evidence.emit("context_ambiguity", retrieved_ids=[a["id"] for a in articles],
                               selected_ids=ids)
            raise HarnessError("component_context_ambiguity",
                               "Context selection would hide competing retrieved answers.")
        return selected

    def _decision(self, ticket, articles):
        return self.call_component("build_decision", ticket, articles)

    def _validate_decision(self, decision):
        if type(decision) is dict and decision.get("action") == "draft":
            valid = self.call_component("citations_valid", decision.get("citations"),
                                        [a["id"] for a in self.state["articles"]])
            if type(valid) is not bool or not valid:
                raise HarnessError("component_citations", "Learner citation check rejected the draft.")
        # Independent host validation remains mandatory even for a permissive helper.
        validate_decision(decision, self.state["articles"])

    def _operation_key(self, action):
        key = self.call_component("operation_key", self.run_id, self.state["ticket_id"], action)
        if type(key) is not str or not key or len(key) > 160:
            raise HarnessError("component_key", "Operation key must be a bounded nonempty string.")
        return key

    def _retry_delay(self, attempt):
        delay = self.call_component("retry_delay_ms", attempt, 100, 400)
        if type(delay) is not int or not 0 <= delay <= 400:
            raise HarnessError("component_retry", "Retry delay must be an integer within its cap.")
        return delay  # Engine charges virtual time; this never sleeps.

    def _complete(self, status, code=None):
        events = read_trace(self.trace.path)
        try:
            self.summary = self.call_component("summarize_trace", events)
            if (type(self.summary) is not dict or self.summary != trace_counts(events)
                    or any(type(n) is not int for n in self.summary.values())):
                raise HarnessError("component_summary", "Trace summary does not match recorded events.")
        except HarnessError as exc:
            status, code = "failed", exc.code
        result = super()._complete(status, code)
        calls = Counter(e["component"] for e in read_trace(self.evidence.path)
                        if e["event"] == "component_called")
        atomic_json(self.run_dir / "composition.json", {
            "schema_version": 1, "binding": self.binding,
            "calls": dict(calls), "summary": self.summary,
            "result_status": result["status"], "result_error": result["error"],
            "provenance": ("Disclosed instructor example; not learner work."
                           if self.components.profile == "completed"
                           else "Locally supplied learner components; authorship is not verified."),
        })
        return result


def evaluate_composed(output_dir, split="all", components=None):
    components = components or Components("student")
    output_dir = Path(output_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise HarnessError("run_exists", "Evaluation requires a fresh output directory.")
    helper_rows = [check_lesson(f"{i:02}", components.module) for i in range(1, 9)]
    rows, scenario_rows, probe_rows, calls = [], [], [], Counter()

    def collect(runner):
        report = json.loads((runner.run_dir / "composition.json").read_text())
        calls.update(report["calls"])

    for case in load_cases(split):
        runner = ComposedRunner(output_dir / case["id"], case=case, components=components)
        result = runner.run()
        checks = assess(case, result, runner.store.data)
        rows.append({"case_id": case["id"], "passed": all(checks.values()), "checks": checks})
        collect(runner)
    for name, expected in SCENARIO_EXPECTATIONS.items():
        path = output_dir / ("scenario-" + name)
        runner = ComposedRunner(path, scenario=name, components=components)
        try:
            result = runner.run()
        except SimulatedCrash:
            runner = ComposedRunner(path, resume=True, components=components)
            result = runner.run()
        actual = (result["status"], result["error"], result["draft_count"], result["writes"])
        events = read_trace(path / "trace.jsonl")
        checks = {"outcome": actual == expected, "terminal_trace": events[-1]["event"] == "run_completed"}
        if name == "crash-after-write":
            checks["replay"] = any(e.get("replayed") is True for e in events)
        if name == "timeout-always":
            checks["one_retry"] = sum(e["event"] == "retry_scheduled" for e in events) == 1
        scenario_rows.append({"scenario": name, "passed": all(checks.values()), "checks": checks})
        collect(runner)
    case = deepcopy(get_case("train-01"))
    case["ticket"]["body"] += " Contact ada@example.test; test key sk-demo-SYNTHETIC_11."
    runner = ComposedRunner(output_dir / "probe-redaction", case=case, components=components)
    result = runner.run()
    ticket = runner.state["ticket"] or {}
    redacted = ticket.get("body", "")
    probe_rows.append({"probe": "redaction_reaches_policy", "passed":
                       result["status"] == "completed" and "[EMAIL]" in redacted
                       and "[KEY]" in redacted and "ada@example.test" not in redacted})
    collect(runner)
    runner = ComposedRunner(output_dir / "probe-context-zero", components=components, context_limit=0)
    result = runner.run()
    probe_rows.append({"probe": "selector_changes_policy_input", "passed":
                       result["status"] == "escalated" and not runner.state["articles"]
                       and result["writes"] == 0})
    collect(runner)
    original = next(a for a in load_knowledge() if a["topic"] == "billing")
    # One answer fits, both do not: a selector alone could hide the disagreement.
    runner = ComposedRunner(output_dir / "probe-hidden-conflict", components=components,
                            context_limit=len(original["answer"]))
    runner.dispatcher.knowledge = runner.dispatcher.knowledge + [{
        **original, "id": original["id"] + "-CONFLICT",
        "answer": "This deliberately conflicts with the approved billing instructions.",
    }]
    result = runner.run()
    probe_rows.append({"probe": "packing_cannot_hide_conflict", "passed":
                       result["status"] == "failed" and result["error"] == "component_context_ambiguity"
                       and result["writes"] == 0})
    collect(runner)
    coverage = {name: calls[name] > 0 for name in HOOKS}
    report = {
        "schema_version": 1, "kind": "complete-composition-gate", "split": split,
        "components": components.identity, "helper_gates": helper_rows,
        "case_count": len(rows), "cases_passed": sum(r["passed"] for r in rows),
        "scenario_count": len(scenario_rows), "scenarios_passed": sum(r["passed"] for r in scenario_rows),
        "probe_count": len(probe_rows), "probes_passed": sum(r["passed"] for r in probe_rows),
        "cases": rows, "scenarios": scenario_rows, "probes": probe_rows,
        "hook_calls": dict(calls), "hook_coverage": coverage,
        "passed": bool(rows) and all(r["passed"] for r in helper_rows + rows + scenario_rows + probe_rows)
                  and all(coverage.values()),
        "limitations": [
            "Completed is disclosed instructor code; a green result is not learner completion.",
            "Student Python runs with local process privileges; this is not an OS sandbox.",
            "Synthetic visible fixtures and deterministic decisions do not measure model quality.",
            "Helper 03 gates only read_ticket; host owns all other tool authorization.",
            "Redaction recognizes only the teaching email/sk-demo formats; raw synthetic store remains local.",
            "Source fingerprints detect accidental component changes, not malicious checkpoint editing.",
        ],
    }
    atomic_json(output_dir / "report.json", report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("run", "evaluate", "resume"):
        p = sub.add_parser(command)
        p.add_argument("--components", choices=("student", "completed"), default="student")
        if command == "resume":
            p.add_argument("checkpoint", type=Path)
        else:
            p.add_argument("--out", type=Path)
        if command == "run":
            p.add_argument("--case", default="train-01")
            p.add_argument("--scenario", choices=tuple(SCENARIO_EXPECTATIONS), default="normal")
        if command in {"run", "resume"}:
            p.add_argument("--context-chars", type=int, default=2048)
        if command == "evaluate":
            p.add_argument("--split", choices=("train", "holdout", "all"), default="all")
    args = parser.parse_args(argv)
    try:
        components = Components(args.components)
        if args.command == "resume":
            runner = ComposedRunner(args.checkpoint.parent, resume=True, components=components,
                                    context_limit=args.context_chars)
        else:
            out = args.out or Path(".lab-runs") / ("composed-" + uuid.uuid4().hex[:10])
            if args.command == "evaluate":
                report = evaluate_composed(out, args.split, components)
                print(json.dumps({"passed": report["passed"], "profile": args.components,
                                  "cases": f"{report['cases_passed']}/{report['case_count']}",
                                  "scenarios": f"{report['scenarios_passed']}/{report['scenario_count']}",
                                  "probes": f"{report['probes_passed']}/{report['probe_count']}",
                                  "hook_coverage": report["hook_coverage"],
                                  "report": str(out / "report.json")}, indent=2))
                return 0 if report["passed"] else 1
            runner = ComposedRunner(out, case=get_case(args.case), scenario=args.scenario,
                                    components=components, context_limit=args.context_chars)
        result = runner.run()
        print(json.dumps({"result": result, "artifacts": str(runner.run_dir)}, indent=2))
        return 1 if result["status"] == "failed" else 0
    except SimulatedCrash as exc:
        print(json.dumps({"error": exc.code, "detail": str(exc)}))
        return 3
    except (HarnessError, ValueError, OSError) as exc:
        print(json.dumps({"error": getattr(exc, "code", "input_error"), "detail": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
