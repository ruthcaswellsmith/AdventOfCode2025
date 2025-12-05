from utils import read_file
from typing import List


class KitchenList:
    def __init__(self, data: List[str]):
        sep = data.index("")

        self.fresh_ranges = [range(*map(int, line.split('-'))) for line in data[:sep]]
        self.fresh_ranges.sort(key=lambda r: r.stop)

        self.items = [int(line) for line in data[sep+1:]]
        self.fresh_items = 0

    @property
    def sum_all_fresh_ingredients(self):
        return sum([r.stop - r.start + 1 for r in self.fresh_ranges])

    def collapse_all_ranges(self):
        j = len(self.fresh_ranges) - 1
        while j > 0:
            r1, r2 = self.fresh_ranges[j-1], self.fresh_ranges[j]
            if not (r1.stop < r2.start or r2.stop < r1.start):
                self.fresh_ranges[j-1] = range(min(r1.start, r2.start), max(r1.stop, r2.stop))
                del self.fresh_ranges[j]
            j -= 1

    def determine_if_fresh(self):
        for item in self.items:
            for r in self.fresh_ranges:
                if r.start <= item <= r.stop:
                    self.fresh_items += 1
                if item < r.stop:
                    break


if __name__ == '__main__':
    filename = 'input/Day5.txt'
    data = read_file(filename)

    kitchen_list = KitchenList(data)
    kitchen_list.collapse_all_ranges()
    kitchen_list.determine_if_fresh()
    print(f"The answer to part 1 is {kitchen_list.fresh_items}")

    print(f"The answer to part 2 is {kitchen_list.sum_all_fresh_ingredients}")
