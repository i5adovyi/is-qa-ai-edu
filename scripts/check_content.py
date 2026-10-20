"""Check academy metadata, lesson structure, resource URLs and local doc links."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check():
    c=json.loads((ROOT/'content/curriculum.json').read_text());rs=json.loads((ROOT/'content/resources.json').read_text());errors=[]
    def need(ok,message):
        if not ok:errors.append(message)
    need(len(c['lessons'])==24,'Expected 24 lessons');need(len(c['stages'])==8,'Expected 8 stages')
    ids=set()
    for l in c['lessons']:
        need(l['id'] not in ids,'Duplicate lesson ID');ids.add(l['id']);p=ROOT/l['file'];need(p.exists(),f'Missing {p}')
        need(l['stage'] in range(1,9),f'Invalid stage {l["id"]}');q=l['quiz'];need(len(q['options'])==4 and q['answer'] in range(4),f'Invalid quiz {l["id"]}')
        need(l.get('exerciseCount')==3,f'Expected three exercises {l["id"]}')
        if p.exists():need(len(p.read_text().split())>=600,f'Lesson too thin {l["id"]}')
    for n in range(1,9):need(sum(l['stage']==n for l in c['lessons'])==3,f'Stage {n} must have three lessons')
    need(len({r['id'] for r in rs})==len(rs),'Duplicate resource ID')
    for r in rs:
        need(r['url'].startswith('https://'),f'Invalid source URL {r["id"]}');need(r['stage'] in range(1,9),f'Invalid resource stage {r["id"]}')
    for folder in ['docs','templates','capstones','content','lab']:
        for p in (ROOT/folder).rglob('*.md'):
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
                if re.match(r'https?://|#|mailto:',target):continue
                dest=target.split('#')[0]
                need((p.parent/dest).exists(),f'Broken link {p.relative_to(ROOT)} -> {target}')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'Content checks passed: {len(c["lessons"])} lessons, {len(rs)} resources, all local Markdown links resolve.')
if __name__=='__main__':check()
