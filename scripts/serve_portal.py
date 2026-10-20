"""Serve a built academy locally without an OpenAI account."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    # Works as scripts/serve_portal.py in the source or serve.py in a portable bundle.
    here = Path(__file__).resolve().parent
    root = here.parent if here.name == "scripts" else here
    dist = root / "dist"
    if not (dist / "index.html").is_file():
        parser.error("Built portal missing. Run python3 scripts/build_portal.py first.")
    handler = partial(SimpleHTTPRequestHandler, directory=str(dist))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        parser.error("Cannot start local server: {}. Try --port 8766.".format(exc))
    print("Academy: http://127.0.0.1:{}/".format(args.port), flush=True)
    print("Local files only. Leave this terminal open; stop with Ctrl+C.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
