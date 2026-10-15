#!/usr/bin/env python3
"""Query Java server status; fail if an expected version does not match."""
import argparse
import json
import socket
import struct


def varint(number):
    number &= 0xffffffff
    output = bytearray()
    while True:
        byte = number & 127
        number >>= 7
        output.append(byte | (128 if number else 0))
        if not number:
            return bytes(output)


def receive(connection, length):
    output = bytearray()
    while len(output) < length:
        chunk = connection.recv(length - len(output))
        if not chunk:
            raise EOFError('Server closed the connection')
        output.extend(chunk)
    return bytes(output)


def read_varint(connection):
    value = 0
    for shift in range(0, 35, 7):
        byte = receive(connection, 1)[0]
        value |= (byte & 127) << shift
        if byte & 128 == 0:
            return value
    raise ValueError('Invalid VarInt')


def query(host, port, timeout=3):
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(timeout)
        address = host.encode('utf-8')
        handshake = varint(0) + varint(-1) + varint(len(address)) + address + struct.pack('>H', port) + varint(1)
        connection.sendall(varint(len(handshake)) + handshake + b'\x01\x00')
        packet_size = read_varint(connection)
        if not 0 < packet_size <= 2 * 1024 * 1024:
            raise ValueError('Invalid status packet size')
        if read_varint(connection) != 0:
            raise ValueError('Unexpected status packet')
        size = read_varint(connection)
        if not 0 < size <= packet_size:
            raise ValueError('Invalid status JSON size')
        return json.loads(receive(connection, size))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port', type=int, nargs='?', default=25565)
    parser.add_argument('--expect-version')
    args = parser.parse_args()
    try:
        status = query(args.host, args.port)
        if args.expect_version and status['version']['name'] != args.expect_version:
            raise ValueError(f'Expected {args.expect_version}, got {status["version"]["name"]}')
        print(json.dumps(status, ensure_ascii=False))
    except (OSError, ValueError, EOFError, KeyError) as error:
        parser.exit(1, f'Server status failed: {error}\n')
