#!/usr/bin/env python3
"""Read saved Overworld chunks near spawn without exposing seeds or players."""
import argparse
import collections
import gzip
import json
import pathlib
import struct
import zlib

from nbt import read_gzip, read_nbt


def block_name(value):
    if isinstance(value, dict):
        return value.get('id', value.get('Name', value.get('')))
    return value


def packed(values, index, bits):
    per_long = 64 // bits
    return ((values[index // per_long] & ((1 << 64) - 1))
            >> ((index % per_long) * bits)) & ((1 << bits) - 1)


def palette_value(container, index, minimum_bits):
    palette = container['palette']
    if len(palette) == 1:
        value = palette[0]
    else:
        bits = max(minimum_bits, (len(palette) - 1).bit_length())
        value = palette[packed(container['data'], index, bits)]
    return block_name(value)


def inspect(world, radius):
    data = read_gzip(world / 'level.dat')['Data']
    spawn = data['spawn']
    if spawn['dimension'] != 'minecraft:overworld':
        raise ValueError('Spawn is not in the Overworld')
    sx, sy, sz = spawn['pos']
    region_dir = world / 'dimensions/minecraft/overworld/region'
    regions = {}
    biomes = collections.Counter()
    ground = collections.Counter()
    heights = []
    tree_chunks = []
    loaded_chunks = 0
    for cz in range(sz // 16 - radius, sz // 16 + radius + 1):
        for cx in range(sx // 16 - radius, sx // 16 + radius + 1):
            key = (cx // 32, cz // 32)
            if key not in regions:
                path = region_dir / f'r.{key[0]}.{key[1]}.mca'
                regions[key] = path.read_bytes() if path.exists() else b''
            raw_region = regions[key]
            if not raw_region:
                continue
            loc = struct.unpack_from('>I', raw_region,
                                     4 * (cx % 32 + (cz % 32) * 32))[0]
            if not loc:
                continue
            offset = (loc >> 8) * 4096
            size = struct.unpack_from('>I', raw_region, offset)[0]
            compression = raw_region[offset + 4]
            payload = raw_region[offset + 5:offset + 4 + size]
            if compression == 2:
                payload = zlib.decompress(payload)
            elif compression == 1:
                payload = gzip.decompress(payload)
            elif compression != 3:
                raise ValueError(f'Unsupported chunk compression {compression}')
            chunk = read_nbt(payload)
            if chunk['Status'] != 'minecraft:full':
                continue
            loaded_chunks += 1
            sections = {section['Y']: section for section in chunk['sections']}
            tree_blocks = set()
            for section in sections.values():
                for item in section['block_states']['palette']:
                    name = block_name(item)
                    if name.endswith(('_log', '_leaves')):
                        tree_blocks.add(name)
            if tree_blocks:
                tree_chunks.append({'chunk': [cx, cz], 'blocks': sorted(tree_blocks)})
            heightmap = chunk['Heightmaps']['MOTION_BLOCKING_NO_LEAVES']
            min_y = chunk['yPos'] * 16
            # Four sample columns per chunk: sample the actual surface, avoiding
            # cave palettes and placeholder biomes from ungenerated sections.
            for x, z in ((2, 2), (2, 10), (10, 2), (10, 10)):
                y = min_y + packed(heightmap, z * 16 + x, 9) - 1
                heights.append(y)
                section = sections.get(y // 16)
                if section is None:
                    continue
                biomes[palette_value(section['biomes'],
                                     x // 4 + (z // 4) * 4 + ((y % 16) // 4) * 16, 1)] += 1
                ground[palette_value(section['block_states'],
                                     x + z * 16 + (y % 16) * 256, 4)] += 1
    return {'spawn': [sx, sy, sz], 'radius_chunks': radius,
            'full_chunks': loaded_chunks, 'surface_biome_samples': dict(biomes),
            'surface_height_range': [min(heights), max(heights)] if heights else None,
            'surface_block_samples': dict(ground), 'tree_chunks': tree_chunks,
            'grass_and_trees': bool(ground.get('minecraft:grass_block') and tree_chunks)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('world', type=pathlib.Path)
    parser.add_argument('--radius', type=int, default=4)
    args = parser.parse_args()
    if not 0 <= args.radius <= 16:
        parser.error('--radius must be between 0 and 16')
    print(json.dumps(inspect(args.world, args.radius), ensure_ascii=False, indent=2))
