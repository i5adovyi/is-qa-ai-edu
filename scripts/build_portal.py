"""Build the dependency-free academy portal from the editable course sources."""
import json
import shutil
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'

def build():
    OUT.mkdir(exist_ok=True)
    curriculum = json.loads((ROOT/'content/curriculum.json').read_text())
    resources = json.loads((ROOT/'content/resources.json').read_text())
    docs = {}
    for folder in ['content', 'docs', 'templates', 'capstones', 'lab']:
        for p in sorted((ROOT/folder).rglob('*.md')):
            if 'runs' in p.parts:
                continue
            text = p.read_text()
            title = next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')), p.stem)
            path = p.relative_to(ROOT).as_posix()
            docs[path] = {'title': title, 'text': text, 'words': len(text.split())}
    docs['README.md'] = {'title':'Project README','text':(ROOT/'README.md').read_text()}
    data = {'curriculum':curriculum,'resources':resources,'documents':docs,'edition':'October 2026','built':'2026-10-20'}
    for name in ['index.html','style.css','app.js']:
        shutil.copyfile(ROOT/'portal'/name,OUT/name)
    (OUT/'data.js').write_text('window.ACADEMY = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n')
    for directory in ['content','docs','templates','capstones']:
        shutil.copytree(ROOT/directory,OUT/directory,dirs_exist_ok=True)
    if (ROOT/'output/pdf/ai-engineering-fieldbook.pdf').exists():
        shutil.copyfile(ROOT/'output/pdf/ai-engineering-fieldbook.pdf',OUT/'fieldbook.pdf')
    print(f'Built {len(curriculum["lessons"])} lessons, {len(resources)} resources, {len(docs)} documents in {OUT}')

if __name__ == '__main__':
    build()
