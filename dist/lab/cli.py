"""Run with python3 -m lab.cli. Standard library only."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import uuid

from .contracts import HarnessError, SimulatedCrash
from .engine import Runner, SCENARIOS, get_case
from .evaluation import evaluate
from .practice import check_lesson
from .storage import read_trace


def fresh_path(prefix):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path(".lab-runs") / f"{prefix}-{stamp}-{uuid.uuid4().hex[:6]}"


def show_result(result, directory):
    decision = result.get("decision") or {}
    print(f"Status: {result['status']} | action: {decision.get('action', 'none')}"
          f" | category: {decision.get('category', 'none')}")
    if result["error"]:
        print(f"Error: {result['error']}")
    print(f"Drafts: {result['draft_count']} | durable writes: {result['writes']}"
          f" | tool attempts: {result['usage']['tool_calls']}")
    if decision.get("reply"):
        print(f"Local draft: {decision['reply']}")
    print(f"Run artifacts: {Path(directory).resolve()}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Signal Desk offline agent-engineering lab")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Run a reference scenario")
    demo.add_argument("--scenario", choices=SCENARIOS, default="normal")
    demo.add_argument("--case", default="train-01")
    demo.add_argument("--out", type=Path)
    resume = commands.add_parser("resume", help="Resume an existing checkpoint")
    resume.add_argument("checkpoint", type=Path)
    evaluation = commands.add_parser("evaluate", help="Run behavioral and resilience acceptance gates")
    evaluation.add_argument("--split", choices=["train", "holdout", "all"], default="holdout")
    evaluation.add_argument("--policy", choices=["reference", "student"], default="reference")
    evaluation.add_argument("--out", type=Path)
    evaluation.add_argument("--no-scenarios", action="store_true")
    trace = commands.add_parser("trace", help="Inspect an event log without exposing ticket text")
    trace.add_argument("path", type=Path)
    trace.add_argument("--json", action="store_true")
    practice = commands.add_parser("practice", help="Check your isolated student.py extension")
    practice.add_argument("--lab", choices=[f"{i:02}" for i in range(1, 9)], required=True)
    commands.add_parser("schemas", help="Print the tool contracts")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            directory = args.out or fresh_path(args.scenario)
            runner = Runner(directory, get_case(args.case), args.scenario)
            try:
                result = runner.run()
            except SimulatedCrash:
                print(f"Simulated crash after committed write. Resume:\n"
                      f"python3 -m lab.cli resume '{directory / 'checkpoint.json'}'")
                return 3
            show_result(result, directory)
            return 0 if result["status"] != "failed" else 1
        if args.command == "resume":
            if args.checkpoint.name != "checkpoint.json":
                raise HarnessError("checkpoint_path", "Provide the run's checkpoint.json file.")
            runner = Runner(args.checkpoint.parent, resume=True)
            result = runner.run()
            show_result(result, args.checkpoint.parent)
            return 0 if result["status"] != "failed" else 1
        if args.command == "evaluate":
            policy = None
            if args.policy == "student":
                from .student import build_decision
                policy = build_decision
            directory = args.out or fresh_path("eval-" + args.split)
            report = evaluate(directory, args.split, policy, not args.no_scenarios)
            print(f"Cases: {report['cases_passed']}/{report['case_count']} | "
                  f"scenarios: {report['scenarios_passed']}/{report['scenario_count']}")
            print(f"Acceptance gate: {'PASS' if report['passed'] else 'FAIL'}")
            if report["failed_checks"]:
                print("Failed checks: " + json.dumps(report["failed_checks"], sort_keys=True))
            print(f"Report: {(directory / 'report.json').resolve()}")
            return 0 if report["passed"] else 1
        if args.command == "trace":
            events = read_trace(args.path)
            if args.json:
                print(json.dumps(events, indent=2))
            else:
                for item in events:
                    details = " ".join(f"{key}={item[key]}" for key in
                                       ("phase", "tool", "code", "action", "replayed", "status")
                                       if key in item)
                    print(f"{item['sequence']:03} {item['event']:<19} {details}")
                print("Event counts: " + json.dumps(dict(Counter(
                    event["event"] for event in events)), sort_keys=True))
            return 0
        if args.command == "practice":
            report = check_lesson(args.lab)
            for item in report["checks"]:
                print(f"{'PASS' if item['passed'] else 'FAIL'} {item['name']} {item['detail']}")
            return 0 if report["passed"] else 1
        if args.command == "schemas":
            from .contracts import TOOL_SCHEMAS
            print(json.dumps(TOOL_SCHEMAS, indent=2))
            return 0
    except HarnessError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError, NotImplementedError) as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
