"""Run the actual MCP integration acceptance gate."""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Fresh output directory")
    parser.add_argument("--server-file", type=Path, help="Use a learner copy of server.py")
    parser.add_argument("--exercise", action="store_true", help="Also require the learner list_topics extension")
    args = parser.parse_args()
    try:
        import anyio
        from .client import run_suite
    except ImportError:
        parser.exit(2, "Optional MCP dependencies missing. Follow lab/mcp_lab/README.md in a separate Python 3.12 environment.\n")
    try:
        report = anyio.run(run_suite, args.out, args.server_file, args.exercise)
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + "\n")
    print("Real MCP checks: {passed}/{total}; evidence: {path}".format(path=args.out, **report))
    if report["aborted"]:
        print("Integration aborted; later checks did not run. Inspect report.json and messages.jsonl.")
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
