from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple, Generator

import numpy as np

from utils import read_file


class Present:
    def __init__(self, grid: np.ndarray[int]):
        self.grid = grid
        self.occupied_spaces = np.sum(np.sum(self.grid == 1))

    def get_padded_and_rotated_presents(self, size: Tuple[int, int]) -> Generator[np.ndarray, None, None]:
        for u_rows in range(size[0] - self.grid.shape[0] + 1):
            l_rows = size[0] - self.grid.shape[0] - u_rows
            for l_cols in range(size[1] - self.grid.shape[1] + 1):
                r_cols = size[1] - self.grid.shape[1] - l_cols
                for i in range(4):
                    p = np.rot90(self.grid, i)
                    yield np.pad(p, ((u_rows, l_rows), (l_cols, r_cols)))


class Region:
    def __init__(self, size: Tuple[int, int], quantities: List[int], presents: List[Present]):
        self.size = size
        self.area = np.zeros(size, dtype=int)
        self.quantities = [i for i, q in enumerate(quantities) for _ in range(q)]
        self.presents = presents

    @lru_cache
    def place_present(self, q: int) -> bool:
        if q == len(self.quantities):
            # All presents placed successfully!
            return True

        present = self.presents[self.quantities[q]]
        for padded_and_rotated in present.get_padded_and_rotated_presents(self.size):
            if self.present_fits(padded_and_rotated):
                self.update_area(padded_and_rotated, 'add')

                if self.place_present(q + 1):
                    return True

                self.update_area(padded_and_rotated, 'remove')

        return False

    def present_fits(self, padded_piece: np.ndarray) -> bool:
        return True if np.max(self.area + padded_piece) < 2 else False

    def update_area(self, p: np.ndarray, action: str):
        self.area = self.area + p if action == 'add' else self.area - p


class Situation:
    def __init__(self, data: List[str]):
        self.data = data
        self.presents = self._get_presents()
        self.regions = self._get_regions()

    def _get_presents(self) -> List[Present]:
        presents = []
        while self.data[0][1] == ':':
            self.data = self.data[1:]
            present = []
            while self.data[0]:
                present.append([1 if e == '#' else 0 for e in self.data[0]])
                self.data = self.data[1:]
            presents.append(Present(np.array(present, dtype=int)))
            self.data = self.data[1:]
        return presents

    def _get_regions(self) -> List[Region]:
        regions = []
        while self.data:
            pts = self.data[0].split(':')
            x, y = [int(e) for e in pts[0].split('x')]
            quantities = [int(e) for e in pts[1].strip().split(' ')]
            regions.append(Region((x, y), quantities, self.presents))
            self.data = self.data[1:]

        return regions

    @staticmethod
    def process_region(region: Region):
        return region.place_present(0)


if __name__ == '__main__':
    """I created the above solution (spent a long time figuring out the 
    recursion) and it worked for test data.  I knew it was highly unlikely
    it would work on real data which had a much larger search space.  So 
    I spent the rest of the day thinking about strategies for the real data.  
    I became focused on tracking how much space was available (as space became
    inaccessible as you placed pieces).  So I took a look at the data and realized
    half the problems were unsolvable from the get-go because there wasn't enough space.  
    Then I noticed it seemed binary - the problems either were just short of space
    or had hundreds of extra spaces.  When I entered the number of regions that had a lot
    of extra space, that was the answer!  
    Quite anti-climactic IMHO but I guess it's Eric's sense of humor."""

    filename = 'input/test.txt'
    data = read_file(filename)
    situation = Situation(data)
    print(f'The answer to Part 1 is '
          f'{sum([region.place_present(0) for region in situation.regions])}')

    filename = 'input/Day12.txt'
    data = read_file(filename)
    situation = Situation(data)
    unsolvable = sum(r.size[0] * r.size[1] < \
                     sum([situation.presents[q].occupied_spaces for q in r.quantities])
                     for r in situation.regions)
    print(f'The answer to Part 1 is {len(situation.regions) - unsolvable}.')
