"""Generate the offline subject/path index from the same metadata as the portal."""
import json
from pathlib import Path

def build_catalog(root):
    tracks = sorted([t for p in (root/'content/tracks').glob('catalog-*.json')
                     for t in json.loads(p.read_text())], key=lambda t: t['order'])
    paths = json.loads((root/'content/tracks/paths.json').read_text())
    topics = {t['id']: t for track in tracks for t in track['lessons']}
    lines = ['# Complete subject and learning-path catalog', '',
             'This index is generated from the same metadata as the portal. Start with '
             '[Start from zero](START-HERE.md) or choose a subject below. '
             'Every original lesson remains available; the [original map](ORIGINAL-LESSON-MAP.md) '
             'preserves its previous order.', '']
    for track in tracks:
        lines += ['## '+track['title'], '', track['summary'], '',
                  'Helpful first: '+(', '.join(next(t['title'] for t in tracks if t['id']==p)
                                              for p in track['prerequisites']) or 'No previous AI knowledge.'), '']
        for topic in track['lessons']:
            lines += ['- **'+topic['level'].capitalize()+'** · ['+topic['title']+'](../'+topic['file']+') — '+topic['summary']]
        lines += ['']
    lines += ['## Curated paths', '', 'These paths select topics across subjects. Prerequisites describe the starting point, not a grading gate.', '']
    for path in paths:
        lines += ['### '+path['title'], '', path['summary'], '', '**Before this:** '+path['prerequisite'], '']
        for i, name in enumerate(path['topics']):
            t=topics[name]
            lines += [str(i+1)+'. ['+t['title']+'](../'+t['file']+')']
        lines += ['', '**Afterward:** '+path['after'], '']
    (root/'docs/SUBJECT-CATALOG.md').write_text('\n'.join(lines)+'\n')

if __name__ == '__main__':
    build_catalog(Path(__file__).resolve().parents[1])
