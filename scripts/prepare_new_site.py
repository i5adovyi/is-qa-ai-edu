"""Prepare a separate source copy for publishing a NEW private Site in another account."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from package_project import source_files

ROOT = Path(__file__).resolve().parents[1]


def prepare(source, destination):
    """Copy distributed sources, reset only the copy's Site identity, and build it."""
    source = Path(source).resolve()
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("Destination already exists. Choose a new folder; nothing was overwritten.")
    # Resolve parent links before testing containment. An export inside the source
    # could be mistaken for project material or recursively packaged on later runs.
    destination = destination.resolve()
    if destination == source or source in destination.parents:
        raise ValueError("Destination must be outside the original project folder.")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent does not exist. Create it first, then retry.")
    files = list(source_files(source))
    required = ("academy.py", "academy_local.py", "academy.json", "scripts/build_portal.py")
    for name in required:
        if source / name not in files:
            raise ValueError("Missing required source: " + name)
    configuration = json.loads((source / "academy.json").read_text(encoding="utf-8"))
    configuration["hostedUrl"] = None
    # Exclusive creation prevents an existing learner's copy from being replaced.
    destination.mkdir()
    for item in files:
        relative = item.relative_to(source)
        if relative.parts[0] == ".openai" or relative.as_posix() == "academy.json":
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
    (destination / "academy.json").write_text(
        json.dumps(configuration, indent=2) + "\n", encoding="utf-8"
    )
    hosting = destination / ".openai" / "hosting.json"
    hosting.parent.mkdir()
    hosting.write_text(
        json.dumps({"static": {"directory": "dist"}}, indent=2) + "\n", encoding="utf-8"
    )
    subprocess.run(
        [sys.executable, str(destination / "scripts/build_portal.py")],
        cwd=str(destination), check=True
    )
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--destination", required=True,
        help="new folder outside this project (parent must exist)"
    )
    args = parser.parse_args(argv)
    try:
        destination = prepare(ROOT, args.destination)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, "Could not prepare new Site: {}.\nIf a new folder was created, "
                    "it is incomplete; inspect it and choose another destination.\n".format(exc))
    print("Prepared new-account source: " + str(destination))
    print("No existing Site identity, Git history, or learner data was transferred.")
    print("Local launch: open that folder, then run python3 academy.py local")
    print("To publish: sign in to the target account, open this prepared folder in Codex,")
    print("and ask the Sites workflow to create a NEW private Site. Read docs/NEW-ACCOUNT.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
