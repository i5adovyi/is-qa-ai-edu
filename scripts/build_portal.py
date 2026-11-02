"""Build the dependency-free academy portal from the editable course sources."""
import json
import os
import shutil
import re
import subprocess
import sys
from pathlib import Path
from package_project import excluded_path
from academy_local import has_symlink, is_link, unlinked_files
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
        for p in unlinked_files(ROOT / folder, ROOT)
        if p.suffix in DOWNLOAD_SUFFIXES
        and p.relative_to(ROOT).as_posix() != 'content/incidents.json'
        and not excluded_path(p.relative_to(ROOT))
        and not any(part in EXCLUDED_PARTS for part in p.relative_to(ROOT).parts)
    )

def verify_build_paths(root):
    # These inputs are opened directly (rather than copied by the filtered tree walker).
    direct = ['README.md', 'AGENTS.md', 'CLAUDE.md', 'academy.json', 'docs/SUBJECT-CATALOG.md',
              'templates', 'capstones', 'lab', 'content', 'portal', 'output/pdf', 'dist']
    for name in direct:
        if has_symlink(root / name, root):
            raise ValueError('Linked build path: ' + name)
    # Validate curated inputs and every existing output before the first write.
    # In particular, copytree(dirs_exist_ok=True) follows existing destination links.
    for name in ('content', 'portal', 'output/pdf', 'dist'):
        for parent, dirs, files in os.walk(root / name):
            for child in dirs + files:
                item = Path(parent) / child
                if is_link(item):
                    raise ValueError('Linked build path: ' + str(item.relative_to(root)))


def build():
    verify_build_paths(ROOT)
    build_catalog(ROOT)
    OUT.mkdir(exist_ok=True)
    curriculum = json.loads((ROOT/'content/curriculum.json').read_text(encoding='utf-8'))
    resources = json.loads((ROOT/'content/resources.json').read_text(encoding='utf-8'))
    docs = {}
    for folder in ['content', 'docs', 'templates', 'capstones', 'lab']:
        for p in sorted(unlinked_files(ROOT/folder, ROOT)):
            if p.suffix.lower() != '.md' or excluded_path(p.relative_to(ROOT)) or any(
                    part in EXCLUDED_PARTS for part in p.relative_to(ROOT).parts):
                continue
            text = p.read_text(encoding='utf-8')
            title = next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')), p.stem)
            path = p.relative_to(ROOT).as_posix()
            docs[path] = {'title': title, 'text': text, 'words': len(text.split())}
    docs['README.md'] = {'title':'Project README','text':(ROOT/'README.md').read_text(encoding='utf-8')}
    if (ROOT/'AGENTS.md').is_file():
        docs['AGENTS.md'] = {'title':'Shared assistant instructions','text':(ROOT/'AGENTS.md').read_text(encoding='utf-8')}
    if (ROOT/'CLAUDE.md').is_file():
        docs['CLAUDE.md'] = {'title':'Claude project instructions','text':(ROOT/'CLAUDE.md').read_text(encoding='utf-8')}
    assets = downloadable_assets()
    learning = json.loads((ROOT/'content/learning.json').read_text(encoding='utf-8'))
    incidents = json.loads((ROOT/'content/incidents.json').read_text(encoding='utf-8'))
    runtime = json.loads((ROOT/'academy.json').read_text(encoding='utf-8'))
    guide = json.loads((ROOT/'content/sdet-path.json').read_text(encoding='utf-8'))
    course = sorted([item for p in sorted((ROOT/'content/how-to').glob('map-*.json'))
                     for item in json.loads(p.read_text(encoding='utf-8'))], key=lambda item: item['lesson'])
    tracks = sorted([track for p in sorted((ROOT/'content/tracks').glob('catalog-*.json')) for track in json.loads(p.read_text(encoding='utf-8'))], key=lambda t: t['order'])
    paths = json.loads((ROOT/'content/tracks/paths.json').read_text(encoding='utf-8'))
    data = {'tracks':tracks,'paths':paths,'course':course,'guide':guide,'curriculum':curriculum,'learning':learning,'incidents':incidents,'runtime':runtime,'resources':resources,'documents':docs,'assets':assets,'edition':'October 2026','built':'2026-10-21'}
    for name in ['index.html','style.css','theme.js','tracks.js','app.js']:
        shutil.copyfile(ROOT/'portal'/name,OUT/name)
    (OUT/'data.js').write_text('window.ACADEMY = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n', encoding='utf-8')
    def ignore_private(directory, names):
        return [name for name in names if (
            name == 'incidents.json'
            or excluded_path((Path(directory) / name).relative_to(ROOT))
            or is_link(Path(directory) / name)
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
