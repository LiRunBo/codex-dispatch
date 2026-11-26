import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from dispatch import prepare

class TestPrepare(unittest.TestCase):
    def test_default_readonly(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(prepare({'objective':'test','workspace':d})[1], 'read-only')
    def test_bad_sandbox(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                prepare({'objective':'test','workspace':d,'sandbox':'danger-full-access'})
    def test_skill(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'review'; p.mkdir(); (p/'SKILL.md').write_text('review')
            self.assertIn(str(p.resolve()), prepare({'objective':'review','workspace':d,'skills':[str(p)]})[3])
    def test_missing_skill(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                prepare({'objective':'review','workspace':d,'skills':[d]})
    def test_timeout(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                prepare({'objective':'test','workspace':d,'timeout_seconds':0})
