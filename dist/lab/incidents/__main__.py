import argparse
import json
import sys

from . import engine
from .scenarios import IDS


def main(argv=None):
    parser = argparse.ArgumentParser(description="Local incident practice; guidance opens only after a saved attempt.")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create a new workspace without overwriting anything")
    init.add_argument("incident", choices=IDS)
    init.add_argument("--workspace", required=True)
    init.add_argument("--variant", choices=["primary", "transfer"], default="primary")
    init.add_argument("--project", choices=["support", "qa", "research"], default="support")
    for name in ("run", "check", "attempt", "hint", "debrief"):
        command = sub.add_parser(name)
        command.add_argument("--workspace", required=True)
        if name == "attempt":
            command.add_argument("--hypothesis", required=True)
            command.add_argument("--evidence", required=True)
            command.add_argument("--next-check", required=True)
        if name == "hint":
            command.add_argument("--level", type=int, choices=[1, 2, 3], required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            root = engine.initialize(args.incident, args.workspace, args.variant, args.project)
            result = {"created": str(root), "next": "Read brief.md, evidence/, input.json, and CONTRACT.md. Record an attempt before requesting guidance."}
        elif args.command == "run":
            result = engine.run(args.workspace)
        elif args.command == "check":
            result = engine.check(args.workspace)
        elif args.command == "attempt":
            result = engine.attempt(args.workspace, args.hypothesis, args.evidence, args.next_check)
        elif args.command == "hint":
            result = engine.guidance(args.workspace, args.level)
        else:
            result = engine.guidance(args.workspace)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 1 if args.command == "check" and not result["passed"] else 0


if __name__ == "__main__":
    sys.exit(main())
