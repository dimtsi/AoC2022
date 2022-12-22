import functools
import os
from collections import Counter, defaultdict, deque
from datetime import datetime
from functools import reduce, lru_cache
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
    Union,
    Generator,
)
from copy import deepcopy
from heapq import heappop, heappush
import string

import re

import numpy as np
from sympy import symbols, Eq, solve, Symbol

FACING = {"N", "S", "E", "W"}

ROT = {
    "N": {"R": "E", "L": "W"},
    "E": {"R": "S", "L": "N"},
    "S": {"R": "W", "L": "E"},
    "W": {"R": "N", "L": "S"},
}

DIR_SCORE = {"E": 0, "S": 1, "W": 2, "N": 3}


def parse(filename: str):
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

    row_limits = {}
    for i in range(len(g)):
        min_i, max_i = None, None
        for j in range(len(g[0])):
            if g[i][j] != " ":
                if not min_i:
                    min_i = i, j
                max_i = i, j
        row_limits[i] = min_i, max_i

    col_limits = {}
    for j in range(len(g[1])):
        min_j, max_j = None, None
        for i in range(len(g)):
            if g[i][j] != " ":
                if not min_j:
                    min_j = i, j
                max_j = i, j
        col_limits[j] = min_j, max_j

    # print_g(g)
    #
    # for (min_i, max_i) in row_limits.values():
    #     g[min_i[0]][min_i[1]] = "B"
    #     g[max_i[0]][max_i[1]] = "B"
    #
    # for (min_j, max_j) in col_limits.values():
    #     g[min_j[0]][min_j[1]] = "B"
    #     g[max_j[0]][max_j[1]] = "B"
    #
    # g[start[0]][start[1]] = "S"
    #
    #
    # print_g(g)
    return g, moves_out, start, row_limits, col_limits


def print_g(g, curr=None):
    g = deepcopy(g)
    if curr:
        g[curr[0]][curr[1]] = "B"
    for row in g:
        print("".join(row))


def move(g, pos, dir, n_moves, row_lims, col_lims):
    x, y = pos
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

    for i in range(n_moves):
        # print(i + 1, n_moves, dir)
        if dir == "N" and (x, y) == col_lims[y][0]:
            new_x, new_y = col_lims[y][1]
        elif dir == "S" and (x, y) == col_lims[y][1]:
            new_x, new_y = col_lims[y][0]
        elif dir == "E" and (x, y) == row_lims[x][1]:
            new_x, new_y = row_lims[x][0]
        elif dir == "W" and (x, y) == row_lims[x][0]:
            new_x, new_y = row_lims[x][1]
        else:
            new_x, new_y = x + dx, y + dy

        assert g[new_x][new_y] != " "

        if g[new_x][new_y] == "#":
            return x, y
        else:
            x, y = new_x, new_y
        # print("===============================\n\n")
        # print_g(g, (x, y))
        # print()
    return x, y


def run(g, moves, start, row_limits, col_limits):
    dir = "E"
    curr_pos = start
    print_g(g, curr_pos)
    while moves:
        m = moves.popleft()
        if isinstance(m, int):
            curr_pos = move(g, curr_pos, dir, m, row_limits, col_limits)
        elif isinstance(m, str):
            dir = ROT[dir][m]
        # print_g(g, curr_pos)
        # print()

    res = 1000 * (curr_pos[0] + 1) + 4 * (curr_pos[1] + 1) + DIR_SCORE[dir]
    print(res)
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start_t = time()
    answer_a = None, None

    grid, moves, start, row_lims, col_lims = parse(filename)
    answer_a = run(grid, moves, start, row_lims, col_lims)

    # lines = parse(filename)
    # answer_b = runp2(lines)
    end = time()

    print(end - start_t)
    return answer_a


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 6032
    answer_a = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")

    # Test on your input and submit
    answer_a = main(input)
    print(f"Your input answers: \nA: {answer_a}")
    #
    submit_answer(answer_a, "a", datetime(2022, 12, 22))
