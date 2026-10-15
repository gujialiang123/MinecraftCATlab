#!/usr/bin/env python3
"""Reject unsafe or incompatible backups before a live server is stopped."""
import json
from pathlib import Path, PurePosixPath
import sys
import tarfile


def check(archive, data):
    expected = json.loads((data / '.runtime.json').read_text())
    allowed = {'world', 'server.properties', 'whitelist.json', 'ops.json', 'banned-ips.json',
               'banned-players.json', '.runtime.json', 'user_jvm_args.txt', 'eula.txt'}
    with tarfile.open(archive, 'r:gz') as bundle:
        members = bundle.getmembers()
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] not in allowed:
                raise ValueError(f'Unsafe or unexpected archive path: {member.name}')
            if not (member.isfile() or member.isdir()):
                raise ValueError(f'Links and special files are not allowed: {member.name}')
        markers = [member for member in members if member.name == '.runtime.json']
        if len(markers) != 1 or not markers[0].isfile() or markers[0].size > 65536:
            raise ValueError('Backup has no unique vanilla runtime marker; modded/legacy backups cannot be restored here')
        saved = json.load(bundle.extractfile(markers[0]))
        if saved != expected:
            raise ValueError('Backup runtime/version differs from this vanilla server')
        if not any(member.name == 'world/level.dat' and member.isfile() for member in members):
            raise ValueError('Backup has no world/level.dat')
    print(f'Backup is safe and matches vanilla {expected["minecraft"]}')


if __name__ == '__main__':
    try:
        check(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        raise SystemExit(f'Backup refused: {error}')
