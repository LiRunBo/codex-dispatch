"""Read-only preflight for CodexDispatch; no model calls."""
import json
import shutil
import subprocess
import sys
from skill_resolver import roots, discover

def probe(executable, args):
    try:
        p = subprocess.run([executable, *args], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=15)
        return {'exit_code':p.returncode, 'output':(p.stdout + p.stderr).strip()[:1200]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'exit_code':None, 'error':str(e)}

def main():
    executable = shutil.which('codex')
    report = {'python':sys.version.split()[0], 'codex_path':executable, 'skill_roots':[str(p) for p in roots()], 'skills':discover(roots())}
    if executable:
        report['version'] = probe(executable, ['--version'])
        report['login_status'] = probe(executable, ['login', 'status'])
    report['note'] = 'Preflight only; sandbox, network and real delegation need a local smoke test.'
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if executable and report['version']['exit_code'] == 0 and report['login_status']['exit_code'] == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
