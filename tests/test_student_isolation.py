"""A learner's unfinished source must not disable the working reference."""

from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


class StudentIsolationTest(unittest.TestCase):
    def test_broken_student_source_does_not_break_reference_commands(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(Path(__file__).parents[1] / "lab", root / "lab",
                            ignore=shutil.ignore_patterns("__pycache__"))
            for variant, source in (
                ("syntax", "def unfinished(:\n    pass\n"),
                ("import", "import academy_missing_student_dependency\n"),
            ):
                (root / "lab/student.py").write_text(source, encoding="utf-8")
                commands = [
                    (["lab.cli", "demo"], 0),
                    (["lab.composed", "run", "--components", "completed"], 0),
                    (["lab.model_bridge", "export"], 0),
                    (["lab.cli", "practice", "--lab", "01"], 2),
                    (["lab.cli", "evaluate", "--policy", "student"], 2),
                    (["lab.composed", "run", "--components", "student"], 2),
                ]
                for index, (arguments, expected) in enumerate(commands):
                    with self.subTest(variant=variant, command=arguments):
                        output = root / f"{variant}-{index}"
                        if "practice" not in arguments:
                            arguments = arguments + ["--out", str(output)]
                        result = subprocess.run(
                            [sys.executable, "-m"] + arguments, cwd=root,
                            text=True, capture_output=True, timeout=30)
                        self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
                        if expected == 2:
                            self.assertIn("student_import", result.stderr + result.stdout)
                            self.assertNotIn("Traceback", result.stderr + result.stdout)
                            self.assertFalse(output.exists())

    def test_student_checkpoint_resumes_in_a_fresh_process_with_another_hash_seed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repository = Path(__file__).parents[1]
            shutil.copytree(repository / "lab", root / "lab",
                            ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(repository / "content/labs/solutions/reference.py",
                            root / "lab/student.py")
            fingerprints = []
            for seed in ("1", "9"):
                environment = {**os.environ, "PYTHONHASHSEED": seed,
                               "PYTHONPYCACHEPREFIX": str(root / ("cache-" + seed))}
                inspected = subprocess.run(
                    [sys.executable, "-c",
                     "from lab.composed import Components; "
                     "print(Components('student').identity['fingerprint'])"],
                    cwd=root, env=environment, text=True, capture_output=True, timeout=30)
                self.assertEqual(inspected.returncode, 0, inspected.stderr)
                fingerprints.append(inspected.stdout.strip())
                arguments = (["run", "--scenario", "crash-after-write", "--out", str(root / "run")]
                             if seed == "1" else ["resume", str(root / "run/checkpoint.json")])
                result = subprocess.run(
                    [sys.executable, "-m", "lab.composed"] + arguments + ["--components", "student"],
                    cwd=root, env=environment, text=True, capture_output=True, timeout=30)
                self.assertEqual(result.returncode, 3 if seed == "1" else 0,
                                 result.stderr + result.stdout)
            self.assertEqual(fingerprints[0], fingerprints[1])
            result = json.loads((root / "run/result.json").read_text())
            self.assertEqual((result["draft_count"], result["writes"]), (1, 1))


if __name__ == "__main__":
    unittest.main()
