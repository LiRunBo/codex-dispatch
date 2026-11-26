"""Discover existing global skills without changing them."""
import argparse
import json
import os
from pathlib import Path
import re
import sys

SELF = Path(__file__).resolve().parents[1]

def roots(explicit=()):
    # Installed beside the user's global skills; optional extra roots are explicit.
    candidates = [*explicit, *os.environ.get('CODEX_DISPATCH_SKILL_ROOTS', '').split(os.pathsep), str(SELF.parent)]
    result = []
    for value in candidates:
        if not value:
            continue
        p = Path(value).expanduser().resolve()
        if p.is_dir() and p not in result:
            result.append(p)
    return result

def discover(search_roots):
    found = {}
    for root in search_roots:
        for directory in sorted(Path(root).iterdir()):
            try:
                path = directory.resolve()
                if not directory.is_dir() or path == SELF:
                    continue
                md = path / 'SKILL.md'
                if not md.is_file():
                    continue
                with md.open(encoding='utf-8') as handle:
                    text = handle.read(65536)
                header = re.match(r'^---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S)
                name = re.search(r'^name:\s*([^\n]+)$', header.group(1), re.M) if header else None
                if not name:
                    continue
                canonical = name.group(1).strip().strip('"\'')
                if not canonical or canonical == 'codex-dispatch':
                    continue
                found[str(path)] = {'name':canonical, 'folder':directory.name, 'path':str(path)}
            except (OSError, UnicodeError):
                continue
    return sorted(found.values(), key=lambda item:(item['name'], item['path']))

def resolve(names, inventory):
    output = []
    for name in names:
        matches = [item for item in inventory if name.casefold() in (item['name'].casefold(), item['folder'].casefold())]
        if len(matches) != 1:
            raise ValueError(f'{name}: ' + ('not found' if not matches else 'ambiguous: ' + ', '.join(item['path'] for item in matches)))
        if matches[0]['path'] not in output:
            output.append(matches[0]['path'])
    return output

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', action='append', default=[])
    p.add_argument('names', nargs='*')
    args = p.parse_args()
    try:
        inventory = discover(roots(args.root))
        print(json.dumps(resolve(args.names, inventory) if args.names else inventory, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
