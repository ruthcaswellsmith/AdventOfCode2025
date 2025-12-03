from utils import read_file


class BatteryBank:
    def __init__(self, line: str, num_batteries: int):
        self.digits = line
        self.num_batteries = num_batteries
        self.on = []

        for i in range(self.num_batteries):
            next_battery = max(self.digits[:len(self.digits) - (self.num_batteries-i) + 1])
            self.digits = self.digits[self.digits.index(next_battery)+1:]
            self.on.append(next_battery)

    @property
    def max_joltage(self):
        return int(''.join(self.on))


if __name__ == '__main__':
    filename = 'input/Day3.txt'
    data = read_file(filename)

    for i, num_batteries in enumerate([2, 12]):
        battery_banks = [BatteryBank(line, num_batteries) for line in data]

        print(f"The answer to part {i+1} is "
              f"{sum([b.max_joltage for b in battery_banks])}")
