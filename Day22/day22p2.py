from collections import deque
from datetime import datetime
from typing import (
    Tuple,
    Optional,
)
from copy import deepcopy

import re

from Day22.borders import (
    BORDERS_SAMPLE,
    BORDERS_INPUT,
    TELEPORT_SAMPLE,
    TELEPORT_INPUT,
)

FACING = {"N", "S", "E", "W"}

ROT = {
    "N": {"R": "E", "L": "W"},
    "E": {"R": "S", "L": "N"},
    "S": {"R": "W", "L": "E"},
    "W": {"R": "N", "L": "S"},
}

DIR_SCORE = {"E": 0, "S": 1, "W": 2, "N": 3}

BORDERS = {}  # type: ignore
TELEPORT = {}  # type: ignore


def parse(filename: str):
    global BORDERS, TELEPORT
    BORDERS, TELEPORT = {}, {}
    with open(filename, "r") as f:
        lines, moves = f.read().split("\n\n")
    lines = lines.split("\n")  # type: ignore

    g = []
    max_x = 0
    for line in lines:
        max_x = max(max_x, len(line))

    for line in lines:
        row = []
        l_line = len(line)
        for p in line:
            row.append(p)
        for em in range(max_x - l_line):
            row.append(" ")
        g.append(row)

    move_nums = deque([int(x) for x in re.findall("\d+", moves)])
    move_dirs = deque([move for move in moves if move.isalpha()])

    q = []
    while move_nums or move_dirs:
        if move_nums:
            n = move_nums.popleft()
            q.append(n)
        if move_dirs:
            n = move_dirs.popleft()  # type: ignore
            q.append(n)

    moves_out = deque(q)

    for i, el in enumerate(g[0]):
        if el == ".":
            start = (0, i)
            break

    BORDERS = BORDERS_SAMPLE if "sample" in filename else BORDERS_INPUT
    TELEPORT = TELEPORT_SAMPLE if "sample" in filename else TELEPORT_INPUT
    print_g(g, start, borders=BORDERS)
    return g, moves_out, start


def print_g(g, curr=None, borders=None):
    g = deepcopy(g)
    if curr:
        g[curr[0]][curr[1]] = "B"

    if borders:
        for i, b_c in borders.items():
            for _, b in b_c.items():
                for pos in b:
                    try:
                        g[pos[0]][pos[1]] = str(i)
                    except:
                        print()

    for row in g:
        print("".join(row))


def teleport(pos, dir, side):
    idx_in_border = BORDERS[side][dir].index(pos)

    target_side, target_border, rev_bord, target_dir = TELEPORT[side][dir]
    target_border = BORDERS[target_side][target_border][:]
    if rev_bord:
        target_border = list(reversed(target_border))

    target_pos = target_border[idx_in_border]

    return target_pos, target_dir, target_side


def move(g, pos, dir, n_moves, side):
    x, y = pos

    for i in range(n_moves):
        print(i + 1, n_moves, dir)
        if (
            (dir == "N" and (x, y) in BORDERS[side]["N"])
            or (dir == "W" and (x, y) in BORDERS[side]["W"])
            or (dir == "E" and (x, y) in BORDERS[side]["E"])
            or (dir == "S" and (x, y) in BORDERS[side]["S"])
        ):
            (new_x, new_y), new_dir, new_side = teleport((x, y), dir, side)
            origin = "teleport"
        else:
            if dir == "N":
                dy = 0
                dx = -1

            elif dir == "S":
                dy = 0
                dx = 1

            elif dir == "W":
                dy = -1
                dx = 0

            elif dir == "E":
                dy = 1
                dx = 0
            else:
                assert False
            origin = "regular"
            new_x, new_y, new_dir, new_side = x + dx, y + dy, dir, side
        try:
            assert g[new_x][new_y] != " "
        except:
            print()

        if g[new_x][new_y] == "#":
            return x, y, dir, side
        else:
            x, y, dir, side = new_x, new_y, new_dir, new_side
        # print("===============================\n\n")
        # print_g(g, (x, y))
        # print()
    return x, y, dir, side


def run(g, moves, start):
    dir = "E"
    side = 1
    pos = start
    print_g(g, pos)
    while moves:
        m = moves.popleft()
        if isinstance(m, int):
            *pos, dir, side = move(g, pos, dir, m, side)
        elif isinstance(m, str):
            dir = ROT[dir][m]
        # print_g(g, pos)
        # print()

    res = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + DIR_SCORE[dir]
    print(res)
    # assert False
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start_t = time()

    grid, moves, start = parse(filename)
    answer_b = run(grid, moves, start)

    end = time()

    print(end - start_t)
    return answer_b


if __name__ == "__main__":

    from utils import submit_answer

    sample = "input.txt"
    input = "input.txt"

    sample_b_answer = 5031

    answer_b = main(sample)

    assert (
        answer_b == sample_b_answer
    ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
    print("sampleB correct")

    # Test on your input and submit
    answer_b = main(input)
    print(f"Your input answers: \nB: {answer_b}")
    #
    submit_answer(answer_b, "b", datetime(2022, 12, 22))
