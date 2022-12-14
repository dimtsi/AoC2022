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

R = set()
S = set()
MAX_Y = None
BOTTOM = None


def parse(filename: str):
    with open(filename, "r") as f:
        moves: List[str] = f.read().strip().split("\n")

    return moves


def single_rock_path(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    R.add(tuple(p1))
    R.add(tuple(p2))

    dx = x2 - x1
    dy = y2 - y1

    if dx != 0:
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            R.add((x, y1))
    elif dy != 0:
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            R.add((x1, y))
    elif dx != 0 and dy != 0:
        raise Exception("Check input")


def build_abyss_limits():
    global BOTTOM
    global MAX_Y
    BOTTOM = set(x[0] for x in R)
    MAX_Y = max(R, key=lambda x: x[1])[1]


def build_rock_path(line):
    rocks = []
    for move in line.split(" -> "):
        rocks.append(list(map(int, re.findall("-?\d+", move))))
    for i in range(len(rocks) - 1):
        single_rock_path(rocks[i], rocks[i + 1])


def is_blocked(pos, p2=False):
    if (pos in S) or (pos in R) or (p2 and pos[1] == MAX_Y + 2):
        return True
    return False


def next_pos(pos, p2=False):
    x, y = pos

    if is_blocked((x, y + 1), p2):
        if is_blocked((x - 1, y + 1), p2):
            if is_blocked((x + 1, y + 1), p2):
                return None
            else:
                return x + 1, y + 1
        else:
            return x - 1, y + 1
    else:
        return x, y + 1


def sand_drop():
    global MAX_Y
    start = (500, 0)
    curr = start
    abyss = False
    while curr:
        prev = curr
        curr = next_pos(curr)
        if curr:
            if curr[0] not in BOTTOM or curr[1] > MAX_Y:
                abyss = True
                break
        else:
            break
    if not abyss:
        S.add(prev)
    return abyss


def sand_drop_p2():
    start = (500, 0)
    curr = start
    while curr:
        prev = curr
        curr = next_pos(curr, p2=True)
        if not curr:
            break
    S.add(prev)
    return


def run(lines):
    global R, S, BOTTOM, MAX_Y

    R, S, BOTTOM, MAX_Y = set(), set(), None, None
    [build_rock_path(line) for line in lines]
    build_abyss_limits()

    cnt = 0
    abyss = False
    while not abyss:
        abyss = sand_drop()
        cnt += 1
    return cnt - 1


def runp2(lines):
    global R, S, BOTTOM, MAX_Y

    R, S, BOTTOM, MAX_Y = set(), set(), None, None
    [build_rock_path(line) for line in lines]
    build_abyss_limits()

    cnt = 0
    while (500, 0) not in S:
        sand_drop_p2()
        cnt += 1
    return cnt


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = runp2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 24
    sample_b_answer = 93

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

    submit_answer(answer_a, "a")
    submit_answer(answer_b, "b")
