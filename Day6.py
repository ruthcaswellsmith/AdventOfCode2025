from utils import read_file, Part
from typing import List

import numpy as np


class Mathsheet:
    def __init__(self, data: List[str], part: Part):
        self.data = data
        self.operators = [e for e in data[-1].split()]
        self.nums, self.results = None, []
        if part == Part.PT1:
            self._process_pt1()
        else:
            self._process_pt2()

    @property
    def result(self):
        return sum(self.results)

    def _process_pt1(self):
        self.nums = np.array([[int(e) for e in line.split()] for line in data[:-1]], dtype=int)
        self.nums = self.nums.T

        self.results = [self.operate_on_elements(self.nums[i, :], op)
                        for i, op in enumerate(self.operators)]

    def _process_pt2(self):
        self.nums = \
            np.array([[0 if e == ' ' else int(e) for e in line] for line in data[:-1]], dtype=int)
        self.nums = self.nums.T
        elements, op_num = [], len(self.operators)-1
        for i in range(self.nums.shape[0]-1, -1, -1):
            try:
                elements.append(
                    int("".join([str(e) for e in self.nums[i] if e != 0]))
                )
            except ValueError:
                self.results.append(
                    self.operate_on_elements(np.array(elements), self.operators[op_num])
                )
                op_num -= 1
                elements = []
        self.results.append(
            self.operate_on_elements(elements, self.operators[op_num])
        )

    @staticmethod
    def operate_on_elements(elements: np.ndarray, op: str) -> np.int64:
        return np.sum(elements) if op == '+' else np.prod(elements)


if __name__ == '__main__':
    filename = 'input/Day6.txt'
    data = read_file(filename)

    math_sheet = Mathsheet(data, Part.PT1)
    print(f"The answer to part 1 is {math_sheet.result}")

    math_sheet = Mathsheet(data, Part.PT2)
    print(f"The answer to part 1 is {math_sheet.result}")
