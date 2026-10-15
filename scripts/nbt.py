"""Small read-only NBT reader for inspecting saved vanilla world settings."""
import gzip
import io
import struct


def read_nbt(data):
    stream = io.BytesIO(data)

    def number(fmt):
        size = struct.calcsize(fmt)
        raw = stream.read(size)
        if len(raw) != size:
            raise ValueError('Truncated NBT data')
        return struct.unpack(fmt, raw)[0]

    def string():
        length = number('>H')
        raw = stream.read(length)
        if len(raw) != length:
            raise ValueError('Truncated NBT string')
        return raw.decode('utf-8')

    def length():
        value = number('>i')
        if value < 0:
            raise ValueError('Negative NBT array length')
        return value

    def payload(kind):
        numeric = {1: '>b', 2: '>h', 3: '>i', 4: '>q', 5: '>f', 6: '>d'}
        if kind in numeric:
            return number(numeric[kind])
        if kind == 7:
            size = length()
            value = stream.read(size)
            if len(value) != size:
                raise ValueError('Truncated NBT byte array')
            return value
        if kind == 8:
            return string()
        if kind == 9:
            child = number('>B')
            return [payload(child) for _ in range(length())]
        if kind == 10:
            value = {}
            while True:
                child = number('>B')
                if child == 0:
                    return value
                name = string()
                value[name] = payload(child)
        if kind in (11, 12):
            fmt = '>i' if kind == 11 else '>q'
            return [number(fmt) for _ in range(length())]
        raise ValueError(f'Unsupported NBT tag {kind}')

    kind = number('>B')
    string()
    return payload(kind)


def read_gzip(path):
    with gzip.open(path, 'rb') as source:
        return read_nbt(source.read())
