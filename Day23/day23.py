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


def parse(filename: str):
    with open(filename, "r") as f:
        groups: List[str] = f.read().strip().split("\n")
    g = {}

    for i, v in enumerate(groups):
        for j in range(len(v)):
            if v[j] == "#":
                g[(i, j)] = "#"

    # print_g(g)
    return g


def print_g(g):

    g = deepcopy(g)

    max_i, max_j = (
        max(g.keys(), key=lambda x: x[0])[0],
        max(g.keys(), key=lambda x: x[1])[1],
    )
    min_i, min_j = (
        min(g.keys(), key=lambda x: x[0])[0],
        min(g.keys(), key=lambda x: x[1])[1],
    )

    g_p = [
        ["." for j in range(min_j, max_j + 1)] for i in range(min_i, max_i + 1)
    ]

    for k in g:
        g_p[k[0] - min_i][k[1] - min_j] = "#"

    for row in g_p:
        print("".join(row))


def get_neighbors(i: int, j: int) -> List[Tuple[int, int]]:
    neighbors = []

    neighbors.append((i - 1, j))
    neighbors.append((i + 1, j))
    neighbors.append((i, j - 1))
    neighbors.append((i, j + 1))
    # diagonal
    neighbors.append((i - 1, j - 1))
    neighbors.append((i - 1, j + 1))
    neighbors.append((i + 1, j - 1))
    neighbors.append((i + 1, j + 1))
    return neighbors


def parse2(filename: str):
    with open(filename, "r") as f:
        groups: List[str] = f.read().strip().split("\n")

    pairs = [eval(line) for line in groups if line != ""]
    return pairs


def propose(g, pos, order):
    neighs = get_neighbors(*pos)
    if not any(neigh in g for neigh in neighs):
        return None

    n, s, w, e, nw, ne, sw, se = neighs

    while order:
        o = order.popleft()
        if o == "N":
            if n not in g and ne not in g and nw not in g:
                return n
        elif o == "S":
            if s not in g and se not in g and sw not in g:
                return s
        elif o == "W":
            if w not in g and nw not in g and sw not in g:
                return w
        elif o == "E":
            if e not in g and ne not in g and se not in g:
                return e


def get_S(g):
    max_i, max_j = (
        max(g.keys(), key=lambda x: x[0])[0],
        max(g.keys(), key=lambda x: x[1])[1],
    )
    min_i, min_j = (
        min(g.keys(), key=lambda x: x[0])[0],
        min(g.keys(), key=lambda x: x[1])[1],
    )

    return (abs(max_i - min_i) + 1) * (abs(max_j - min_j) + 1) - len(g)


def run(g, p2=False):
    order = deque(["N", "S", "W", "E"])

    r = 0
    while True:
        new_g = defaultdict(list)
        for k in g:
            prop_k = propose(g, k, deepcopy(order))
            if prop_k:
                new_g[prop_k].append(k)
            else:
                new_g[k].append(k)

        # remove conflicts
        to_add = []
        to_pop = []
        for k in new_g:
            if len(new_g[k]) > 1:
                for confl in new_g[k]:
                    if confl in new_g:
                        assert False
                    to_add.append(confl)
                to_pop.append(k)
        # Remove unused keys
        for k in to_add:
            new_g[k] = [k]
        for k in to_pop:
            new_g.pop(k)

        if set(new_g.keys()) == set(g.keys()):
            g = new_g
            break
        g = new_g
        order.rotate(-1)
        r += 1
        if r == 10 and not p2:
            break
        print_g(g)
        print()

    s = get_S(g)
    if p2:
        return r + 1
    return s


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

    sample_a_answer = 110
    sample_b_answer = 20

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

    submit_answer(answer_a, "a", datetime(2022, 12, 23))
    submit_answer(answer_b, "b", datetime(2022, 12, 23))
