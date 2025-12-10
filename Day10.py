from __future__ import annotations

from typing import List
from collections import deque
import pulp as p

from utils import read_file, Part


class Machine:
    def __init__(self, line: str):
        parts = line.split(' ')
        self.indicators = sum([2**i if e == '#' else 0 for i, e in enumerate(parts[0].strip('[').strip(']'))])
        self.buttons = [[int(e) for e in p.strip('(').strip(')').split(',')] for p in parts[1:-1]]
        self.joltages = [int(e) for e in parts[-1].strip('{').strip('}').split(',')]

    @staticmethod
    def press_button(button: List[int], state: int) -> int:
        return state ^ sum([2**i for i in button])

    def find_min_button_presses(self, part: Part):
        if part == Part.PT1:
            return self.solve_pt1()
        else:
            return self.solve_pt2()

    def solve_pt1(self):
        q = deque()
        state, button_presses = 0, 0
        q.append((state, button_presses))
        visited = {state}
        while q:
            state, button_presses = q.popleft()
            button_presses += 1
            for b in self.buttons:
                new_state = self.press_button(b, state)
                if new_state == self.indicators:
                    return button_presses
                if new_state not in visited:
                    visited.add(new_state)
                    q.append((new_state, button_presses))

    def solve_pt2(self):
        prob = p.LpProblem("HowManyButtonPresses?", p.LpMinimize)

        # Define our variables
        button_presses = [p.LpVariable(f"button{i}", lowBound=0, cat='Integer')
                          for i, button in enumerate(self.buttons)]

        # Define our objective function
        prob += sum(button_presses), "ObjectiveFunction"

        # Define our constraints
        for j, joltage in enumerate(self.joltages):
            c = [button_presses[i] for i, button in enumerate(self.buttons) if j in button]
            prob += sum(c) == joltage, f'Constraint{j}'

        # Solve the problem
        prob.solve(p.PULP_CBC_CMD(msg=False))

        return sum([int(b.varValue) for b in button_presses])


if __name__ == '__main__':
    filename = 'input/Day10.txt'
    data = read_file(filename)

    machines = [Machine(line) for line in data]
    print(f"The answer to Part 1 is {sum([m.find_min_button_presses(Part.PT1) for m in machines])}.")

    print(f"The answer to Part 2 is {sum([m.find_min_button_presses(Part.PT2) for m in machines])}.")
