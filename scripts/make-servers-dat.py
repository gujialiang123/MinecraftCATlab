#!/usr/bin/env python3
"""Build a deterministic Prism-compatible server list for the public relay."""
import gzip
import struct
from pathlib import Path

root = Path(__file__).resolve().parents[1]
address = (root / 'server/public-address.txt').read_text().strip()
if not address or any(char.isspace() for char in address):
    raise ValueError('server/public-address.txt must contain one host:port')

def nbt_string(value):
    raw = value.encode('utf-8')
    return struct.pack('>H', len(raw)) + raw

def string_tag(name, value):
    return b'\x08' + nbt_string(name) + nbt_string(value)

server = string_tag('name', 'JialiangCraft') + string_tag('ip', address) + b'\x00'
payload = b'\x0a\x00\x00' + b'\x09' + nbt_string('servers') + b'\x0a' + struct.pack('>i', 1) + server + b'\x00'
(root / 'pack/servers.dat').write_bytes(gzip.compress(payload, mtime=0))
print(address)
