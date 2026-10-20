"""Package the ready-built local portal without account, runtime, or learner data."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUT = DIST / "academy-portable.zip"


def package():
    if not (DIST / "index.html").is_file():
        raise SystemExit("Build the portal before packaging the portable bundle.")
    prefix = "ai-engineering-academy-portable/"
    with ZipFile(OUT, "w", ZIP_DEFLATED) as archive:
        for item in sorted(DIST.rglob("*")):
            if item.is_file() and not item.is_symlink() and item != OUT:
                archive.write(item, prefix + "dist/" + item.relative_to(DIST).as_posix())
        archive.write(ROOT / "scripts/serve_portal.py", prefix + "serve.py")
        archive.write(ROOT / "docs/CONTINUE-LEARNING.md", prefix + "CONTINUE-LEARNING.md")
        archive.write(ROOT / "docs/ACCOUNT-MIGRATION.md", prefix + "ACCOUNT-MIGRATION.md")
        archive.writestr(prefix + "README.txt", (
            "AI ENGINEERING ACADEMY — PORTABLE EDITION\n\n"
            "Extract this entire folder. Python 3.9+ is required for the local server.\n"
            "Open a terminal in this folder and run: python3 serve.py\n"
            "On Windows, use: py -3 serve.py\n"
            "Visit http://127.0.0.1:8765 and keep the terminal open. Stop with Ctrl+C.\n\n"
            "No OpenAI account is required for this local portal.\n"
            "Import your separately exported progress JSON on the Progress page.\n"
            "Personal progress, credentials and chat history are NOT in this bundle.\n"
            "External videos/courses require internet; live-model labs need their own access.\n"
            "Editable sources are in dist/academy-source.zip. The PDF is dist/fieldbook.pdf.\n"
            "Read ACCOUNT-MIGRATION.md and CONTINUE-LEARNING.md before changing accounts.\n"
        ))
    print("{} ({:,} bytes)".format(OUT, OUT.stat().st_size))


if __name__ == "__main__":
    package()
