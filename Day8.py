from __future__ import annotations

from utils import read_file, XYZ
from typing import List
import heapq

import numpy as np


class Circuits:
    def __init__(self, data: List[str]):
        self.junction_boxes = [XYZ(tuple(map(int, line.split(',')))) for line in data]
        self.distances = self._find_distances()
        self.connections = 0
        self.circuits = []

    @property
    def circuits_by_length(self):
        return sorted([len(c) for c in self.circuits], reverse=True)

    def _find_distances(self):
        distances = []
        for i, j1 in enumerate(self.junction_boxes):
            for j2 in self.junction_boxes[i + 1:]:
                heapq.heappush(distances, (j1.euclidean(j2), j1.id, j2.id))
        return distances

    def process_pt1(self, n: int):
        while self.connections < n:
            self.connections += 1
            dist, j1, j2 = heapq.heappop(self.distances)
            self.connect_boxes(j1, j2)
        return np.prod(circuits.circuits_by_length[:3])

    def process_pt2(self):
        while len(self.junction_boxes) > 0:
            dist, j1, j2 = heapq.heappop(self.distances)
            self.connect_boxes(j1, j2)
        return int(j1.split('-')[0]) * int(j2.split('-')[0])

    def remove_box(self, j: str):
        for e in self.junction_boxes:
            if e.id == j:
                self.junction_boxes.remove(e)

    def connect_boxes(self, j1: str, j2: str):
        # how many circuits contain j1 or j2?
        circuits_containing = [c for c in self.circuits if j1 in c or j2 in c]

        if not circuits_containing:
            # create a new circuit
            self.circuits.append({j1, j2})
            for j in [j1, j2]:
                self.remove_box(j)
        elif len(circuits_containing) == 1:
            c = circuits_containing[0]
            # if this circuit contains both do nothing otherwise add to circuit
            if not (j1 in c and j2 in c):
                [c.add(j) for j in [j1, j2]]
                for j in [j1, j2]:
                    self.remove_box(j)
        else:
            # each box is in a different circuit; combine them
            c1, c2 = circuits_containing[0], circuits_containing[1]
            self.circuits[self.circuits.index(c1)] = c1.union(c2)
            self.circuits.remove(c2)


if __name__ == '__main__':
    filename = 'input/Day8.txt'
    data = read_file(filename)

    circuits = Circuits(data)
    print(f"The answer to Part 1 is {circuits.process_pt1(1000)}.")
    print(f"The answer to Part 2 is {circuits.process_pt2()}.")
