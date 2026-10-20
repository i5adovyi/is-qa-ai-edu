"""Validate learning metadata, actual exercise sections, assets and Markdown anchors."""
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

def headings(text):
    """GitHub-style IDs for ordinary Markdown headings, ignoring fenced code."""
    used = {}
    result = set()
    in_code = False
    for line in text.splitlines():
        if line.startswith('```'):
            in_code = not in_code
            continue
        match = re.match(r'^#{1,6}\s+(.+)', line)
        if in_code or not match:
            continue
        value = re.sub(r'[^\w\- ]', '', match[1].strip().lower()).replace(' ', '-')
        count = used.get(value, 0)
        used[value] = count + 1
        result.add(value + ('-' + str(count) if count else ''))
    return result

def validate(root):
    c = json.loads((root / 'content/curriculum.json').read_text())
    resources = json.loads((root / 'content/resources.json').read_text())
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
    need(len(c['lessons']) == 24, 'Expected 24 lessons')
    need({s['id'] for s in c['stages']} == set(range(1, 9)), 'Expected stages 1 through 8')
    ids = set()
    for lesson in c['lessons']:
        name = lesson['id']
        need(name not in ids, 'Duplicate lesson ID ' + name)
        ids.add(name)
        path = root / lesson['file']
        need(path.is_file(), 'Missing lesson ' + lesson['file'])
        need(lesson['stage'] in range(1, 9), 'Invalid stage ' + name)
        quiz = lesson['quiz']
        need(len(quiz['options']) == 4 and type(quiz['answer']) is int and quiz['answer'] in range(4), 'Invalid quiz ' + name)
        need(bool(quiz.get('explanation', '').strip()), 'Missing quiz explanation ' + name)
        need(type(lesson['minutes']) is int and lesson['minutes'] > 0, 'Invalid duration ' + name)
        if path.is_file():
            text = path.read_text()
            exercises = re.findall(r'^## Exercise ([123])\b', text, re.M)
            need(exercises == ['1', '2', '3'] and lesson.get('exerciseCount') == len(exercises), 'Exercise sections do not match metadata ' + name)
            need(len(text.split()) >= 600, 'Lesson too thin ' + name)
            need('## Hints and solution outline' in text, 'Missing solution guidance ' + name)
    need(ids == {str(i).zfill(2) for i in range(1, 25)}, 'Lesson IDs must be 01 through 24')
    for stage in range(1, 9):
        need(sum(l['stage'] == stage for l in c['lessons']) == 3, 'Expected three lessons in stage ' + str(stage))
    need(len({r['id'] for r in resources}) == len(resources), 'Duplicate resource ID')
    for resource in resources:
        need(resource['url'].startswith('https://'), 'Invalid resource URL ' + resource['id'])
        need(resource['stage'] in range(1, 9), 'Invalid resource stage ' + resource['id'])
    labs = sorted((root / 'content/labs').glob('[0-9][0-9]-*.md'))
    need([p.name[:2] for p in labs] == [str(i).zfill(2) for i in range(1, 16)],
         'Expected fifteen unique numbered lab guides, 01 through 15')
    learning = json.loads((root / 'content/learning.json').read_text())
    exercises = learning['exercises']
    need(len(exercises) == 72, 'Expected 72 exercise workspace records')
    need(len({e['id'] for e in exercises}) == 72, 'Duplicate workspace exercise ID')
    for exercise in exercises:
        need(exercise['lesson'] in ids, 'Unknown exercise lesson')
        need(bool(exercise.get('prompt')) and bool(exercise.get('criteria')), 'Missing exercise contract')
        need(len(exercise.get('hints', [])) == 3, 'Expected three progressive hints')
        need(bool(exercise.get('steps')), 'Missing exercise steps')
    need(len(learning['checks']) >= 72, 'Expected at least 72 applied checks')
    need(len({x['id'] for x in learning['checks']}) == len(learning['checks']), 'Duplicate applied-check ID')
    for key in ('starterLinks', 'transferLinks', 'walkthroughLinks'):
        for exercise in exercises:
            for link in exercise.get(key, []):
                need((root / link['path'].split('#')[0]).is_file(), 'Missing learning asset ' + link['path'])
    paths = [root / 'README.md']
    for folder in ['docs', 'templates', 'capstones', 'content', 'lab']:
        paths.extend((root / folder).rglob('*.md'))
    for path in paths:
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
            if re.match(r'https?://|mailto:', target):
                continue
            file_part, _, fragment = target.partition('#')
            dest = (path.parent / unquote(file_part)).resolve() if file_part else path.resolve()
            need(dest.is_file(), f'Broken link {path.relative_to(root)} -> {target}')
            if dest.is_file() and fragment and dest.suffix == '.md':
                need(unquote(fragment) in headings(dest.read_text()), f'Broken section {path.relative_to(root)} -> {target}')
    return errors

def check():
    errors = validate(ROOT)
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Content checks passed: 24 lessons, 72 exercise workspaces, applied checks, 15 lab guides, resource metadata, and local file/section links.')

if __name__ == '__main__':
    check()
