"""Package source only; exclude learner records, runtime artifacts, and credentials."""
from pathlib import Path
import sys
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from academy_local import has_symlink, unlinked_files

OUT = ROOT / 'dist/academy-source.zip'
INCLUDE = [
    'README.md', 'AGENTS.md', 'CLAUDE.md', 'academy.py', 'academy_local.py', 'academy.json',
    '.openai/hosting.json', '.gitignore', '.gitattributes', '.github',
    'docs', 'content', 'templates', 'capstones', 'lab', 'tests', 'scripts',
    'portal', 'output/pdf',
]
EXCLUDE = {
    '__pycache__', '.ds_store', 'runs', 'work', '.tmp', 'tmp', '.git',
    '.academy-data', '.codex', '.venv', 'venv', 'node_modules', '.lab-runs',
}


def excluded_path(relative):
    """Runtime data is never a teaching asset, even inside an included folder."""
    relative = Path(relative)
    parts = [part.lower() for part in relative.parts]
    name = relative.name.lower()
    return (
        any(part in EXCLUDE for part in parts)
        or ('.openai' in parts and relative.as_posix() != '.openai/hosting.json')
        or any(part.startswith('.env') and part != '.env.example' for part in parts)
        or name.endswith(('.pyc', '.zip', '.sqlite', '.sqlite3', '.db'))
        or any(marker in name for marker in ('.sqlite-', '.sqlite3-', '.db-'))
        or name.startswith(('academy-progress', 'academy-recovery'))
        or (name.startswith('academy-') and name.endswith('.json') and 'progress' in name)
    )


def source_files(root=ROOT):
    """Yield source files only. Shared with the new-account export command."""
    root = Path(root).resolve()
    for name in INCLUDE:
        for item in sorted(unlinked_files(root / name, root)):
            relative = item.relative_to(root)
            if not excluded_path(relative):
                yield item


def package(root=ROOT, output=None):
    root = Path(root).resolve()
    output = Path(output).absolute() if output else root / 'dist/academy-source.zip'
    if root in output.parents and has_symlink(output, root):
        raise ValueError('Linked source archive destination')
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for item in source_files(root):
            archive.write(item, 'ai-engineering-academy/' + item.relative_to(root).as_posix())
    print(f'{output} ({output.stat().st_size:,} bytes)')


if __name__ == '__main__':
    package()
