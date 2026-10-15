#!/usr/bin/env python3
"""Install the pinned official server into a new or matching vanilla directory."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get('JC_DATA_DIR', ROOT.parent / 'jialiangcraft-vanilla-26.3-data')).resolve()
LOCK = json.loads((ROOT / 'server/vanilla.lock.json').read_text())
JAVA_LOCK = json.loads((ROOT / 'server/java.lock.json').read_text())
JAVA_HOME = ROOT / '.tools/java25'


def download(url, target, algorithm, digest, size=None):
    request = urllib.request.Request(url, headers={'User-Agent': 'JialiangCraft/2.0.0'})
    with urllib.request.urlopen(request, timeout=90) as source, target.open('wb') as output:
        shutil.copyfileobj(source, output)
    if hashlib.new(algorithm, target.read_bytes()).hexdigest() != digest:
        raise RuntimeError(f'Checksum mismatch: {target.name}')
    if size is not None and target.stat().st_size != size:
        raise RuntimeError(f'Size mismatch: {target.name}')


if (DATA / 'run.sh').exists() or (DATA / 'mods').exists():
    raise SystemExit('Refusing to deploy vanilla over a modded server directory')
marker = DATA / '.runtime.json'
if marker.exists():
    if json.loads(marker.read_text()) != LOCK:
        raise SystemExit('Runtime differs; use a separate data directory for another version')
elif (DATA / 'world').exists():
    raise SystemExit('Refusing an existing world without matching vanilla runtime metadata')

JAVA_HOME.parent.mkdir(parents=True, exist_ok=True)
if not JAVA_HOME.exists():
    with tempfile.TemporaryDirectory(dir=JAVA_HOME.parent) as temp:
        temp = Path(temp)
        archive = temp / 'java.tar.gz'
        download(JAVA_LOCK['url'], archive, 'sha256', JAVA_LOCK['sha256'])
        extracted = temp / 'extracted'
        extracted.mkdir()
        with tarfile.open(archive) as bundle:
            bundle.extractall(extracted, filter='data')
        homes = [path for path in extracted.iterdir() if (path / 'bin/java').is_file()]
        if len(homes) != 1:
            raise RuntimeError('Unexpected Java archive layout')
        homes[0].rename(JAVA_HOME)
release = (JAVA_HOME / 'release').read_text()
if f'JAVA_VERSION="{JAVA_LOCK["java_version"]}"' not in release:
    raise SystemExit('Installed isolated Java does not match server/java.lock.json')
subprocess.run([str(JAVA_HOME / 'bin/java'), '-version'], check=True)

DATA.mkdir(parents=True, exist_ok=True)
target = DATA / 'server.jar'
if not target.exists() or hashlib.sha1(target.read_bytes()).hexdigest() != LOCK['server_sha1']:
    temporary = DATA / 'server.jar.part'
    try:
        download(LOCK['server_url'], temporary, 'sha1', LOCK['server_sha1'], LOCK['server_size'])
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
shutil.copy2(ROOT / 'server/server.properties', DATA / 'server.properties')
(DATA / 'eula.txt').write_text('eula=true\n')
(DATA / 'user_jvm_args.txt').write_text('-Xms1G\n-Xmx4G\n-XX:ActiveProcessorCount=4\n-Dfile.encoding=UTF-8\n')
marker.write_text(json.dumps(LOCK, indent=2) + '\n')
print(f'Installed verified official Minecraft {LOCK["minecraft"]} in {DATA}')
