"""Personal learning records must never enter course downloads."""
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from scripts.package_project import package, source_files


class DistributionTests(unittest.TestCase):
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
            outside = Path(temporary) / "personal-notes.md"
            outside.write_text("PRIVATE")
            (root / "docs/linked.md").symlink_to(outside)
            (root / "docs/linked-dir").symlink_to(outside.parent, target_is_directory=True)
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
            (root / "docs").symlink_to(personal, target_is_directory=True)
            self.assertEqual(list(source_files(root)), [])


if __name__ == "__main__":
    unittest.main()
