"""Repo-local skill installation, validation, and reproducible host prompts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from academy_local import is_link

SOURCE = ROOT / "content" / "skill-practice"
NAME = "signal-desk-evidence-review"
REQUIRED = ("SKILL.md", "references/review-contract.md", "assets/review-template.json", "scripts/check_packet.py")


def safe_workspace(path, root=ROOT):
    root = root.resolve()
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    if ".." in candidate.parts:
        raise ValueError("workspace must not contain '..'")
    try:
        relative = candidate.relative_to(root / "work")
    except ValueError:
        raise ValueError("workspace must be a child of this academy's work directory")
    if not relative.parts:
        raise ValueError("choose a dedicated child directory under work")
    cursor = root
    for part in candidate.relative_to(root).parts:
        cursor = cursor / part
        if is_link(cursor):
            raise ValueError("symlink workspace component rejected: " + str(cursor))
    return candidate


def validate_install(workspace):
    skill = workspace / ".agents" / "skills" / NAME
    for rel in REQUIRED:
        path = skill / rel
        cursor = path
        while cursor != workspace:
            if is_link(cursor):
                raise ValueError("symlink skill component rejected: " + str(cursor))
            cursor = cursor.parent
        if not path.is_file():
            raise ValueError("missing skill dependency: " + rel)
    text = (skill / "SKILL.md").read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("SKILL.md requires YAML frontmatter")
    front = text.split("---\n", 2)[1]
    if "name: " + NAME not in front or "description: " not in front:
        raise ValueError("skill metadata is missing")
    return {"status": "installed_and_validated", "host_behavior": "not_tested", "skill": NAME,
            "files": {rel: hashlib.sha256((skill / rel).read_bytes()).hexdigest() for rel in REQUIRED}}


def install(workspace, source=SOURCE):
    if workspace.exists():
        raise ValueError("workspace already exists; choose a fresh name (no overwrite)")
    package = source / NAME
    if is_link(source):
        raise ValueError("source symlinks are not allowed")
    # Stop at a redirected directory before recursing through its contents.
    for parent, directories, files in os.walk(source):
        if any(is_link(Path(parent) / name) for name in directories + files):
            raise ValueError("source symlinks are not allowed")
    for rel in REQUIRED:
        if not (package / rel).is_file():
            raise ValueError("source dependency missing: " + rel)
    workspace.mkdir(parents=True)
    destination = workspace / ".agents" / "skills" / NAME
    shutil.copytree(package, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(source / "fixtures", workspace / "fixtures")
    result = validate_install(workspace)
    (workspace / "installation.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "validate"))
    parser.add_argument("--workspace", default="work/skill-practice")
    args = parser.parse_args()
    try:
        workspace = safe_workspace(args.workspace)
        result = install(workspace) if args.command == "install" else validate_install(workspace)
    except (ValueError, OSError) as exc:
        parser.exit(1, "ERROR: " + str(exc) + "\n")
    result["workspace"] = str(workspace)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
