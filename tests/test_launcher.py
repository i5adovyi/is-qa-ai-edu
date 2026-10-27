"""Exercise real local server startup, failure modes, and legacy entry points."""
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="academy-launcher-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "course with spaces"
        self.root.mkdir()
        for name in ("academy.py", "academy_local.py", "academy.json"):
            shutil.copyfile(ROOT / name, self.root / name)
        (self.root / "dist").mkdir()
        for name in ("index.html", "app.js", "theme.js", "tracks.js", "data.js", "style.css"):
            (self.root / "dist" / name).write_text("ACADEMY-ASSET", encoding="utf-8")
        (self.root / "private-note.txt").write_text("NOT-PUBLIC", encoding="utf-8")
        self.env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(self.root / "academy.py")] + list(args),
                              cwd=self.temp.name, env=self.env, capture_output=True, text=True, timeout=15)

    @contextmanager
    def server(self, entry="academy.py", args=()):
        with socket.socket() as candidate:
            candidate.bind(("127.0.0.1", 0))
            port = candidate.getsockname()[1]
        process = subprocess.Popen([sys.executable, str(self.root / entry)] +
                                   list(args) + ["--port", str(port)],
                                   cwd=self.temp.name, env=self.env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            url = "http://127.0.0.1:{}/".format(port)
            deadline = time.monotonic() + 10
            while True:
                if process.poll() is not None:
                    out, err = process.communicate()
                    self.fail("Server exited early: " + out + err)
                try:
                    with urlopen(url, timeout=0.3) as response:
                        self.assertEqual(response.read(), b"ACADEMY-ASSET")
                    break
                except (URLError, TimeoutError):
                    if time.monotonic() >= deadline:
                        self.fail("Server did not start")
                    time.sleep(0.05)
            yield url
        finally:
            if process.poll() is None:
                process.terminate()
            process.communicate(timeout=5)

    def test_portable_mode_works_from_another_directory_and_only_serves_dist(self):
        with self.server(args=("local", "--no-browser")) as url:
            for path in ("app.js", "theme.js", "tracks.js", "data.js", "style.css"):
                with urlopen(url + path) as response:
                    self.assertEqual(response.read(), b"ACADEMY-ASSET")
            for path in ("private-note.txt", "academy.json", "../private-note.txt", ".git/config"):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(url + path)
                self.assertEqual(caught.exception.code, 404)

    def test_simultaneous_tabs_can_load_all_assets(self):
        with self.server(args=("local", "--no-browser")) as url:
            assets = ["app.js", "theme.js", "tracks.js", "data.js", "style.css"] * 6
            barrier = Barrier(len(assets))
            def fetch(name):
                barrier.wait(timeout=5)
                with urlopen(url + name, timeout=5) as response:
                    return response.read()
            with ThreadPoolExecutor(max_workers=len(assets)) as pool:
                self.assertEqual(list(pool.map(fetch, assets)), [b"ACADEMY-ASSET"] * len(assets))

    def test_source_mode_rebuilds_in_its_own_directory(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "build_portal.py").write_text(
            "from pathlib import Path\n"
            "assert Path.cwd() == Path(__file__).resolve().parents[1]\n"
            "Path('built.txt').write_text('built')\n", encoding="utf-8")
        with self.server(args=("local", "--no-browser")):
            self.assertTrue((self.root / "built.txt").is_file())
        (self.root / "built.txt").unlink()
        with self.server(args=("local", "--no-browser", "--no-build")):
            self.assertFalse((self.root / "built.txt").exists())

    def test_hosted_prints_configured_url_without_build_or_server(self):
        shutil.rmtree(self.root / "dist")
        result = self.invoke("hosted", "--no-browser")
        self.assertEqual(result.returncode, 0, result.stderr)
        config = json.loads((self.root / "academy.json").read_text())
        self.assertIn(config["hostedUrl"], result.stdout)
        self.assertFalse((self.root / "dist").exists())

    def test_portable_download_can_be_extracted_and_downloaded_again(self):
        with self.server(args=("local", "--no-browser")) as url:
            with urlopen(Request(url + "academy-portable.zip", method="HEAD")) as response:
                self.assertEqual(response.read(), b"")
                self.assertGreater(int(response.headers["Content-Length"]), 0)
            with urlopen(url + "academy-portable.zip") as response:
                data = response.read()
        self.assertFalse((self.root / "dist/academy-portable.zip").exists())
        with ZipFile(BytesIO(data)) as archive:
            names = archive.namelist()
            self.assertIn("ai-engineering-academy-portable/academy.py", names)
            self.assertIn("ai-engineering-academy-portable/academy_local.py", names)
            self.assertIn("ai-engineering-academy-portable/academy.json", names)
            self.assertNotIn("ai-engineering-academy-portable/private-note.txt", names)
            extracted = Path(self.temp.name) / "roundtrip"
            archive.extractall(extracted)
        self.root = extracted / "ai-engineering-academy-portable"
        with self.server(args=("local", "--no-browser")) as url:
            with urlopen(url + "academy-portable.zip") as response:
                with ZipFile(BytesIO(response.read())) as second:
                    self.assertEqual(second.namelist(), names)

    def test_invalid_port_incomplete_build_bad_config_and_build_failure_are_clear(self):
        result = self.invoke("local", "--no-browser", "--port", "0")
        self.assertEqual(result.returncode, 2)
        self.assertIn("port must be", result.stderr)
        (self.root / "dist/data.js").unlink()
        result = self.invoke("local", "--no-browser")
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing or incomplete", result.stderr)
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "build_portal.py").write_text("raise SystemExit(1)\n", encoding="utf-8")
        result = self.invoke("local", "--no-browser")
        self.assertEqual(result.returncode, 2)
        self.assertIn("server was not started", result.stderr)
        (self.root / "academy.json").write_text('{"hostedUrl": 123}', encoding="utf-8")
        result = self.invoke("hosted", "--no-browser")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_busy_port_keeps_existing_listener(self):
        with socket.socket() as existing:
            existing.bind(("127.0.0.1", 0))
            existing.listen()
            result = self.invoke("local", "--no-browser", "--port", str(existing.getsockname()[1]))
            self.assertEqual(result.returncode, 2)
            self.assertIn("Try --port", result.stderr)
            self.assertGreater(existing.fileno(), 0)

    def test_legacy_source_and_portable_server_commands(self):
        (self.root / "scripts").mkdir()
        for name in ("serve.py", "serve_portal.py"):
            shutil.copyfile(ROOT / "scripts" / name, self.root / "scripts" / name)
        shutil.copyfile(ROOT / "scripts/serve_portal.py", self.root / "serve.py")
        for entry in ("scripts/serve.py", "scripts/serve_portal.py", "serve.py"):
            with self.subTest(entry=entry), self.server(entry):
                pass


if __name__ == "__main__":
    unittest.main()
