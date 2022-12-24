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


class Blizzard:
    def __init__(self, nb, sb, wb, eb, walls, freeze=True):
        self.nb = nb
        self.sb = sb
        self.wb = wb
        self.eb = eb
        self.walls = walls
        self.n_rows = max(walls, key=lambda x: x[0])[0] + 1
        self.n_cols = max(walls, key=lambda x: x[1])[1] + 1

        if freeze:
            self.freeze()

    def next(self):
        nnb, nwb, nsb, neb = set(), set(), set(), set()
        # n
        for i, j in self.nb:
            if i == 1:
                nnb.add((self.n_rows - 1 - 1, j))
            else:
                nnb.add((i - 1, j))
        # s
        for i, j in self.sb:

            if i == self.n_rows - 1 - 1:
                nsb.add((1, j))
            else:
                nsb.add((i + 1, j))
        # w
        for i, j in self.wb:

            if j == 1:
                nwb.add((i, self.n_cols - 1 - 1))
            else:
                nwb.add((i, j - 1))
        # e
        for i, j in self.eb:

            if j == self.n_cols - 1 - 1:
                neb.add((i, 1))
            else:
                neb.add((i, j + 1))

        return Blizzard(nnb, nsb, nwb, neb, self.walls)

    def is_blizz(self, pos):
        if any(pos in x for x in [self.nb, self.wb, self.eb, self.sb]):
            return True
        return False

    def possible_moves(self, pos):
        i, j = pos
        cands = []
        if i - 1 >= 0:
            cands.append((i - 1, j))
        if i + 1 < self.n_rows:
            cands.append((i + 1, j))
        if j - 1 >= 0:
            cands.append((i, j - 1))
        if j + 1 < self.n_cols:
            cands.append((i, j + 1))
        cands.append((i, j))

        final_cands = [
            cand
            for cand in cands
            if (not self.is_blizz(cand) and not cand in self.walls)
        ]
        return final_cands

    def freeze(self):
        self.nb = frozenset(self.nb)
        self.sb = frozenset(self.sb)
        self.wb = frozenset(self.wb)
        self.sb = frozenset(self.sb)
        self.walls = frozenset(self.walls)

    def print(self):
        g = [["." for j in range(self.n_cols)] for i in range(self.n_rows)]

        for i, j in self.nb:
            if g[i][j] != ".":
                if g[i][j].isnumeric():
                    g[i][j] = str(int(g[i][j]) + 1)
                else:
                    g[i][j] = "2"
                continue
            g[i][j] = "^"

        for i, j in self.sb:
            if g[i][j] != ".":
                if g[i][j].isnumeric():
                    g[i][j] = str(int(g[i][j]) + 1)
                else:
                    g[i][j] = "2"
                continue

            g[i][j] = "v"

        for i, j in self.wb:
            if g[i][j] != ".":
                if g[i][j].isnumeric():
                    g[i][j] = str(int(g[i][j]) + 1)
                else:
                    g[i][j] = "2"
                continue
            g[i][j] = "<"

        for i, j in self.eb:
            if g[i][j] != ".":
                if g[i][j].isnumeric():
                    g[i][j] = str(int(g[i][j]) + 1)
                else:
                    g[i][j] = "2"
                continue
            g[i][j] = ">"

        for i, j in self.walls:
            if g[i][j] != ".":
                assert False
            g[i][j] = "#"
        for row in g:
            print("".join(row))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (
            other.nb == self.nb
            and other.sb == self.sb
            and other.wb == self.wb
            and other.eb == self.eb
        )

    def __hash__(self):
        return hash(
            tuple(
                [
                    frozenset(self.sb),
                    frozenset(self.wb),
                    frozenset(self.eb),
                    frozenset(self.sb),
                ]
            )
        )

    # Have to implement the following for heapq to work in dist and position equality cases
    def __lt__(self, other):
        return other

    def __le__(self, other):
        return other


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    nb, sb, eb, wb = set(), set(), set(), set()
    walls = set()

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            v = lines[i][j]
            if v == "^":
                nb.add((i, j))

            elif v == "v":
                sb.add((i, j))

            elif v == "<":
                wb.add((i, j))

            elif v == ">":
                eb.add((i, j))
            elif v == "#":
                walls.add((i, j))

    g = Blizzard(nb, sb, wb, eb, walls, True)
    return g


def manh(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def astar(g, start, end):

    start_state = (start, g)
    f_score = defaultdict(lambda: float("inf"))
    g_score = defaultdict(lambda: float("inf"))
    f_score[start_state] = 0
    g_score[start_state] = 0

    pq = [(0, start_state)]
    while pq:
        curr_f_score, curr_state = heappop(pq)
        curr_pos, curr_blizz = curr_state
        next_blizz = curr_blizz.next()
        if curr_pos == end:
            print("Found!!!!!!!!")
            return curr_f_score, curr_blizz  # , came_from

        for (i, j) in next_blizz.possible_moves(curr_pos):
            new_state = ((i, j), next_blizz)
            new_g_score = g_score[curr_state] + 1
            if new_g_score < g_score[new_state]:
                g_score[new_state] = new_g_score
                h = manh((i, j), end)
                f_score[new_state] = new_g_score + h
                heappush(pq, (f_score[new_state], new_state))
    return None


def run(g, p2=False):
    start, end = (0, 1), (g.n_rows - 1, g.n_cols - 2)
    res1, res2 = 0, 0
    res, g = astar(g, start, end)
    print(f"A: {res}")
    if p2:
        res1, g = astar(g, end, start)
        print(f"B: {res1}")
        res2, g = astar(g, start, end)
        print(f"C: {res2}")
    final = res + res1 + res2
    return final


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = run(lines, True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 18
    sample_b_answer = 54

    answer_a, answer_b = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    if answer_b:
        assert (
            answer_b == sample_b_answer
        ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
        print("sampleB correct")

    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")

    # submit_answer(answer_a, "a", datetime(2022, 12, 24))
    # submit_answer(answer_b, "b", datetime(2022, 12, 23))
