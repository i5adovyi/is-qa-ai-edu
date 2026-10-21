"""Curriculum integrity failures must be actionable before publication."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.check_tracks import validate_tracks

ROOT = Path(__file__).resolve().parents[1]

class TrackCatalogTests(unittest.TestCase):
    def mutate(self, change):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'content/tracks').mkdir(parents=True)
            (root/'content/how-to').mkdir()
            tracks = [t for p in (ROOT/'content/tracks').glob('catalog-*.json')
                      for t in json.loads(p.read_text())]
            paths = json.loads((ROOT/'content/tracks/paths.json').read_text())
            change(tracks, paths)
            (root/'content/tracks/catalog-test.json').write_text(json.dumps(tracks))
            (root/'content/tracks/paths.json').write_text(json.dumps(paths))
            for p in (ROOT/'content/how-to').glob('map-*.json'):
                (root/'content/how-to'/p.name).write_text(p.read_text())
            # Test navigation errors independently of article availability.
            return validate_tracks(root)

    def test_complete_catalog(self):
        self.assertEqual(validate_tracks(ROOT), [])

    def test_missing_original_mapping(self):
        def change(tracks, paths):
            next(t for x in tracks for t in x['lessons'] if t.get('lesson'))['lesson'] = '99'
        self.assertIn('Every original lesson must appear exactly once in the subject catalog', self.mutate(change))

    def test_unknown_path_destination(self):
        errors = self.mutate(lambda tracks, paths: paths[0]['topics'].append('missing-topic'))
        self.assertTrue(any('Unknown or empty learning path topic' in e for e in errors))

    def test_missing_prerequisite_in_path(self):
        def change(tracks, paths):
            route = next(p for p in paths if p['id'] == 'zero')
            route['topics'].remove('foundations-tokens')
        self.assertTrue(any('Path skips a declared prerequisite' in e for e in self.mutate(change)))

    def test_prerequisite_cycle(self):
        def change(tracks, paths):
            tracks[0]['prerequisites'] = [tracks[1]['id']]
            tracks[1]['prerequisites'] = [tracks[0]['id']]
        self.assertIn('Subject prerequisite cycle', self.mutate(change))

    def test_backwards_topic_prerequisite(self):
        def change(tracks, paths):
            tracks[0]['lessons'][0]['prerequisites'] = [tracks[0]['lessons'][-1]['id']]
        self.assertTrue(any('must precede' in e for e in self.mutate(change)))

    def test_duplicate_ids_and_level_regression(self):
        def change(tracks, paths):
            tracks[0]['lessons'][1]['id'] = tracks[0]['lessons'][0]['id']
            tracks[0]['lessons'][0]['level'] = 'advanced'
        errors = self.mutate(change)
        self.assertIn('Duplicate topic ID', errors)
        self.assertTrue(any('Levels out of order' in e for e in errors))

if __name__ == '__main__':
    unittest.main()
