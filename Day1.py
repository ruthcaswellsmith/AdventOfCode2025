from utils import read_file

if __name__ == '__main__':
    filename = 'input/Day1.txt'
    data = read_file(filename)

    pointing_at = 50
    password_pt1, password_pt2 = 0, 0
    for line in data:

        direction, clicks = line[:1], int(line[1:])

        password_pt2 += int(clicks / 100)
        clicks %= 100

        if direction == 'R' and pointing_at + clicks >= 100:
            password_pt2 += 1
        elif direction == 'L' and clicks >= pointing_at > 0:
            password_pt2 += 1

        clicks = -clicks if direction == 'L' else clicks
        pointing_at = (pointing_at + clicks + 100) % 100
        password_pt1 += 1 if pointing_at == 0 else 0

    print(f"The answer to part 1 is {password_pt1}")
    print(f"The answer to part 2 is {password_pt2}")
