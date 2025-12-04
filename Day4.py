from utils import read_file
from typing import List

import numpy as np


class Diagram:
    def __init__(self, data: List[str]):
        self.diagram = np.array([[e == '@' for e in line] for line in data], dtype=bool)
        self.shape = np.shape(self.diagram)
        self.padded, self.prefix_sum, self.accessible, self.removed = \
            None, None, np.zeros(self.shape, dtype=bool), 0

    @property
    def total_accessible(self):
        return np.sum(self.accessible)

    def determine_accessible(self):
        self.accessible = np.zeros(self.shape, dtype=bool)
        self.prefix_sum = np.cumsum(np.cumsum(np.pad(self.diagram, 2), axis=0), axis=1)
        occupied_rows, occupied_cols = np.where(self.diagram)
        for i, j in zip(occupied_rows, occupied_cols):
            neighbors = self.prefix_sum[i + 3][j + 3] - \
                        self.prefix_sum[i][j + 3] - \
                        self.prefix_sum[i + 3][j] + \
                        self.prefix_sum[i][j]
            self.accessible[i, j] = (neighbors - 1) < 4

    def remove_all(self):
        while self.total_accessible > 0:
            self.removed += self.total_accessible
            self.diagram[self.accessible] = False
            self.determine_accessible()


if __name__ == '__main__':
    filename = 'input/Day4.txt'
    data = read_file(filename)

    diagram = Diagram(data)
    diagram.determine_accessible()
    print(f"The answer to part 1 is {diagram.total_accessible}")

    diagram.remove_all()
    print(f"The answer to part 2 is {diagram.removed}")
