#!/usr/bin/env python3
import gzip
import json
import sys
import zipfile
from pathlib import Path

path = sys.argv[1]
with zipfile.ZipFile(path) as archive:
    manifest = json.loads(archive.read('modrinth.index.json'))
    assert manifest['dependencies']['minecraft'] == '1.21.1'
    assert manifest['dependencies']['neoforge'] == '21.1.252'
    files = manifest['files']
    assert len(files) >= 20, len(files)
    assert any(f['env'].get('client') == 'unsupported' for f in files)
    assert any(f['env'].get('server') == 'unsupported' for f in files)
    assert 'overrides/servers.dat' in archive.namelist()
    expected_address = (Path(__file__).resolve().parents[1] / 'server/public-address.txt').read_text().strip().encode()
    assert expected_address in gzip.decompress(archive.read('overrides/servers.dat'))
    assert 'overrides/config/voicechat/voicechat-server.properties' in archive.namelist()
    assert 'scaled_add_xp_cost(distance, 0.02)' in archive.read('overrides/config/waystones-common.toml').decode()
    print(f'Valid .mrpack: {len(files)} pinned files, server list and config included')
