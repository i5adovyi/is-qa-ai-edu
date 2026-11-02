"""Exercise durable progress through real HTTP servers, restarts, and SQLite backups."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, contextmanager
import http.client
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from academy_local import MAX_BODY
from tests.link_fixtures import directory_link, file_symlink


def state(note="Persisted work"):
    return {"version": 2, "done": ["L01"], "bookmarks": [], "gates": [],
            "notes": {"lesson": note}, "quiz": {}, "exercises": {}, "retention": [],
            "onboarding": [], "intervals": [1, 3, 7, 14], "futureEdition": {"keep": True}}


class LocalDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="academy-local-data-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "academy"
        self.root.mkdir()
        for name in ("academy.py", "academy_local.py", "academy.json"):
            shutil.copyfile(ROOT / name, self.root / name)
        (self.root / "dist").mkdir()
        for name in ("index.html", "app.js", "theme.js", "tracks.js", "data.js", "style.css"):
            (self.root / "dist" / name).write_text("COURSE", encoding="utf-8")
        self.profile = self.root / ".academy-data"
        self.env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(self.root / "academy.py"), *args],
                              cwd=self.temp.name, env=self.env, capture_output=True, text=True, timeout=15)

    @contextmanager
    def server(self, data_dir=None):
        with socket.socket() as candidate:
            candidate.bind(("127.0.0.1", 0))
            port = candidate.getsockname()[1]
        args = [sys.executable, str(self.root / "academy.py"), "local", "--no-build", "--no-browser",
                "--port", str(port)]
        if data_dir is not None:
            args += ["--data-dir", str(data_dir)]
        process = subprocess.Popen(args, cwd=self.temp.name, env=self.env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        url = "http://127.0.0.1:{}".format(port)
        try:
            deadline = time.monotonic() + 10
            while True:
                if process.poll() is not None:
                    out, err = process.communicate()
                    self.fail("Server exited early: " + out + err)
                try:
                    self.request(url)
                    break
                except (URLError, TimeoutError):
                    if time.monotonic() > deadline:
                        self.fail("Server did not start")
                    time.sleep(.04)
            yield url
        finally:
            if process.poll() is None:
                process.terminate()
            process.communicate(timeout=5)

    def request(self, url, payload=None, token=None, headers=None, path="/api/local-state", raw=None):
        supplied = dict(headers or {})
        method = "GET"
        body = None
        if payload is not None or raw is not None:
            method = "PUT"
            body = raw if raw is not None else json.dumps(payload).encode()
            supplied.setdefault("Content-Type", "application/json")
            supplied.setdefault("Origin", url)
            if token is not None:
                supplied["X-Academy-Token"] = token
        request = Request(url + path, data=body, headers=supplied, method=method)
        try:
            response = urlopen(request, timeout=5)
        except HTTPError as exc:
            response = exc
        with response:
            body = response.read()
            return response.status, json.loads(body), response.headers

    def test_committed_state_survives_restart_port_change_and_token_rotation(self):
        with self.server() as url:
            code, first, headers = self.request(url)
            self.assertEqual(code, 200)
            self.assertEqual(first["kind"], "academy-local")
            self.assertEqual(first["revision"], 0)
            self.assertIsNone(first["state"])
            self.assertEqual(Path(first["databasePath"]), (self.profile / "progress.sqlite3").resolve())
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertNotIn("Access-Control-Allow-Origin", headers)
            self.assertEqual(self.request(url, {"revision": 0, "state": state()}, first["csrfToken"])[:2],
                             (200, {"revision": 1}))
        with self.server() as url:
            _, restored, _ = self.request(url)
            self.assertEqual(restored["databaseId"], first["databaseId"])
            self.assertNotEqual(restored["csrfToken"], first["csrfToken"])
            self.assertEqual(restored["revision"], 1)
            self.assertEqual(restored["state"], state())
            self.assertEqual(self.request(url, {"revision": 1, "state": state("Wrong")}, first["csrfToken"])[0], 403)

    def test_concurrent_stale_tabs_cannot_overwrite_committed_work(self):
        with self.server() as url:
            token = self.request(url)[1]["csrfToken"]
            def write(number):
                return self.request(url, {"revision": 0, "state": state(str(number))}, token)
            with ThreadPoolExecutor(max_workers=5) as pool:
                results = list(pool.map(write, range(5)))
            self.assertEqual(sum(result[0] == 200 for result in results), 1)
            self.assertEqual(sum(result[0] == 409 for result in results), 4)
            for code, payload, _ in results:
                if code == 409:
                    self.assertEqual(payload["revision"], 1)
            _, saved, _ = self.request(url)
            self.assertEqual(saved["revision"], 1)
            self.assertEqual(self.request(url, {"revision": 1, "state": state("Merged")}, token)[0], 200)
            self.assertEqual(self.request(url)[1]["state"], state("Merged"))

    def test_host_origin_and_csrf_checks_reject_untrusted_writes(self):
        with self.server() as url:
            token = self.request(url)[1]["csrfToken"]
            payload = {"revision": 0, "state": state()}
            cases = [({"Host": "attacker.invalid:" + str(urlsplit(url).port)}, token),
                     ({"Origin": "https://attacker.invalid"}, token),
                     ({"Origin": "null"}, token), ({}, None), ({}, "wrong-token"),
                     ({"Origin": "http://localhost:" + str(urlsplit(url).port)}, token)]
            for headers, credential in cases:
                with self.subTest(headers=headers, credential=credential):
                    self.assertEqual(self.request(url, payload, credential, headers)[0], 403)
            self.assertEqual(self.request(url, headers={"Host": "127.0.0.1"})[0], 403)
            self.assertEqual(self.request(url)[1]["revision"], 0)
            # localhost itself works when both Host and Origin agree.
            alternate = "http://localhost:" + str(urlsplit(url).port)
            self.assertEqual(self.request(alternate, payload, token)[0], 200)

    def test_missing_origin_duplicate_host_and_oversized_content_are_rejected(self):
        with self.server() as url:
            token = self.request(url)[1]["csrfToken"]
            port = urlsplit(url).port
            payload = json.dumps({"revision": 0, "state": state()}).encode()
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("PUT", "/api/local-state", payload,
                         {"X-Academy-Token": token, "Content-Type": "application/json"})
            response = conn.getresponse()
            self.assertEqual(response.status, 403)
            response.read()
            conn.close()
            for length in (str(MAX_BODY + 1), "9" * 5000):
                conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
                conn.request("PUT", "/api/local-state", b"", {"Origin": url, "X-Academy-Token": token,
                             "Content-Type": "application/json", "Content-Length": length})
                response = conn.getresponse()
                self.assertEqual(response.status, 413)
                response.read()
                conn.close()
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            conn.putrequest("GET", "/api/local-state")
            conn.putheader("Host", "attacker.invalid")
            conn.endheaders()
            response = conn.getresponse()
            self.assertEqual(response.status, 403)
            response.read()
            conn.close()

    def test_invalid_json_state_and_media_never_replace_valid_work(self):
        with self.server() as url:
            token = self.request(url)[1]["csrfToken"]
            self.assertEqual(self.request(url, {"revision": 0, "state": state()}, token)[0], 200)
            malformed = [b"{", b"[]", b'{"revision":1,"revision":0,"state":{}}',
                         b'{"revision":1,"state":NaN}', b'\xff']
            for raw in malformed:
                with self.subTest(raw=raw):
                    self.assertEqual(self.request(url, token=token, raw=raw)[0], 400)
            for payload in ({"revision": True, "state": state()}, {"revision": -1, "state": state()},
                            {"revision": 1, "state": {}}, {"revision": 1, "state": []},
                            {"revision": 1, "state": dict(state(), version=True)},
                            {"revision": 1, "state": dict(state(), notes=[])}):
                with self.subTest(payload=payload):
                    self.assertEqual(self.request(url, payload, token)[0], 400)
            self.assertEqual(self.request(url, {"revision": 1, "state": state()}, token,
                                          {"Content-Type": "text/plain"})[0], 415)
            self.assertEqual(self.request(url)[1]["state"], state())
            self.assertEqual(self.request(url)[1]["revision"], 1)

    def test_backup_captures_live_wal_and_refuses_overwrite(self):
        custom = Path(self.temp.name) / "personal profile"
        output = Path(self.temp.name) / "backup.sqlite3"
        with self.server(custom) as url:
            token = self.request(url)[1]["csrfToken"]
            self.assertEqual(self.request(url, {"revision": 0, "state": state()}, token)[0], 200)
            result = self.invoke("backup", "--data-dir", str(custom), "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            original = output.read_bytes()
            duplicate = self.invoke("backup", "--data-dir", str(custom), "--output", str(output))
            self.assertEqual(duplicate.returncode, 2)
            self.assertIn("already exists", duplicate.stderr)
            self.assertEqual(output.read_bytes(), original)
            result = self.invoke("status", "--data-dir", str(custom))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["revision"], 1)
        restored = Path(self.temp.name) / "restored"
        restored.mkdir()
        shutil.copyfile(output, restored / "progress.sqlite3")
        with self.server(restored) as url:
            self.assertEqual(self.request(url)[1]["state"], state())
        self.assertFalse(self.profile.exists())

    def test_missing_or_corrupt_database_fails_explicitly_without_reset(self):
        self.assertEqual(self.invoke("status").returncode, 2)
        self.assertFalse(self.profile.exists())
        self.profile.mkdir()
        file = self.profile / "progress.sqlite3"
        file.write_bytes(b"A damaged file that must be preserved")
        for command in (("status",), ("local", "--no-browser", "--no-build")):
            result = self.invoke(*command)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not reset", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(file.read_bytes(), b"A damaged file that must be preserved")

    def test_corrupt_saved_record_is_not_silently_replaced(self):
        with self.server() as url:
            path = Path(self.request(url)[1]["databasePath"])
            with closing(sqlite3.connect(str(path))) as db:
                db.execute("UPDATE progress SET state='{}'")
                db.commit()
            code, payload, _ = self.request(url)
            self.assertEqual(code, 500)
            self.assertIn("not reset", payload["error"])
        result = self.invoke("status")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not reset", result.stderr)

    def test_private_runtime_files_symlinks_and_directory_lists_are_not_served_or_packaged(self):
        dist = self.root / "dist"
        filenames = ["private.sqlite3", "private.sqlite3-wal", "private.db", ".env", "academy-progress-1.json",
                     "academy-recovery-1.json", "academy-browser-progress.json", "academy-database-progress.json",
                     ".academy-data/progress.sqlite3", "directory/private.db-shm"]
        for filename in filenames:
            path = dist / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("PRIVATE", encoding="utf-8")
        (self.root / "secrets").mkdir()
        (self.root / "secrets/password.txt").write_text("PRIVATE", encoding="utf-8")
        directory_link(dist / "linked", self.root / "secrets")
        with self.subTest(link="file symlink"):
            file_symlink(dist / "leaked.txt", self.root / "secrets/password.txt")
            filenames.append("leaked.txt")
        with self.server() as url:
            for path in [*filenames, "linked/password.txt", "directory/"]:
                with self.subTest(path=path), self.assertRaises(HTTPError) as caught:
                    urlopen(url + "/" + path)
                self.assertEqual(caught.exception.code, 404)
            with urlopen(url + "/academy-portable.zip") as response:
                with ZipFile(BytesIO(response.read())) as archive:
                    names = archive.namelist()
                    self.assertIn("ai-engineering-academy-portable/academy_local.py", names)
                    for name in names:
                        self.assertNotIn(b"PRIVATE", archive.read(name))
                        self.assertNotIn(".academy-data", name)

    def test_data_and_backups_cannot_be_written_into_published_assets(self):
        for path in (self.root / "dist/data", self.root / "dist"):
            result = self.invoke("local", "--no-build", "--no-browser", "--data-dir", str(path))
            self.assertEqual(result.returncode, 2)
            self.assertIn("outside dist", result.stderr)
        directory_link(self.root / "linked-dist", self.root / "dist")
        result = self.invoke("local", "--no-build", "--no-browser", "--data-dir", str(self.root / "linked-dist/data"))
        self.assertEqual(result.returncode, 2)
        with self.server():
            result = self.invoke("backup", "--output", str(self.root / "dist/new.sqlite3"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("outside dist", result.stderr)
            self.assertFalse((self.root / "dist/new.sqlite3").exists())

    def test_unpublished_copy_runs_locally_and_hosted_mode_explains_next_step(self):
        config = json.loads((self.root / "academy.json").read_text())
        config["hostedUrl"] = None
        (self.root / "academy.json").write_text(json.dumps(config), encoding="utf-8")
        with self.server() as url:
            self.assertEqual(self.request(url)[0], 200)
        result = self.invoke("hosted", "--no-browser")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no published Site yet", result.stderr)


if __name__ == "__main__":
    unittest.main()
