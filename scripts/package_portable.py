"""Package the ready-built local portal without account, runtime, or learner data."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUT = DIST / "academy-portable.zip"


def package():
    if not (DIST / "index.html").is_file():
        raise SystemExit("Build the portal before packaging the portable bundle.")
    launcher = runpy.run_path(str(ROOT / "academy.py"))
    with launcher["portable_archive"](ROOT) as archive:
        OUT.write_bytes(archive.getvalue())
    print("{} ({:,} bytes)".format(OUT, OUT.stat().st_size))


if __name__ == "__main__":
    package()
