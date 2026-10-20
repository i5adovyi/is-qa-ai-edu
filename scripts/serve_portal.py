"""Compatibility entry point: serve the built academy without opening a browser."""
from pathlib import Path
import runpy
import sys


def main():
    here = Path(__file__).resolve().parent
    root = here.parent if here.name == "scripts" else here
    launcher = runpy.run_path(str(root / "academy.py"))
    return launcher["main"](["local", "--no-build", "--no-browser"] + sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
