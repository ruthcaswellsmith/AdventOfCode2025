from __future__ import annotations

from utils import read_file
from typing import List, Tuple, Union

from functools import lru_cache


class Manifold:
    def __init__(self, data: List[str]):
        self.shape = (len(data), len(data[0]))
        self.beams = {(0, data[0].index('S'))}
        self.splitters = [(j, i) for j, line in enumerate(data)
                          for i, e in enumerate(line) if e == '^']
        self.splits = 0

    def split_beam(self):
        i = 0
        while i < self.shape[0]:
            i += 1
            new_beams = set()
            for beam in self.beams:
                if (beam[0]+1, beam[1]) in self.splitters:
                    self.splits += 1
                    [new_beams.add(
                        (beam[0] + 1, beam[1] + j)) for j in [-1, 1]]
                else:
                    new_beams.add((beam[0] + 1, beam[1]))
            self.beams = new_beams.copy()


class GraphNode:
    def __init__(self, id: Tuple[int, int], children: Union[None, List[GraphNode]]):
        self.id = id
        self.children = children

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Graph:
    def __init__(self, data: List[str]):
        self.shape = (len(data), len(data[0]))
        self.root = GraphNode((0, data[0].index('S')), None)
        self.nodes = {self.root.id: self.root}
        self.visited = set()
        self.splitters = [(j, i) for j, line in enumerate(data)
                          for i, e in enumerate(line) if e == '^']
        self._build_graph(self.root)
        self.paths = 0

    def _get_or_create_node(self, id: Tuple[int, int]) -> GraphNode:
        if id not in self.nodes:
            self.nodes[id] = GraphNode(id, None)
        return self.nodes[id]

    def _build_graph(self, node: GraphNode):
        if node.id[0] == self.shape[0] - 1:
            return

        if node.id in self.visited:
            return
        self.visited.add(node.id)

        if (node.id[0] + 1, node.id[1]) in self.splitters:
            node.children = [
                self._get_or_create_node((node.id[0] + 1, node.id[1] + 1)),
                self._get_or_create_node((node.id[0] + 1, node.id[1] - 1)),
            ]
        else:
            node.children = [
                self._get_or_create_node((node.id[0] + 1, node.id[1])),
            ]

        for child in node.children:
            self._build_graph(child)

    @lru_cache
    def count_paths(self, node: GraphNode) -> int:
        if node.id[0] == self.shape[0] - 1:
            return 1

        total = 0
        for child in node.children:
            total += self.count_paths(child)

        return total


if __name__ == '__main__':
    filename = 'input/Day7.txt'
    data = read_file(filename)

    manifold = Manifold(data)
    manifold.split_beam()
    print(f"The answer to Part 1 is {manifold.splits}.")

    graph = Graph(data)
    print(f"The answer to Part 2 is {graph.count_paths(graph.root)}.")
