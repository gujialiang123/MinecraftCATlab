#!/usr/bin/env python3
"""Build a deterministic Prism-compatible server list from server.properties."""
import gzip
import struct
from pathlib import Path

root = Path(__file__).resolve().parents[1]
properties = dict(line.split('=', 1) for line in (root / 'server/server.properties').read_text().splitlines() if '=' in line and not line.startswith('#'))
address = f"{properties['server-ip']}:{properties['server-port']}"

def nbt_string(value):
    raw = value.encode('utf-8')
    return struct.pack('>H', len(raw)) + raw

def string_tag(name, value):
    return b'\x08' + nbt_string(name) + nbt_string(value)

server = string_tag('name', 'JialiangCraft') + string_tag('ip', address) + b'\x00'
payload = b'\x0a\x00\x00' + b'\x09' + nbt_string('servers') + b'\x0a' + struct.pack('>i', 1) + server + b'\x00'
(root / 'pack/servers.dat').write_bytes(gzip.compress(payload, mtime=0))
print(address)
