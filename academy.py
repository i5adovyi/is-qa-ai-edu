"""Open the hosted academy or build and serve a local copy. Python 3.9+, no packages."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit
import webbrowser
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent


def portable_archive(root):
    """Package only course assets; also works inside an extracted portable copy."""
    root = Path(root)
    dist = root / "dist"
    buffer = BytesIO()
    prefix = "ai-engineering-academy-portable/"
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for item in sorted(dist.rglob("*")):
            if item.is_file() and not item.is_symlink() and item != dist / "academy-portable.zip":
                archive.write(item, prefix + "dist/" + item.relative_to(dist).as_posix())
        for name in ("academy.py", "academy.json"):
            archive.write(root / name, prefix + name)
        legacy = root / "scripts/serve_portal.py"
        if not legacy.is_file():
            legacy = root / "serve.py"
        if legacy.is_file():
            archive.write(legacy, prefix + "serve.py")
        for name in ("CONTINUE-LEARNING.md", "ACCOUNT-MIGRATION.md", "RUN-ANYWHERE.md"):
            source = root / "docs" / name
            if not source.is_file():
                source = root / name
            if source.is_file() and not source.is_symlink():
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
            "Import your separately exported progress JSON on the Progress page.\n"
            "Personal progress, credentials and chat history are NOT in this bundle.\n"
            "External resources need internet; live-model labs need their own access.\n"
            "Editable sources: dist/academy-source.zip. PDF: dist/fieldbook.pdf.\n"
            "Read RUN-ANYWHERE.md, ACCOUNT-MIGRATION.md and CONTINUE-LEARNING.md.\n"
        ))
    buffer.seek(0)
    return buffer


class AcademyHandler(SimpleHTTPRequestHandler):
    def send_head(self):
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
    parser.add_argument("mode", nargs="?", choices=("local", "hosted"), default="local")
    parser.add_argument("--port", type=int, default=8765, help="local port (default: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="print the URL without opening a browser")
    parser.add_argument("--no-build", action="store_true", help="serve existing dist files without rebuilding")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        config = configuration()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error("Cannot read academy.json: {}".format(exc))
    if args.mode == "hosted":
        print("Hosted academy: " + config["hostedUrl"], flush=True)
        print("Sign in with an account authorized for this private Site. No local server is started.", flush=True)
        if not args.no_browser:
            open_browser(config["hostedUrl"])
        return 0

    dist = ROOT / "dist"
    builder = ROOT / "scripts" / "build_portal.py"
    # Source clones/ZIPs rebuild on launch. The portable ZIP already contains dist.
    if builder.is_file() and not args.no_build:
        print("Building the local academy from this copy's sources…", flush=True)
        try:
            subprocess.run([sys.executable, str(builder)], cwd=str(ROOT), check=True)
        except subprocess.CalledProcessError:
            parser.error("Build failed; server was not started. Fix the reported error and retry.")
    required = ("index.html", "app.js", "style.css", "data.js")
    if not all((dist / name).is_file() for name in required):
        parser.error("Built portal is missing or incomplete. Run without --no-build in the source copy, "
                     "or extract the complete portable ZIP, including dist/.")
    handler = partial(AcademyHandler, directory=str(dist))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        parser.error("Cannot start local server: {}. Try --port 8766.".format(exc))
    url = "http://127.0.0.1:{}/".format(args.port)
    print("Local academy: " + url, flush=True)
    print("No OpenAI login required. Keep this terminal open; stop with Ctrl+C.", flush=True)
    print("Keep the same address and port for your saved progress; export/import when switching.", flush=True)
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
