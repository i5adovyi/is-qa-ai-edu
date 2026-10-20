"""Package source only; exclude learner records, runtime artifacts, and credentials."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/academy-source.zip'
INCLUDE = [
    'README.md', 'AGENTS.md', 'academy.py', 'academy_local.py', 'academy.json',
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
        path = root / name
        if not path.exists():
            continue
        for item in ([path] if path.is_file() else sorted(path.rglob('*'))):
            relative = item.relative_to(root)
            if excluded_path(relative) or not item.is_file():
                continue
            # A symlinked file or any symlinked ancestor may point at private data.
            if any(part.is_symlink() for part in [item, *item.parents] if part != root):
                continue
            yield item


def package(root=ROOT, output=None):
    root = Path(root).resolve()
    output = Path(output) if output else root / 'dist/academy-source.zip'
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for item in source_files(root):
            archive.write(item, 'ai-engineering-academy/' + item.relative_to(root).as_posix())
    print(f'{output} ({output.stat().st_size:,} bytes)')


if __name__ == '__main__':
    package()
