"""Local run records and conservative session continuation."""
import json
from pathlib import Path
import re
import uuid

def valid_id(value):
    if not isinstance(value, str):
        return False
    try:
        return str(uuid.UUID(value)) == value.lower()
    except ValueError:
        return False

def scan_events(path):
    ids = set()
    terminal = None
    malformed = 0
    with Path(path).open(encoding='utf-8', errors='replace') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError()
            except ValueError:
                malformed += 1
                continue
            kind = event.get('type')
            if kind == 'thread.started' and valid_id(event.get('thread_id')):
                ids.add(event['thread_id'].lower())
            if kind in ('turn.completed', 'turn.failed'):
                terminal = kind
    return {'session_id': next(iter(ids)) if len(ids) == 1 else None,
            'terminal_event': terminal, 'malformed_events': malformed,
            'ambiguous_session': len(ids) > 1}

def load_previous(root, run_id, workspace, sandbox):
    if not isinstance(run_id, str) or not re.fullmatch(r'run-[A-Za-z0-9_-]+', run_id):
        raise ValueError('Invalid previous run ID')
    root = Path(root).resolve()
    run = (root / run_id).resolve()
    if run.parent != root:
        raise ValueError('Previous run escapes local run directory')
    status = json.loads((run / 'status.json').read_text(encoding='utf-8'))
    if not isinstance(status, dict):
        raise ValueError('Invalid previous run record')
    if status.get('state') != 'completed' or not valid_id(status.get('session_id')):
        raise ValueError('Only a completed run with a recorded session can be resumed')
    previous_workspace = status.get('workspace')
    if not isinstance(previous_workspace, str) or not Path(previous_workspace).is_absolute() or Path(previous_workspace).resolve() != Path(workspace).resolve():
        raise ValueError('Resume requires the same workspace')
    if status.get('sandbox') != sandbox:
        raise ValueError('Resume requires the same sandbox; start fresh for changed permissions')
    return status['session_id'].lower()

def command(codex, sandbox, result, session=None):
    base = [codex, '-a', 'never', 'exec', '--json', '-o', str(result)]
    if session:
        if not valid_id(session):
            raise ValueError('Invalid session ID')
        # Explicit config is needed because resume flag support differs across versions.
        return base + ['-c', 'sandbox_mode=' + json.dumps(sandbox), 'resume', session, '-']
    return base + ['--sandbox', sandbox, '-']

def write_status(path, status):
    path = Path(path)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)
