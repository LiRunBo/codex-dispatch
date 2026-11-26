import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from session_manager import scan_events, load_previous, command, write_status

SID = '0199a213-81c0-7800-8aa1-bbab2a035a53'

class TestSessionManager(unittest.TestCase):
    def test_trace(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'events.jsonl'
            path.write_text(json.dumps({'type':'thread.started','thread_id':SID})+'\ninvalid\n'+json.dumps({'type':'turn.completed'})+'\n')
            result = scan_events(path)
            self.assertEqual(result['session_id'], SID)
            self.assertEqual(result['terminal_event'], 'turn.completed')
            self.assertEqual(result['malformed_events'], 1)
    def test_ambiguous(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'events.jsonl'
            path.write_text('\n'.join(json.dumps({'type':'thread.started','thread_id':s}) for s in [SID,'0199a213-81c0-7800-8aa1-bbab2a035a54']))
            self.assertIsNone(scan_events(path)['session_id'])
            self.assertTrue(scan_events(path)['ambiguous_session'])
    def test_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            run = root / 'run-test'
            run.mkdir()
            write_status(run/'status.json',{'state':'completed','session_id':SID,'workspace':d,'sandbox':'read-only'})
            self.assertEqual(load_previous(root,'run-test',root,'read-only'),SID)
            with self.assertRaises(ValueError):
                load_previous(root,'run-test',root,'workspace-write')
            with self.assertRaises(ValueError):
                load_previous(root,'run-test',root/'other','read-only')
            with self.assertRaises(ValueError):
                load_previous(root,'../escape',root,'read-only')
            write_status(run/'status.json',{'state':'timeout','session_id':SID})
            with self.assertRaises(ValueError):
                load_previous(root,'run-test',root,'read-only')
    def test_command(self):
        fresh = command('codex','read-only','result.md')
        self.assertIn('--json',fresh)
        self.assertIn('--sandbox',fresh)
        resumed = command('codex','read-only','result.md',SID)
        self.assertIn('sandbox_mode="read-only"',resumed)
        self.assertIn(SID,resumed)
        self.assertNotIn('--last',resumed)
    def test_failed_terminal(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'events.jsonl'
            path.write_text('{"type":"turn.completed"}\n{"type":"turn.failed"}\n')
            self.assertEqual(scan_events(path)['terminal_event'],'turn.failed')
