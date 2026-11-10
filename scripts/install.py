#!/usr/bin/env python3
"""Link the blackwall command directly to this repository."""
from datetime import datetime
import os
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
source = root / 'bin/blackwall'
home = Path.home()
target = home / '.local/bin/blackwall'
if not source.is_file():
    raise SystemExit('Missing CLI: ' + str(source))
if target.is_symlink() and target.resolve() == source:
    print('Already linked: ' + str(target) + ' → ' + str(source))
else:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup = home / '.config/blackwall/backups' / stamp / 'blackwall-launcher'
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup, follow_symlinks=False)
    temporary = target.with_name('blackwall.install-' + str(os.getpid()))
    try:
        temporary.symlink_to(source)
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
    print('Linked: ' + str(target) + ' → ' + str(source))
