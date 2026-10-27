"""Build the dependency-free academy portal from the editable course sources."""
import json
import shutil
import re
import subprocess
import sys
from pathlib import Path
from package_project import excluded_path
from build_subject_catalog import build_catalog

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
DOWNLOAD_SUFFIXES = {'.py', '.json', '.txt', '.toml', '.yaml', '.yml', '.lock'}
EXCLUDED_PARTS = {'runs', '__pycache__', '.venv', 'node_modules'}

def downloadable_assets():
    """Build an explicit allowlist from the distributed teaching sources."""
    return sorted(
        p.relative_to(ROOT).as_posix()
        for folder in ('content', 'lab')
        for p in (ROOT / folder).rglob('*')
        if p.is_file() and p.suffix in DOWNLOAD_SUFFIXES
        and p.relative_to(ROOT).as_posix() != 'content/incidents.json'
        and not excluded_path(p.relative_to(ROOT))
        and not any(part in EXCLUDED_PARTS for part in p.relative_to(ROOT).parts)
        and not p.is_symlink()
    )

def build():
    build_catalog(ROOT)
    OUT.mkdir(exist_ok=True)
    curriculum = json.loads((ROOT/'content/curriculum.json').read_text())
    resources = json.loads((ROOT/'content/resources.json').read_text())
    docs = {}
    for folder in ['content', 'docs', 'templates', 'capstones', 'lab']:
        for p in sorted((ROOT/folder).rglob('*.md')):
            if excluded_path(p.relative_to(ROOT)) or p.is_symlink() or any(
                    part in EXCLUDED_PARTS for part in p.relative_to(ROOT).parts):
                continue
            text = p.read_text()
            title = next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')), p.stem)
            path = p.relative_to(ROOT).as_posix()
            docs[path] = {'title': title, 'text': text, 'words': len(text.split())}
    docs['README.md'] = {'title':'Project README','text':(ROOT/'README.md').read_text()}
    if (ROOT/'AGENTS.md').is_file():
        docs['AGENTS.md'] = {'title':'Shared assistant instructions','text':(ROOT/'AGENTS.md').read_text()}
    if (ROOT/'CLAUDE.md').is_file():
        docs['CLAUDE.md'] = {'title':'Claude project instructions','text':(ROOT/'CLAUDE.md').read_text()}
    assets = downloadable_assets()
    learning = json.loads((ROOT/'content/learning.json').read_text())
    incidents = json.loads((ROOT/'content/incidents.json').read_text())
    runtime = json.loads((ROOT/'academy.json').read_text())
    guide = json.loads((ROOT/'content/sdet-path.json').read_text())
    course = sorted([item for p in sorted((ROOT/'content/how-to').glob('map-*.json'))
                     for item in json.loads(p.read_text())], key=lambda item: item['lesson'])
    tracks = sorted([track for p in sorted((ROOT/'content/tracks').glob('catalog-*.json')) for track in json.loads(p.read_text())], key=lambda t: t['order'])
    paths = json.loads((ROOT/'content/tracks/paths.json').read_text())
    data = {'tracks':tracks,'paths':paths,'course':course,'guide':guide,'curriculum':curriculum,'learning':learning,'incidents':incidents,'runtime':runtime,'resources':resources,'documents':docs,'assets':assets,'edition':'October 2026','built':'2026-10-21'}
    for name in ['index.html','style.css','theme.js','tracks.js','app.js']:
        shutil.copyfile(ROOT/'portal'/name,OUT/name)
    (OUT/'data.js').write_text('window.ACADEMY = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n')
    def ignore_private(directory, names):
        return [name for name in names if (
            name == 'incidents.json'
            or excluded_path((Path(directory) / name).relative_to(ROOT))
            or (Path(directory) / name).is_symlink()
        )]
    for directory in ['content','docs','templates','capstones']:
        shutil.copytree(ROOT/directory,OUT/directory,dirs_exist_ok=True,
                        ignore=ignore_private)
    # Metadata includes opt-in guidance: do not offer it as a casual learner download.
    # The editable source ZIP still contains it; this is pedagogy, not access control.
    (OUT/'content/incidents.json').unlink(missing_ok=True)
    for relative in assets:
        destination = OUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    if (ROOT/'output/pdf/ai-engineering-fieldbook.pdf').exists():
        shutil.copyfile(ROOT/'output/pdf/ai-engineering-fieldbook.pdf',OUT/'fieldbook.pdf')
    subprocess.run([sys.executable, str(ROOT/'scripts/package_project.py')], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/package_portable.py')], check=True)
    print(f'Built {len(curriculum["lessons"])} lessons, {len(resources)} resources, {len(docs)} documents in {OUT}')

if __name__ == '__main__':
    build()
