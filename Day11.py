from __future__ import annotations

from typing import List
from enum import Enum

from utils import read_file


class SpecialNode(Enum):
    DAC = 'dac'
    FFT = 'fft'

    def opposite(self) -> SpecialNode:
        return SpecialNode.FFT if self == SpecialNode.DAC else SpecialNode.DAC


class PathCounts:
    def __init__(self):
        self.d = {SpecialNode.FFT.value: 0, SpecialNode.DAC.value: 0, 'both': 0, 'neither': 0}

    def __add__(self, other: PathCounts):
        result = PathCounts()
        result.d = {k: self.d[k] + other.d[k] for k in self.d.keys()}
        return result

    @property
    def total_paths(self) -> int:
        return sum(self.d.values())

    @property
    def total_paths_with_dac_and_fft(self) -> int:
        return self.d['both']

    def update(self, node: str):
        result = PathCounts()
        if node in [e.value for e in SpecialNode]:
            special_node = SpecialNode(node)
            opp = special_node.opposite().value
            result.d[node] = self.d['neither']
            result.d['neither'] = 0
            result.d['both'] = self.d[opp]
            result.d[opp] = 0
        elif node == 'out':
            result.d['neither'] = 1
        else:
            result.d = self.d.copy()
        return result


class Devices:
    def __init__(self, data: List[str]):
        self.devices = {}
        for line in data:
            pts = line.split(":")
            self.devices[pts[0]] = pts[1].strip().split(' ')
        self.cache = {}

    def clear_cache(self):
        self.cache = {}

    def find_paths(self, node: str, path: List[str], visited: set):
        if node == "out":
            return PathCounts().update('out')

        if node in self.cache:
            return self.cache[node]

        visited.add(node)

        path_counts = sum([
            self.find_paths(c, path + [c], visited.copy()) for c in self.devices[node] if c not in visited
        ], PathCounts())

        visited.remove(node)
        path_counts = path_counts.update(node)
        self.cache[node] = path_counts

        return path_counts


if __name__ == '__main__':
    filename = 'input/Day11.txt'
    data = read_file(filename)

    devices = Devices(data)
    res = devices.find_paths('you', [], set())
    print(f"The answer to Part 1 is {res.total_paths}.")

    devices.clear_cache()
    res = devices.find_paths('svr', [], set())
    print(f"The answer to Part 2 is {res.total_paths_with_dac_and_fft}.")
