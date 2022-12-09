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


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    res = []
    for line in lines:
        direction, n = line.split(" ")
        res.append((direction, int(n)))
    return res


def move_head(dir: str, curr_pos: Tuple[int, int]) -> Tuple[int, int]:
    x, y = curr_pos
    if dir == "R":
        x += 1
    elif dir == "L":
        x -= 1
    elif dir == "U":
        y += 1
    elif dir == "D":
        y -= 1
    return x, y


def move_tail(h_xy: Tuple[int, int], t_xy: Tuple[int, int]) -> Tuple[int, int]:
    h_x, h_y = h_xy
    t_x, t_y = t_xy

    dx = h_x - t_x
    dy = h_y - t_y

    if abs(dx) > 1:
        if dx > 0:
            t_x += 1
        else:
            t_x -= 1
        if dy != 0:
            if dy > 0:
                t_y += 1
            else:
                t_y -= 1
    elif abs(dy) > 1:
        if dy > 0:
            t_y += 1
        else:
            t_y -= 1
        if dx != 0:
            if dx > 0:
                t_x += 1
            else:
                t_x -= 1
    return t_x, t_y


def run(moves):
    visited = {(0, 0)}
    head_pos, tail_pos = (0, 0), (0, 0)
    for dir, n in moves:
        for i in range(n):
            head_pos = move_head(dir, head_pos)
            tail_pos = move_tail(head_pos, tail_pos)
            if tail_pos not in visited:
                visited.add(tail_pos)

    res = len(visited)

    return res


def runp2(moves):
    visited = {(0, 0)}
    knot_pos = [(0, 0) for _ in range(9)]
    head_pos = (0, 0)
    for dir, n in moves:
        for i in range(n):
            head_pos = move_head(dir, head_pos)
            prev_pos = head_pos
            for j in range(len(knot_pos)):
                tail_pos = move_tail(prev_pos, knot_pos[j])
                knot_pos[j] = tail_pos
                prev_pos = tail_pos
                if j == 8 and knot_pos[j] not in visited:
                    visited.add(knot_pos[j])

    res = len(visited)
    return res


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

    sample_a_answer = 13
    sample_b_answer = 1

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
