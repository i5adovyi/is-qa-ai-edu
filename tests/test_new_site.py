"""New-account export must separate Site identity and learner data from course sources."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_new_site import prepare


class NewSiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.parent = Path(self.temporary.name)
        self.source = self.parent / "source"
        self.source.mkdir()
        self.write("academy.json", json.dumps({
            "hostedUrl": "https://old-account.example.test",
            "repositoryUrl": "https://github.com/example/course",
        }))
        self.write("academy.py", "# source launcher\n")
        self.write("academy_local.py", "# local database support\n")
        self.write("AGENTS.md", "# Tutor instructions\n")
        self.write("scripts/build_portal.py", (
            "from pathlib import Path\n"
            "Path('dist').mkdir(exist_ok=True)\n"
            "Path('dist/index.html').write_text('fresh build')\n"
        ))
        self.write(".openai/hosting.json", '{"project_id":"old-project","static":{"directory":"dist"}}')
        self.write("docs/example.md", "# Course material\n")
        self.write("lab/data/example.json", '{"synthetic":"fixture"}')

    def write(self, path, text):
        item = self.source / path
        item.parent.mkdir(parents=True, exist_ok=True)
        item.write_text(text, encoding="utf-8")
        return item

    def test_new_copy_has_no_old_identity_history_or_private_records(self):
        excluded = [
            ".git/config", ".openai/credential.json", ".academy-data/progress.sqlite3",
            ".academy-data/progress.sqlite3-wal", "work/attempts.json",
            ".lab-runs/trace.jsonl", ".env", ".env.local", "lab/.env",
            "lab/runs/attempt.json", "lab/progress.sqlite3", "docs/notes.db",
            "docs/academy-progress-2026.json", "private-notes.md", "dist/stale.html",
            "scripts/__pycache__/old.pyc",
        ]
        for name in excluded:
            self.write(name, "PRIVATE_OR_STALE")
        secret = self.parent / "secret.txt"
        secret.write_text("outside secret")
        (self.source / "docs/link.md").symlink_to(secret)
        original = (self.source / "academy.json").read_bytes()
        original_hosting = (self.source / ".openai/hosting.json").read_bytes()
        destination = prepare(self.source, self.parent / "new-account")
        for name in excluded:
            self.assertFalse((destination / name).exists(), name)
        self.assertFalse((destination / "docs/link.md").exists())
        self.assertEqual((destination / "dist/index.html").read_text(), "fresh build")
        self.assertEqual((destination / "academy_local.py").read_text(), "# local database support\n")
        self.assertEqual((destination / "AGENTS.md").read_text(), "# Tutor instructions\n")
        self.assertEqual(json.loads((destination / ".openai/hosting.json").read_text()),
                         {"static": {"directory": "dist"}})
        configuration = json.loads((destination / "academy.json").read_text())
        self.assertIsNone(configuration["hostedUrl"])
        self.assertEqual(configuration["repositoryUrl"], "https://github.com/example/course")
        self.assertEqual((self.source / "academy.json").read_bytes(), original)
        self.assertEqual((self.source / ".openai/hosting.json").read_bytes(), original_hosting)
        self.assertTrue((destination / "lab/data/example.json").is_file())

    def test_existing_destination_and_source_descendant_refused(self):
        existing = self.parent / "existing"
        existing.mkdir()
        marker = existing / "keep.txt"
        marker.write_text("keep")
        for destination in (existing, self.source, self.source / "new-account"):
            with self.assertRaises(ValueError):
                prepare(self.source, destination)
        self.assertEqual(marker.read_text(), "keep")
        self.assertFalse((self.source / "new-account").exists())
        alias = self.parent / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError):
            prepare(self.source, alias / "nested")

    def test_missing_parent_or_required_source_creates_nothing(self):
        with self.assertRaises(ValueError):
            prepare(self.source, self.parent / "missing" / "new")
        (self.source / "academy.py").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required source"):
            prepare(self.source, self.parent / "new")
        self.assertFalse((self.parent / "new").exists())

    def test_broken_builder_reports_failure_without_mutating_source(self):
        self.write("scripts/build_portal.py", "raise SystemExit(9)\n")
        with self.assertRaises(subprocess.CalledProcessError):
            prepare(self.source, self.parent / "failed")
        self.assertEqual(json.loads((self.source / "academy.json").read_text())["hostedUrl"],
                         "https://old-account.example.test")
        self.assertTrue((self.parent / "failed/academy.py").is_file())

    def test_cli_requires_explicit_destination(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/prepare_new_site.py")],
            capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--destination", result.stderr)


if __name__ == "__main__":
    unittest.main()
