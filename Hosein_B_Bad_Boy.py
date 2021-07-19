import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.y}, {self.x})'

    def diff(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Path:
    def __init__(self, base, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.path = base.diff(p1) + p1.diff(p2) + p2.diff(base)

    def __str__(self):
        return f'->{self.p1}->{self.p2}'


def ans_chk(base, y1, x1, y2, x2):
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    return Path(base, p1, p2).path


def adviser(y_max, x_max, home_y, home_x, asns):
    home = Point(home_x, home_y)
    corners = (Point(1, 1), Point(x_max, 1), Point(1, y_max), Point(x_max, y_max))
    diffs = []
    for p in corners:
        for q in corners:
            bpqb = Path(home, p, q)
            diffs.append(bpqb)
    diffs = sorted(diffs, key=lambda x: x.path)
    ansa = ans_chk(home, *asns)
    print(diffs[-1], diffs[-1].path, ansa)


tests = (
    (2, 3, 1, 1, (1, 2, 2, 3)),
    (4, 4, 1, 2, (4, 1, 4, 4)),
    (3, 5, 2, 2, (3, 1, 1, 5)),
    (5, 1, 2, 1, (5, 1, 1, 1)),
    (3, 1, 3, 1, (1, 1, 2, 1)),
    (1, 1, 1, 1, (1, 1, 1, 1)),
    (1_000_000_000, 1_000_000_000, 1_000_000_000, 50, (50, 1, 1, 1_000_000_000))
)
star_time = time.time()
for test in tests:
    adviser(*test)
print(time.time() - star_time)
