"""Open the hosted academy or build and serve a local copy. Python 3.9+, no packages."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
from urllib.parse import urlsplit
import webbrowser
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
# Legacy launchers and the portable packager load this file through runpy.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from academy_local import ConflictError, MAX_BODY, ProgressDatabase, StateError, strict_json


def private_asset(relative):
    parts = [part.lower() for part in Path(relative).parts]
    name = Path(relative).name.lower()
    excluded = {".academy-data", ".git", ".openai", ".codex", ".venv", "venv",
                "node_modules", "__pycache__", "work", "runs", ".lab-runs"}
    return (any(part in excluded for part in parts)
            or any(part.startswith(".env") and part != ".env.example" for part in parts)
            or name.endswith((".sqlite", ".sqlite3", ".db", ".pyc"))
            or any(marker in name for marker in (".sqlite-", ".sqlite3-", ".db-"))
            or name.startswith(("academy-progress", "academy-recovery", "academy-browser-progress",
                                "academy-database-progress")))


def has_symlink(path, boundary):
    current = Path(path)
    boundary = Path(boundary)
    while current != boundary:
        if current.is_symlink():
            return True
        if current.parent == current:
            return True
        current = current.parent
    return boundary.is_symlink()


def portable_archive(root):
    """Package only course assets; also works inside an extracted portable copy."""
    root = Path(root)
    dist = root / "dist"
    buffer = BytesIO()
    prefix = "ai-engineering-academy-portable/"
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for item in sorted(dist.rglob("*")):
            if (item.is_file() and not has_symlink(item, dist)
                    and not private_asset(item.relative_to(dist))
                    and item != dist / "academy-portable.zip"):
                archive.write(item, prefix + "dist/" + item.relative_to(dist).as_posix())
        for name in ("academy.py", "academy_local.py", "academy.json"):
            if has_symlink(root / name, root):
                raise StateError("Cannot package a linked launcher file: " + name)
            archive.write(root / name, prefix + name)
        legacy = root / "scripts/serve_portal.py"
        if not legacy.is_file():
            legacy = root / "serve.py"
        if legacy.is_file() and not has_symlink(legacy, root):
            archive.write(legacy, prefix + "serve.py")
        for name in ("CONTINUE-LEARNING.md", "ACCOUNT-MIGRATION.md", "RUN-ANYWHERE.md",
                     "NEW-ACCOUNT.md", "LOCAL-DATA.md"):
            source = root / "docs" / name
            if not source.is_file():
                source = root / name
            if source.is_file() and not has_symlink(source, root):
                text = source.read_text(encoding="utf-8")
                if name == "RUN-ANYWHERE.md":
                    for linked in ("SETUP.md", "MAINTENANCE.md", "ACCOUNT-MIGRATION.md"):
                        text = text.replace("](" + linked + ")", "](dist/docs/" + linked + ")")
                archive.writestr(prefix + name, text)
        archive.writestr(prefix + "README.txt", (
            "AI ENGINEERING ACADEMY - PORTABLE EDITION\n\n"
            "Extract this entire folder. Python 3.9+ is required.\n"
            "Run: python3 academy.py local\n"
            "On Windows: py -3 academy.py local\n"
            "Keep the terminal open. Stop with Ctrl+C.\n"
            "The browser opens http://127.0.0.1:8765/.\n"
            "Use --port 8766 for another port, or --no-browser to print the URL only.\n"
            "The older python3 serve.py command also works.\n\n"
            "Open the existing private OpenAI Site: python3 academy.py hosted\n"
            "No OpenAI account is required for the local portal.\n"
            "Local progress is saved in .academy-data/progress.sqlite3 between sessions.\n"
            "Back up: python3 academy.py backup --output /path/to/new-backup.sqlite3\n"
            "Import your separately exported progress JSON on the Progress page.\n"
            "Personal progress, credentials and chat history are NOT in this bundle.\n"
            "External resources need internet; live-model labs need their own access.\n"
            "Editable sources: dist/academy-source.zip. PDF: dist/fieldbook.pdf.\n"
            "Read RUN-ANYWHERE.md, ACCOUNT-MIGRATION.md and CONTINUE-LEARNING.md.\n"
        ))
    buffer.seek(0)
    return buffer


class AcademyServer(ThreadingHTTPServer):
    # Several tabs can request the JS, styles, data and state API simultaneously.
    # Python 3.9's default backlog of five can reset these connections on macOS.
    request_queue_size = 128


class AcademyHandler(SimpleHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def json_response(self, status, payload):
        encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(encoded)

    def trusted_host(self):
        expected = {"127.0.0.1:{}".format(self.server.server_port),
                    "localhost:{}".format(self.server.server_port)}
        hosts = self.headers.get_all("Host", [])
        if len(hosts) != 1 or hosts[0] not in expected:
            self.json_response(403, {"error": "Only the exact localhost address and port are allowed."})
            return False
        return True

    def do_PUT(self):
        if not self.trusted_host():
            return
        if urlsplit(self.path).path != "/api/local-state":
            self.json_response(404, {"error": "Unknown local API endpoint."})
            return
        origins = self.headers.get_all("Origin", [])
        if origins != ["http://" + self.headers["Host"]]:
            self.json_response(403, {"error": "Progress writes require this page's exact local origin."})
            return
        tokens = self.headers.get_all("X-Academy-Token", [])
        if len(tokens) != 1 or not secrets.compare_digest(tokens[0].encode("utf-8"),
                                                        self.server.database.csrf_token.encode("ascii")):
            self.json_response(403, {"error": "Missing or stale local token. Reload before saving."})
            return
        if self.headers.get("Transfer-Encoding"):
            self.json_response(400, {"error": "Chunked requests are not supported."})
            return
        lengths = self.headers.get_all("Content-Length", [])
        if not lengths:
            self.json_response(411, {"error": "Content-Length is required."})
            return
        if len(lengths) != 1 or not lengths[0].isascii() or not lengths[0].isdigit():
            self.json_response(400, {"error": "Invalid Content-Length."})
            return
        if len(lengths[0]) > 8:
            self.json_response(413, {"error": "Progress request exceeds the 8 MiB limit."})
            return
        length = int(lengths[0])
        if not 0 < length <= MAX_BODY:
            self.json_response(413, {"error": "Progress request must be between 1 byte and 8 MiB."})
            return
        if self.headers.get_content_type() != "application/json":
            self.json_response(415, {"error": "Content-Type must be application/json."})
            return
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise StateError("Incomplete request body; progress was not saved.")
            payload = strict_json(raw.decode("utf-8"))
            if not isinstance(payload, dict) or set(payload) != {"revision", "state"}:
                raise StateError("Expected a JSON object containing revision and state.")
            revision = self.server.database.write(payload["revision"], payload["state"])
        except ConflictError as exc:
            self.json_response(409, {"error": str(exc), "revision": exc.revision})
        except (ValueError, UnicodeError, RecursionError) as exc:
            self.json_response(400, {"error": "Progress was not saved: {}".format(exc)})
        except (sqlite3.Error, OSError) as exc:
            self.json_response(500, {"error": "Local database write failed: {}. Export your draft.".format(exc)})
        else:
            self.json_response(200, {"revision": revision})

    def list_directory(self, path):
        self.send_error(404, "Directory listing is disabled")
        return None

    def send_head(self):
        if not self.trusted_host():
            return None
        if urlsplit(self.path).path == "/api/local-state":
            try:
                payload = dict(self.server.database.read(), kind="academy-local",
                               csrfToken=self.server.database.csrf_token,
                               databasePath=str(self.server.database.path))
            except (sqlite3.Error, OSError, ValueError, RecursionError) as exc:
                self.json_response(500, {"error": "Local database read failed: {}. The file was not reset.".format(exc)})
            else:
                self.json_response(200, payload)
            return None
        # SimpleHTTPRequestHandler normally follows symlinks. A course file must
        # never expose a linked database, home directory, or other private file.
        translated = Path(self.translate_path(self.path))
        directory = Path(self.directory)
        try:
            relative = translated.relative_to(directory)
            translated.resolve().relative_to(directory.resolve())
        except ValueError:
            self.send_error(404)
            return None
        if has_symlink(translated, directory) or private_asset(relative):
            self.send_error(404)
            return None
        # An extracted ZIP cannot contain itself. Recreate that download locally
        # without requiring hosted access or writing into the learner's copy.
        if urlsplit(self.path).path == "/academy-portable.zip" and not (
                Path(self.directory) / "academy-portable.zip").is_file():
            data = portable_archive(ROOT)
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", 'attachment; filename="academy-portable.zip"')
            self.send_header("Content-Length", str(data.getbuffer().nbytes))
            self.end_headers()
            return data
        return super().send_head()


def configuration():
    config = json.loads((ROOT / "academy.json").read_text(encoding="utf-8"))
    for key in ("hostedUrl", "repositoryUrl"):
        if key == "hostedUrl" and config.get(key) in (None, ""):
            continue
        if not isinstance(config[key], str):
            raise ValueError("{} must be an HTTPS URL".format(key))
        url = urlsplit(config[key])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("{} must be an HTTPS URL without credentials".format(key))
    return config


def open_browser(url):
    try:
        opened = webbrowser.open(url)
    except (webbrowser.Error, OSError):
        opened = False
    if not opened:
        print("Open the printed URL in your browser.", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("local", "hosted", "backup", "status"), default="local")
    parser.add_argument("--port", type=int, default=8765, help="local port (default: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="print the URL without opening a browser")
    parser.add_argument("--no-build", action="store_true", help="serve existing dist files without rebuilding")
    parser.add_argument("--data-dir", type=Path, default=ROOT / ".academy-data",
                        help="local profile directory (default: this project's .academy-data)")
    parser.add_argument("--output", type=Path, help="new SQLite backup filename (backup mode only)")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if args.output and args.mode != "backup":
        parser.error("--output is only supported with backup")
    if args.mode == "backup" and not args.output:
        parser.error("backup requires --output with a new SQLite filename")
    if args.mode == "backup":
        try:
            args.output.expanduser().resolve().relative_to((ROOT / "dist").resolve())
        except ValueError:
            pass
        else:
            parser.error("Backup output must be outside dist/ so private progress is never published.")
    if args.mode in ("backup", "status"):
        try:
            database = ProgressDatabase(args.data_dir / "progress.sqlite3", create=False)
            if args.mode == "backup":
                print("Local progress backup: " + str(database.backup(args.output)), flush=True)
            else:
                record = database.read()
                print(json.dumps({"databasePath": str(database.path), "databaseId": record["databaseId"],
                                  "revision": record["revision"], "hasProgress": record["state"] is not None},
                                 indent=2), flush=True)
        except (OSError, sqlite3.Error, ValueError) as exc:
            parser.error(str(exc))
        return 0
    try:
        config = configuration()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error("Cannot read academy.json: {}".format(exc))
    if args.mode == "hosted":
        if not config.get("hostedUrl"):
            parser.error("This copy has no published Site yet. Run locally, or follow docs/NEW-ACCOUNT.md "
                         "to create a Site in your current OpenAI account.")
        print("Hosted academy: " + config["hostedUrl"], flush=True)
        print("Sign in with an account authorized for this private Site. No local server is started.", flush=True)
        if not args.no_browser:
            open_browser(config["hostedUrl"])
        return 0

    dist = ROOT / "dist"
    data_dir = args.data_dir.expanduser().resolve()
    try:
        data_dir.relative_to(dist.resolve())
    except ValueError:
        pass
    else:
        parser.error("--data-dir must be outside dist/ so private progress is never published.")
    builder = ROOT / "scripts" / "build_portal.py"
    # Source clones/ZIPs rebuild on launch. The portable ZIP already contains dist.
    if builder.is_file() and not args.no_build:
        print("Building the local academy from this copy's sources…", flush=True)
        try:
            subprocess.run([sys.executable, str(builder)], cwd=str(ROOT), check=True)
        except subprocess.CalledProcessError:
            parser.error("Build failed; server was not started. Fix the reported error and retry.")
    required = ("index.html", "app.js", "tracks.js", "style.css", "data.js")
    if dist.is_symlink() or not all((dist / name).is_file() for name in required):
        parser.error("Built portal is missing or incomplete. Run without --no-build in the source copy, "
                     "or extract the complete portable ZIP, including dist/.")
    handler = partial(AcademyHandler, directory=str(dist))
    try:
        server = AcademyServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        parser.error("Cannot start local server: {}. Try --port 8766.".format(exc))
    try:
        server.database = ProgressDatabase(data_dir / "progress.sqlite3")
    except (OSError, sqlite3.Error, ValueError) as exc:
        server.server_close()
        parser.error(str(exc))
    url = "http://127.0.0.1:{}/".format(args.port)
    print("Local academy: " + url, flush=True)
    print("No OpenAI login required. Keep this terminal open; stop with Ctrl+C.", flush=True)
    print("Local progress database: " + str(server.database.path), flush=True)
    print("Progress persists across restarts and ports. Back up with: python3 academy.py backup --output NEW.sqlite3", flush=True)
    try:
        if not args.no_browser:
            open_browser(url)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
