"""Personal learning records must never enter course downloads."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

from scripts.package_project import package, source_files
from tests.link_fixtures import directory_link, file_symlink


class DistributionTests(unittest.TestCase):
    def test_builder_rejects_redirected_inputs_and_output_before_writing(self):
        source = Path(__file__).resolve().parents[1]
        for rel in ("output/pdf", "content/how-to", "dist/docs"):
            with self.subTest(link=rel), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "course"
                (root / "scripts").mkdir(parents=True)
                shutil.copyfile(source / "academy_local.py", root / "academy_local.py")
                for name in ("build_portal.py", "build_subject_catalog.py", "package_project.py"):
                    shutil.copyfile(source / "scripts" / name, root / "scripts" / name)
                outside = Path(temporary) / "personal"
                outside.mkdir()
                marker = outside / "START-HERE.md"
                marker.write_text("untouched")
                link = root / rel
                link.parent.mkdir(exist_ok=True, parents=True)
                directory_link(link, outside)
                run = subprocess.run([sys.executable, "scripts/build_portal.py"], cwd=root,
                                     capture_output=True, text=True, timeout=10)
                self.assertNotEqual(run.returncode, 0)
                self.assertIn("Linked build path: " + rel, run.stderr.replace("\\", "/"))
                self.assertEqual(marker.read_text(), "untouched")
                self.assertFalse((root / "dist/data.js").exists())

    def test_source_archive_excludes_runtime_credentials_databases_and_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve() / "course"
            root.mkdir()
            public = {
                "README.md": "Course",
                "AGENTS.md": "Tutor instructions",
                "CLAUDE.md": "Claude entry point",
                "academy.py": "# launcher",
                "academy_local.py": "# local storage",
                "academy.json": '{"hostedUrl":null}',
                ".openai/hosting.json": '{"static":{"directory":"dist"}}',
                "docs/guide.md": "Public guide",
                ".github/workflows/academy.yml": "name: Tests",
                "lab/example.py": "# teaching source",
                "lab/.env.example": "API_KEY=",
            }
            private = {
                ".academy-data/progress.sqlite3": "PRIVATE",
                "work/attempt.json": "PRIVATE",
                ".openai/credential.json": "PRIVATE",
                ".git/config": "PRIVATE",
                "docs/progress.sqlite3": "PRIVATE",
                "docs/progress.sqlite3-wal": "PRIVATE",
                "docs/progress.sqlite3-shm": "PRIVATE",
                "docs/backup.db": "PRIVATE",
                "docs/backup.sqlite": "PRIVATE",
                "docs/.env": "PRIVATE",
                "docs/.env.local": "PRIVATE",
                "docs/academy-progress (1).json": "PRIVATE",
                "docs/academy-recovery.json": "PRIVATE",
                "docs/academy-browser-progress.json": "PRIVATE",
                "docs/academy-database-progress.json": "PRIVATE",
                "lab/runs/trace.json": "PRIVATE",
                "lab/.venv/config.py": "PRIVATE",
                "lab/__pycache__/old.pyc": "PRIVATE",
                "portal/node_modules/token.txt": "PRIVATE",
                "docs/archive.zip": "PRIVATE",
            }
            for name, text in {**public, **private}.items():
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(text)
            personal = Path(temporary) / "private"
            personal.mkdir()
            outside = personal / "personal-notes.md"
            outside.write_text("PRIVATE")
            directory_link(root / "docs/linked-dir", personal)
            with self.subTest(link="file symlink"):
                file_symlink(root / "docs/linked.md", outside)
            actual = {path.relative_to(root).as_posix() for path in source_files(root)}
            self.assertEqual(actual, set(public))
            output = root / "source.zip"
            package(root, output)
            with ZipFile(output) as archive:
                self.assertEqual(set(archive.namelist()),
                                 {"ai-engineering-academy/" + name for name in public})
                for name in archive.namelist():
                    self.assertNotIn(b"PRIVATE", archive.read(name))

    def test_symlinked_included_folder_is_not_distributed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve() / "course"
            root.mkdir()
            personal = Path(temporary) / "personal"
            personal.mkdir()
            (personal / "notes.md").write_text("PRIVATE")
            directory_link(root / "docs", personal)
            self.assertEqual(list(source_files(root)), [])


if __name__ == "__main__":
    unittest.main()
