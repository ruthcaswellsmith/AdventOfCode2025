from __future__ import annotations

from typing import List, Tuple

from utils import read_file, Part


class LineSegment:
    def __init__(self, t1: Tuple[int, int], t2: Tuple[int, int]):
        self.t1 = t1
        self.t2 = t2
        self.orientation = "H" if self.t1[1] == self.t2[1] else 'V'

    def __hash__(self):
        return "-".join([str(self.t1[0]), str(self.t1[1]), str(self.t2[0]), str(self.t2[1])])

    def __eq__(self, other):
        return True if self.t1 == other.t1 and self.t2 == other.t2 else False

    def intersects(self, other: LineSegment) -> bool:
        if self.orientation == other.orientation:
            # line segments are parallel
            return False
        if len({self.t1, self.t2, other.t1, other.t2}) != 4:
            # line segments share a corner
            return False
        if self.orientation == 'H':
            if min(self.t1[0], self.t2[0]) <= other.t1[0] <= max(self.t1[0], self.t2[0]) and \
                    min(other.t1[1], other.t2[1]) < self.t1[1] < max(other.t1[1], other.t2[1]):
                return True
        elif self.orientation == 'V':
            if min(self.t1[1], self.t2[1]) <= other.t1[1] <= max(self.t1[1], self.t2[1]) and \
                    min(other.t1[1], other.t2[0]) < self.t1[0] < max(other.t1[0], other.t2[1]):
                return True
        return False


class Floor:
    def __init__(self, data: List[str]):
        self.red_tiles = [tuple(map(int, line.split(','))) for line in data]
        self.line_segments = []
        for i, t1 in enumerate(self.red_tiles[:-1]):
            self.line_segments.append(LineSegment(t1, self.red_tiles[i+1]))
        self.line_segments.append(LineSegment(self.red_tiles[-1], self.red_tiles[0]))

    @staticmethod
    def _get_area(t1: Tuple[int, int], t2: Tuple[int, int]):
        return (abs(t2[1] - t1[1]) + 1) * (abs(t2[0] - t1[0]) + 1)

    def find_biggest_rectangle(self, part: Part):
        biggest = 0
        for i, t1 in enumerate(self.red_tiles[:-1]):
            for t2 in self.red_tiles[i + 1:]:
                if part == Part.PT1 or \
                        self._no_line_segment_intersects_perimeter(t1, t2):
                    biggest = max(biggest, self._get_area(t1, t2))
        return biggest

    def _no_line_segment_intersects_perimeter(self, t1: Tuple[int, int], t2: [Tuple, int, int]):
        # Check every side of this rectangle against every line segment
        for side in [
            LineSegment(t1, (t2[0], t1[1])),
            LineSegment((t2[0], t1[1]), t2),
            LineSegment(t2, (t1[0], t2[1])),
            LineSegment((t1[0], t2[1]), t1)
        ]:
            for line_segment in self.line_segments:
                if line_segment.intersects(side):
                    return False
        return True


if __name__ == '__main__':
    filename = 'input/Day9.txt'
    data = read_file(filename)

    floor = Floor(data)
    print(f"The answer to Part 1 is {floor.find_biggest_rectangle(Part.PT1)}.")

    print(f"The answer to Part 2 is {floor.find_biggest_rectangle(Part.PT2)}.")
