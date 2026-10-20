"""Package source only; exclude learner records, runtime artifacts, and credentials."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/academy-source.zip'
INCLUDE=['README.md','.gitignore','.gitattributes','docs','content','templates','capstones','lab','tests','scripts','portal','output/pdf']
EXCLUDE={'__pycache__','.DS_Store','runs'}
def package():
    OUT.parent.mkdir(exist_ok=True)
    with ZipFile(OUT,'w',ZIP_DEFLATED) as z:
        for name in INCLUDE:
            p=ROOT/name
            if not p.exists():continue
            for f in ([p] if p.is_file() else sorted(p.rglob('*'))):
                if f.is_file() and not any(x in EXCLUDE for x in f.parts) and f.suffix!='.pyc':z.write(f,'ai-engineering-academy/'+f.relative_to(ROOT).as_posix())
    print(f'{OUT} ({OUT.stat().st_size:,} bytes)')
if __name__=='__main__':package()
