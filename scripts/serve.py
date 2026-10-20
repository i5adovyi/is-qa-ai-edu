"""Serve only built distribution assets, bound to loopback."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from pathlib import Path
import argparse
root = Path(__file__).resolve().parents[1]/'dist'
parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=8765)
args=parser.parse_args()
if not (root/'index.html').exists():
    raise SystemExit('Build first: python3 scripts/build_portal.py')
print(f'Academy: http://127.0.0.1:{args.port}', flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
