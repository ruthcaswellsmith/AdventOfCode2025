from __future__ import annotations

from typing import List

from functools import lru_cache

from utils import read_file


class Devices:
    def __init__(self, data: List[str]):
        self.devices = {}
        for line in data:
            pts = line.split(":")
            self.devices[pts[0]] = pts[1].strip().split(' ')

    @lru_cache
    def find_paths(self, node: str, end: str):
        if node == end:
            return 1

        return sum([self.find_paths(c, end) for c in self.devices.get(node, [])])


if __name__ == '__main__':
    filename = 'input/Day11.txt'
    data = read_file(filename)

    devices = Devices(data)
    res = devices.find_paths('you', 'out')
    print(f"The answer to Part 1 is {res}.")

    res = devices.find_paths('svr', 'fft') * devices.find_paths('fft', 'dac') * devices.find_paths('dac', 'out') + \
          devices.find_paths('svr', 'dac') * devices.find_paths('dac', 'fft') * devices.find_paths('fft', 'out')
    print(f"The answer to Part 2 is {res}.")
