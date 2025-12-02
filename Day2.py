from utils import read_file, Part
from itertools import chain


class IDRange:
    def __init__(self, line: str):
        self.lower, self.upper = line.split('-')

    def process_range(self, part: Part):
        invalid_ids = []
        validate_id = self.validate_id_pt1 if part == Part.PT1 else self.validate_id_pt2
        for id_number in range(int(self.lower), int(self.upper) + 1):
            if not validate_id(str(id_number)):
                invalid_ids.append(id_number)
        return invalid_ids

    @staticmethod
    def validate_id_pt1(id_str: str):
        halfway = len(id_str)//2
        if id_str[:halfway] == id_str[halfway:]:
            return False
        return True

    @staticmethod
    def validate_id_pt2(id_str: str):
        n = len(id_str)
        divisors = [i for i in range(1, n + 1) if n % i == 0 and i != len(id_str)]

        for d in divisors:
            seq_set = {p for p in [id_str[d*i:d*i+d] for i in range(len(id_str)//d)]}
            if len(seq_set) == 1:
                return False

        return True


if __name__ == '__main__':
    filename = 'input/Day2.txt'
    data = read_file(filename)

    id_ranges = [IDRange(line) for line in data[0].split(',')]

    print(f"The answer to part 1 is "
          f"{sum(list(chain.from_iterable(id_range.process_range(Part.PT1) for id_range in id_ranges)))}")

    print(f"The answer to part 2 is "
          f"{sum(list(chain.from_iterable(id_range.process_range(Part.PT2) for id_range in id_ranges)))}")
