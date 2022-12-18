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

    coords = set()
    for group in groups:
        coord = [int(x) for x in group.split(",")]
        coords.add(tuple(coord))
    return coords


def get_neighbors(i: int, j: int, k: int) -> Set[Tuple[int, int, int]]:
    neighbors = set()

    neighbors.add((i - 1, j, k))
    neighbors.add((i + 1, j, k))
    neighbors.add((i, j + 1, k))
    neighbors.add((i, j - 1, k))
    neighbors.add((i, j, k + 1))
    neighbors.add((i, j, k - 1))
    return neighbors


def run(cubes):
    total_exposed = 0

    for c in cubes:
        neighbors = get_neighbors(*c)
        total_exposed += len(neighbors - cubes)

    print()
    return total_exposed


def out_of_bounds(x, y, z, borders):
    borders_x, borders_y, borders_z = borders
    if not borders_x[0] <= x <= borders_x[1]:
        return True
    if not borders_y[0] <= y <= borders_y[1]:
        return True
    if not borders_z[0] <= z <= borders_z[1]:
        return True
    return False


def runp2(cubes):

    min_i, max_i = (
        min(cubes, key=lambda x: x[0])[0] - 1,
        max(cubes, key=lambda x: x[0])[0] + 1,
    )
    min_j, max_j = (
        min(cubes, key=lambda x: x[1])[1] - 1,
        max(cubes, key=lambda x: x[1])[1] + 1,
    )
    min_k, max_k = (
        min(cubes, key=lambda x: x[2])[2] - 1,
        max(cubes, key=lambda x: x[2])[2] + 1,
    )

    borders = [(min_i, max_i), (min_j, max_j), (min_k, max_k)]

    q = deque([])
    # Start from the perimeter
    for i in (min_i, max_i):
        for j in range(min_j, max_j):
            for k in range(min_k, max_k):
                q.append((i, j, k))

    for j in (min_j, max_j):
        for i in range(min_i, max_i):
            for k in range(min_k, max_k):
                q.append((i, j, k))

    for k in (min_k, max_k):
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                q.append((i, j, k))

    flooded = set()
    while q:
        el = q.popleft()
        for neigh in get_neighbors(*el):
            if neigh in flooded:
                continue
            if out_of_bounds(*neigh, borders):
                continue
            if neigh in cubes:
                continue
            flooded.add(neigh)
            q.append(neigh)

    total_exposed = 0
    for c in cubes:
        neighbors = get_neighbors(*c)
        for neigh in neighbors:
            if neigh in flooded:
                total_exposed += 1
    print(total_exposed)
    return total_exposed


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    linesp2 = parse(filename)
    answer_b = runp2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 64
    sample_b_answer = 58

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

    submit_answer(answer_a, "a", datetime(2022, 12, 18))
    submit_answer(answer_b, "b", datetime(2022, 12, 18))
