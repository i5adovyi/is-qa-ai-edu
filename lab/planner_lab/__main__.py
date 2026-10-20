"""Run a bounded planner loop; network access happens only with an explicit backend."""
import argparse
import asyncio
import json
from pathlib import Path
import sys

from lab.contracts import HarnessError
from .adapters import CodexPlanner, MCPLookup, ResponsesPlanner
from .runtime import Limits, OfflineLookup, ScriptedPlanner, completion, run, supported_decision, tool_proposal


def scenario_actions(name):
    if name == "repeated":
        return [tool_proposal(), tool_proposal()]
    if name == "premature":
        return [completion(supported_decision())]
    if name == "malformed":
        return ["{not valid json"]
    if name == "refusal":
        return [HarnessError("refusal", "Synthetic refusal.")]
    if name == "rate-limit":
        return [HarnessError("rate_limit", "Synthetic rate limit."), tool_proposal(), completion(supported_decision())]
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("scripted", "student", "responses", "codex"), default="scripted")
    parser.add_argument("--lookup", choices=("fixture", "mcp"), default="fixture")
    parser.add_argument("--model", help="Required for either live backend; choose an accessible model explicitly.")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--scenario", choices=("happy", "repeated", "premature", "malformed", "refusal", "rate-limit"), default="happy")
    parser.add_argument("--deadline", type=float, default=30)
    parser.add_argument("--max-decisions", type=int, default=4)
    parser.add_argument("--max-attempts", type=int, default=6)
    parser.add_argument("--max-retries", type=int, default=1)
    parser.add_argument("--max-output-tokens", type=int, default=1024)
    parser.add_argument("--cancel-file", type=Path, help="Creating this file cancels an active run.")
    args = parser.parse_args(argv)
    if args.backend in {"responses", "codex"} and (not args.model or args.scenario != "happy"):
        parser.error("Live backends require --model and do not accept scripted fault scenarios.")
    if args.backend == "student" and args.scenario != "happy":
        parser.error("Fault scenarios use the scripted backend.")
    try:
        limits = Limits(max_decisions=args.max_decisions, max_attempts=args.max_attempts,
                        max_retries=args.max_retries, deadline_seconds=args.deadline)
        from .student import StudentPlanner
        planner = (StudentPlanner() if args.backend == "student"
                   else ScriptedPlanner(scenario_actions(args.scenario)) if args.backend == "scripted"
                   else ResponsesPlanner(args.model, args.max_output_tokens) if args.backend == "responses"
                   else CodexPlanner(args.model))
        lookup = MCPLookup(args.out) if args.lookup == "mcp" else OfflineLookup()
        result = asyncio.run(run(planner, lookup, args.out, limits,
                                 cancelled=lambda: bool(args.cancel_file and args.cancel_file.exists())))
        print(json.dumps({key: result[key] for key in
                          ("status", "error", "planner_evidence", "lookup_evidence", "attempts", "tool_executions")}, indent=2))
        return 0 if result["task_acceptance"] else 1
    except (ValueError, OSError, ImportError) as error:
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
