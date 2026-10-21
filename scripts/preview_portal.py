"""Maintainer static preview: no SQLite API, browser storage only, loopback only."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

class PreviewServer(ThreadingHTTPServer):
    request_queue_size = 128

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8793)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('Port must be between 1 and 65535')
    root = Path(__file__).resolve().parents[1]/'dist'
    if not (root/'index.html').is_file():
        parser.error('Build the portal first')
    server = PreviewServer(('127.0.0.1', args.port), partial(SimpleHTTPRequestHandler, directory=str(root)))
    print('Static browser-storage preview: http://127.0.0.1:'+str(args.port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
