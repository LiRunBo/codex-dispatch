import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from skill_resolver import discover, resolve

class TestResolver(unittest.TestCase):
    def add(self, root, folder, name):
        p = Path(root) / folder
        p.mkdir()
        (p / 'SKILL.md').write_text(f'---\nname: {name}\n---\nBody', encoding='utf-8')
        return str(p.resolve())
    def test_find(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.add(d, 'review', 'peer-review')
            self.assertEqual(resolve(['peer-review'], discover([d])), [path])
    def test_ambiguous(self):
        with tempfile.TemporaryDirectory() as d:
            self.add(d, 'a', 'review')
            self.add(d, 'b', 'review')
            with self.assertRaises(ValueError):
                resolve(['review'], discover([d]))
    def test_missing(self):
        with self.assertRaises(ValueError):
            resolve(['unknown'], [])
    def test_exclude_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            self.add(d, 'copy', 'codex-dispatch')
            self.assertEqual(discover([d]), [])
    def test_multiple(self):
        with tempfile.TemporaryDirectory() as d:
            a = self.add(d, 'a', 'review')
            b = self.add(d, 'b', 'plot')
            self.assertEqual(resolve(['review','plot','review'], discover([d])), [a,b])
