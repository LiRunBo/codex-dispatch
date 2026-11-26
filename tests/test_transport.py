import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import dispatch

class TestTransport(unittest.TestCase):
    def simulate(self, event='turn.completed', result='done', code=0):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            manifest = root / 'task.json'
            manifest.write_text(json.dumps({'objective':'test','workspace':d}), encoding='utf-8')
            def fake_run(cmd, **kwargs):
                kwargs['stdout'].write((json.dumps({'type':event})+'\n').encode())
                if result is not None:
                    Path(cmd[cmd.index('-o')+1]).write_text(result, encoding='utf-8')
                return type('Result', (), {'returncode':code})()
            with patch.object(sys,'argv',['dispatch.py',str(manifest)]), patch.object(Path,'home',return_value=root), patch.object(dispatch.shutil,'which',return_value='codex'), patch.object(dispatch.subprocess,'run',side_effect=fake_run):
                exit_code = dispatch.main()
            run = next((root/'.codex-dispatch'/'runs').iterdir())
            return exit_code, json.loads((run/'status.json').read_text())
    def test_success(self):
        code, status = self.simulate()
        self.assertEqual(code,0)
        self.assertEqual(status['state'],'completed')
    def test_empty_result(self):
        code,status = self.simulate(result=' ')
        self.assertNotEqual(code,0)
        self.assertEqual(status['state'],'failed')
    def test_missing_result(self):
        code,status = self.simulate(result=None)
        self.assertNotEqual(code,0)
    def test_failed_event(self):
        code,status = self.simulate(event='turn.failed')
        self.assertNotEqual(code,0)
    def test_nonzero(self):
        code,status = self.simulate(code=5)
        self.assertEqual(code,5)
        self.assertEqual(status['state'],'failed')
    def test_bad_deliverables(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                dispatch.prepare({'objective':'test','workspace':d,'deliverables':'file'})
