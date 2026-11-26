"""Install into a user-confirmed global skills directory; never overwrite."""
import argparse
from pathlib import Path
import shutil
import sys

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('global_skills_dir', type=Path)
    args = p.parse_args()
    root = args.global_skills_dir.expanduser().resolve()
    source = Path(__file__).resolve().parents[1]
    target = root / 'codex-dispatch'
    if not root.is_dir():
        p.error('Provide the existing global skills directory used by your client')
    if target.exists() or target.is_symlink() or source == target or source in target.parents:
        p.error('Target exists or overlaps source; review and update manually')
    # Install only runtime assets; never copy arbitrary checkout files or secrets.
    target.mkdir()
    for name in ('SKILL.md', 'README.md', 'README.zh-CN.md'):
        shutil.copy2(source / name, target / name)
    for folder in ('scripts', 'references', 'workflows'):
        src = source / folder
        dest = target / folder
        dest.mkdir()
        for item in src.iterdir():
            if item.is_file() and not item.is_symlink() and item.suffix in ('.py', '.md'):
                shutil.copy2(item, dest / item.name)
    print(f'Installed: {target}')
    print(f'Run: python "{target / "scripts" / "doctor.py"}"')
    return 0

if __name__ == '__main__':
    sys.exit(main())
