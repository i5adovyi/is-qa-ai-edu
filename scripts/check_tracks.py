"""Validate subject coverage, navigation integrity, and beginner teaching contracts."""
import json
from collections import Counter
from pathlib import Path

REQUIRED_TRACKS = {'foundations', 'assistants', 'prompting', 'context', 'retrieval',
                   'tools', 'mcp', 'skills', 'agentic', 'harness', 'evaluation',
                   'multiagent', 'security', 'production'}
HEADINGS = ['Start here', 'The idea in plain language', 'A small example',
            'Try it with Codex or Claude Code', 'What you should see',
            'If it goes wrong', 'Go deeper', 'Optional practice']
LEVELS = ['beginner', 'intermediate', 'advanced']

def validate_tracks(root):
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
    try:
        tracks = sorted([t for p in (root/'content/tracks').glob('catalog-*.json')
                         for t in json.loads(p.read_text())], key=lambda t: t['order'])
        paths = json.loads((root/'content/tracks/paths.json').read_text())
    except (OSError, ValueError, KeyError, TypeError) as error:
        return ['Invalid track catalog: ' + str(error)]
    ids = [t['id'] for t in tracks]
    need(REQUIRED_TRACKS.issubset(ids), 'Missing required subject tracks')
    need(len(ids) == len(set(ids)), 'Duplicate subject ID')
    need(len({t['order'] for t in tracks}) == len(tracks), 'Duplicate subject order')
    topics = [topic for track in tracks for topic in track['lessons']]
    topic_ids = [t['id'] for t in topics]
    need(len(topic_ids) == len(set(topic_ids)), 'Duplicate topic ID')
    retained = Counter(t['lesson'] for t in topics if t.get('lesson'))
    need(retained == Counter(str(i).zfill(2) for i in range(1, 25)),
         'Every original lesson must appear exactly once in the subject catalog')
    originals = {t['lesson']: t for p in (root/'content/how-to').glob('map-*.json')
                 for t in json.loads(p.read_text())}
    for track in tracks:
        label = track['id']
        for key in ('title', 'summary', 'why', 'outcomes'):
            need(bool(track.get(key)), f'Missing track {key}: {label}')
        need(all(p in ids and p != label for p in track['prerequisites']),
             f'Unknown/self track prerequisite: {label}')
        sequence = track['lessons']
        levels = [t.get('level') for t in sequence]
        need(set(levels) == set(LEVELS), f'Incomplete level coverage: {label}')
        need(levels == sorted(levels, key=lambda x: LEVELS.index(x) if x in LEVELS else -1),
             f'Levels out of order: {label}')
        prior = set()
        for topic in sequence:
            name = topic['id']
            for key in ('title', 'summary', 'file', 'keywords'):
                need(bool(topic.get(key)), f'Missing topic {key}: {name}')
            need(type(topic.get('minutes')) is int and topic['minutes'] > 0,
                 f'Invalid time estimate: {name}')
            need(set(topic.get('prerequisites', [])).issubset(prior),
                 f'Topic prerequisite must precede it in its track: {name}')
            prior.add(name)
            file = root/topic['file']
            need(file.is_file(), f'Missing subject reading: {name}')
            for material in topic.get('materials', []):
                need((root/material).is_file(), f'Missing related material: {name}: {material}')
            if topic.get('lesson'):
                need(topic['file'] == originals.get(topic['lesson'], {}).get('file'),
                     f'Retained lesson must use its existing beginner guide: {name}')
                continue
            if file.is_file():
                text = file.read_text()
                need(text.startswith('# '+topic['title']+'\n'), f'Topic title mismatch: {name}')
                need(len(text.split()) >= 450, f'Subject reading too thin: {name}')
                for heading in HEADINGS:
                    need('## '+heading+'\n' in text, f'Missing {heading}: {name}')
                need('```text\n' in text, f'Missing copyable assistant prompt: {name}')
                need('ASSISTANT-QUICKSTART.md' in text, f'Missing assistant how-to: {name}')
            resource = topic.get('resource', {})
            for key in ('title', 'provider', 'scope', 'access', 'checked', 'verification'):
                need(bool(resource.get(key)), f'Missing selected source {key}: {name}')
            need(resource.get('url', '').startswith('https://'), f'Invalid selected source: {name}')
    # Reject prerequisite cycles before a learner encounters an impossible route.
    graph = {t['id']: t['prerequisites'] for t in tracks}
    def visit(node, active, seen):
        if node in active:
            return False
        if node in seen:
            return True
        active.add(node)
        if not all(visit(p, active, seen) for p in graph.get(node, [])):
            return False
        active.remove(node)
        seen.add(node)
        return True
    need(all(visit(node, set(), set()) for node in graph), 'Subject prerequisite cycle')
    need(len({p['id'] for p in paths}) == len(paths), 'Duplicate learning path ID')
    need(any(p['id'] == 'zero' for p in paths), 'Missing start-from-zero path')
    path_map = {p['id']: p for p in paths}
    def inherited(path_id, active=None):
        active = set() if active is None else set(active)
        if path_id in active or path_id not in path_map:
            errors.append('Unknown or cyclic prerequisite path: ' + path_id)
            return set()
        active.add(path_id)
        path = path_map[path_id]
        result = set(path['topics'])
        for prior in path.get('requires', []):
            result.update(inherited(prior, active))
        return result
    for path in paths:
        available = set()
        for prior in path.get('requires', []):
            available.update(inherited(prior, {path['id']}))
        for topic_id in path['topics']:
            topic = next((t for t in topics if t['id'] == topic_id), None)
            if topic:
                need(set(topic.get('prerequisites', [])).issubset(available),
                     f'Path skips a declared prerequisite: {path["id"]}: {topic_id}')
            available.add(topic_id)
        for key in ('title', 'audience', 'summary', 'prerequisite', 'outcome', 'after'):
            need(bool(path.get(key)), f'Missing path {key}: {path["id"]}')
        need(bool(path['topics']) and set(path['topics']).issubset(topic_ids),
             f'Unknown or empty learning path topic: {path["id"]}')
        need(len(path['topics']) == len(set(path['topics'])), f'Duplicate path step: {path["id"]}')
        positions = {topic: i for i, topic in enumerate(path['topics'])}
        for topic in topics:
            if topic['id'] in positions:
                need(all(positions.get(p, -1) < positions[topic['id']] for p in topic.get('prerequisites', [])),
                     f'Path reverses topic prerequisites: {path["id"]}: {topic["id"]}')
    return errors

if __name__ == '__main__':
    result = validate_tracks(Path(__file__).resolve().parents[1])
    print('\n'.join(result) if result else 'Subject tracks and learning paths validated')
    raise SystemExit(bool(result))
