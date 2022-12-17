OFFSET = 1
LEN = 7


class SHAPE:
    start: tuple

    @property
    def positions(self):
        return []

    @property
    def max_y(self):
        return max(self.positions, key=lambda x: x[1])[1]

    def right(self, s):
        for x, y in self.positions:
            new_x, new_y = x + 1, y

            if new_x == LEN:
                return False
            elif (new_x, new_y) in s:
                return False
        self.start = self.start[0] + 1, self.start[1]
        return True

    def left(self, s):
        for x, y in self.positions:
            new_x, new_y = x - 1, y

            if new_x == -1:
                return False
            elif (new_x, new_y) in s:
                return False

        self.start = self.start[0] - 1, self.start[1]
        return True

    def down(self, s):
        for x, y in self.positions:
            new_x, new_y = x, y - 1

            if new_y == -1:
                return False
            elif (new_x, new_y) in s:
                return False
        self.start = self.start[0], self.start[1] - 1
        return True


class PLUS(SHAPE):
    def __init__(self, height):
        self.id = "+"
        self.offset = OFFSET
        self.start = (self.offset + 2, height + 5)

    @property
    def positions(self):
        c_x, c_y = self.start
        pos = [
            (c_x, c_y),
            (c_x + 1, c_y),
            (c_x - 1, c_y),
            (c_x, c_y + 1),
            (c_x, c_y - 1),
        ]
        return pos


class DASH(SHAPE):
    def __init__(self, height):
        self.id = "-"
        self.offset = OFFSET
        self.start = (self.offset + 1, height + (3 if height == 0 else 4))

    @property
    def positions(self):
        c_x, c_y = self.start
        pos = [(i, c_y) for i in range(c_x, c_x + 4)]
        return pos


class I(SHAPE):
    def __init__(self, height):
        self.id = "I"
        self.offset = OFFSET
        self.start = (self.offset + 1, height + 4)

    @property
    def positions(self):
        c_x, c_y = self.start
        pos = [(c_x, j) for j in range(c_y, c_y + 4)]
        return pos


class SQ(SHAPE):
    def __init__(self, height):
        self.id = "sq"
        self.offset = OFFSET
        self.start = (self.offset + 1, height + 4)

    @property
    def positions(self):
        c_x, c_y = self.start
        pos = [(c_x + 1, c_y + 1), (c_x + 1, c_y), (c_x, c_y), (c_x, c_y + 1)]
        return pos


class L(SHAPE):
    def __init__(self, height):
        self.id = "L"
        self.offset = OFFSET
        self.start = (self.offset + 3, height + 4)

    @property
    def positions(self):
        c_x, c_y = self.start
        pos = [
            (c_x, c_y),
            (c_x, c_y + 1),
            (c_x, c_y + 2),
            (c_x - 1, c_y),
            (c_x - 2, c_y),
        ]
        return pos
