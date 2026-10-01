#!/usr/bin/env python3
"""Install server-side JARs from pinned Packwiz metadata and verify SHA-512."""
import hashlib
import os
import shutil
import sys
import tomllib
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = Path(os.environ.get('JC_DATA_DIR', root.parent / 'jialiangcraft-data'))
mods = data / 'mods'
stage = data / 'mods.staging'
previous = data / 'mods.previous'
if stage.exists():
    shutil.rmtree(stage)
stage.mkdir(parents=True)
count = 0
try:
    for path in sorted((root / 'pack/mods').glob('*.pw.toml')):
        meta = tomllib.loads(path.read_text())
        if meta.get('side') == 'client':
            continue
        download = meta['download']
        if download['hash-format'] != 'sha512':
            raise RuntimeError(f'{path.name}: expected SHA-512')
        filename = Path(meta['filename']).name
        if filename != meta['filename']:
            raise RuntimeError(f'{path.name}: unsafe filename')
        target = stage / filename
        if (mods / filename).exists():
            shutil.copy2(mods / filename, target)
        else:
            request = urllib.request.Request(download['url'], headers={'User-Agent': 'JialiangCraft/1.0.0'})
            with urllib.request.urlopen(request, timeout=90) as source, target.open('wb') as output:
                shutil.copyfileobj(source, output)
        digest = hashlib.sha512(target.read_bytes()).hexdigest()
        if digest != download['hash']:
            raise RuntimeError(f'{filename}: SHA-512 mismatch')
        print(f'Verified {filename}')
        count += 1
    if previous.exists():
        shutil.rmtree(previous)
    if mods.exists():
        mods.rename(previous)
    stage.rename(mods)
    print(f'Installed {count} server mods from Packwiz metadata')
except Exception:
    shutil.rmtree(stage, ignore_errors=True)
    raise
