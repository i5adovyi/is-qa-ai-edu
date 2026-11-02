"""Validate learning metadata, actual exercise sections, assets and Markdown anchors."""
import json
import re
from pathlib import Path
from urllib.parse import unquote
try:
    from scripts.check_tracks import validate_tracks
except ModuleNotFoundError:
    from check_tracks import validate_tracks

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
    c = json.loads((root / 'content/curriculum.json').read_text(encoding='utf-8'))
    resources = json.loads((root / 'content/resources.json').read_text(encoding='utf-8'))
    errors = validate_tracks(root)
    def need(ok, message):
        if not ok:
            errors.append(message)
    guide = json.loads((root / 'content/sdet-path.json').read_text(encoding='utf-8'))
    topics = guide.get('topics', [])
    need(guide.get('version') == 1, 'Unknown guided-path version')
    need([t.get('id') for t in topics] == [str(i).zfill(2) for i in range(1, 9)],
         'Guided path must have eight ordered, unique topics')
    for topic in topics:
        name = topic.get('id', '?')
        for key in ('title', 'file', 'phase', 'summary', 'prerequisite', 'takeaway'):
            need(bool(topic.get(key)), 'Missing guide field ' + key + ': ' + name)
        text_path = root / topic['file']
        need(text_path.is_file(), 'Missing guided reading ' + topic['file'])
        if text_path.is_file():
            need(text_path.read_text(encoding='utf-8').startswith('# ' + topic['title'] + '\n'),
                 'Guided topic title differs from its reading: ' + name)
        for resource in [topic['resource']] + topic.get('alternatives', []):
            for key in ('provider', 'title', 'scope', 'access', 'checked', 'verification'):
                need(bool(resource.get(key)), 'Missing selected-source ' + key + ': ' + name)
            need(resource.get('url', '').startswith('https://'), 'Invalid selected URL: ' + name)
        need(bool(topic.get('practice')), 'Guided topic has no link to retained material: ' + name)
        for target in topic.get('practice', []):
            need((root / target).is_file(), 'Missing related practice ' + target)
    course = sorted([entry for p in (root / 'content/how-to').glob('map-*.json')
                     for entry in json.loads(p.read_text(encoding='utf-8'))], key=lambda e: e['lesson'])
    lesson_ids = [str(i).zfill(2) for i in range(1, 25)]
    need([e.get('lesson') for e in course] == lesson_ids,
         'Every one of the 24 lessons needs exactly one beginner guide')
    required = ['Start here', 'The idea in plain language', 'A small example',
                'Try it with Codex or Claude Code', 'What you should see',
                'If it goes wrong', 'Go deeper', 'Optional practice']
    for entry in course:
        name = entry['lesson']
        path = root / entry['file']
        need(path.is_file(), 'Missing beginner guide: ' + name)
        if path.is_file():
            text = path.read_text(encoding='utf-8')
            for heading in required:
                need('## ' + heading + '\n' in text, 'Missing teaching section ' + heading + ': ' + name)
            need('```text' in text, 'Missing copyable assistant prompt: ' + name)
            need('ASSISTANT-QUICKSTART.md' in text, 'Missing assistant orientation: ' + name)
        need(bool(entry.get('keywords')), 'Missing discoverability keywords: ' + name)
        need(len(entry.get('materials', [])) >= 2, 'Missing topic materials: ' + name)
        for target in entry.get('materials', []):
            need((root / target).is_file(), 'Missing topic material ' + target)
        for prerequisite in entry.get('prerequisites', []):
            need(prerequisite in lesson_ids and prerequisite != name, 'Invalid prerequisite: ' + name)
            need(prerequisite < name, 'Reading prerequisite appears later: ' + name)
        for key in ('provider', 'title', 'url', 'scope', 'access', 'checked', 'verification'):
            need(bool(entry.get('resource', {}).get(key)), 'Missing beginner source ' + key + ': ' + name)
        need(entry.get('resource', {}).get('url', '').startswith('https://'), 'Invalid beginner source URL: ' + name)
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
            text = path.read_text(encoding='utf-8')
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
    learning = json.loads((root / 'content/learning.json').read_text(encoding='utf-8'))
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
    incidents = json.loads((root / 'content/incidents.json').read_text(encoding='utf-8'))
    need(incidents.get('version') == 1, 'Unknown incident metadata version')
    cases = incidents.get('incidents', [])
    need({x.get('id') for x in cases} == {
        'INC-01', 'INC-02', 'INC-03', 'INC-04', 'INC-05', 'INC-06', 'INC-CAPSTONE'
    } and len(cases) == 7, 'Expected six unique incidents and one capstone incident')
    for incident in cases:
        name = incident['id']
        for key in ('title', 'placement', 'minutes', 'prerequisites', 'briefPath',
                    'steps', 'deliverables', 'criteria', 'debrief', 'transfer'):
            need(bool(incident.get(key)), 'Missing incident ' + key + ': ' + name)
        need(len(incident.get('hints', [])) == 3 and
             all(isinstance(h, str) and h.strip() for h in incident.get('hints', [])),
             'Expected three progressive incident hints: ' + name)
        brief = root / incident.get('briefPath', '')
        need(brief.is_file(), 'Missing incident brief: ' + name)
        if brief.is_file():
            # Guidance belongs in explicit reveal fields, never in the student brief.
            need(incident.get('debrief', '') not in brief.read_text(encoding='utf-8'),
                 'Incident debrief leaked into brief: ' + name)
        step_ids = [s.get('id') for s in incident.get('steps', [])]
        need(len(step_ids) == len(set(step_ids)), 'Duplicate incident step: ' + name)
    paths = [root / name for name in ('README.md', 'AGENTS.md', 'CLAUDE.md')
             if (root / name).is_file()]
    for folder in ['docs', 'templates', 'capstones', 'content', 'lab']:
        paths.extend((root / folder).rglob('*.md'))
    for path in paths:
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if re.match(r'https?://|mailto:', target):
                continue
            file_part, _, fragment = target.partition('#')
            dest = (path.parent / unquote(file_part)).resolve() if file_part else path.resolve()
            need(dest.is_file(), f'Broken link {path.relative_to(root)} -> {target}')
            if dest.is_file() and fragment and dest.suffix == '.md':
                need(unquote(fragment) in headings(dest.read_text(encoding='utf-8')), f'Broken section {path.relative_to(root)} -> {target}')
    return errors

def check():
    errors = validate(ROOT)
    if errors:
        raise SystemExit('\n'.join(errors))
    catalogs = [t for p in (ROOT/'content/tracks').glob('catalog-*.json') for t in json.loads(p.read_text(encoding='utf-8'))]
    print(f'Subjects validated: {len(catalogs)} tracks, {sum(len(t["lessons"]) for t in catalogs)} topics, curated paths and prerequisite closure.')
    print('Content checks passed: 24 retained lessons, 72 exercise workspaces, applied checks, 15 lab guides, six incidents and a capstone incident, resource metadata, and local file/section links.')

if __name__ == '__main__':
    check()
