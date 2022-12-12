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

    grid = []
    for line in lines:
        grid.append(list(line))
    return grid


def get_neighbors(matrix: List[List], i: int, j: int) -> List[Tuple[int, int]]:
    neighbors = []

    n_rows = len(matrix)
    n_cols = len(matrix[i])

    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < n_rows:
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < n_cols:
        neighbors.append((i, j + 1))

    return neighbors


def dijkstra(m: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]):

    distances = defaultdict(lambda: float("inf"))  # type: ignore
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, elem = heappop(pq)
        if elem in visited:
            continue
        visited.add(elem)
        for (i, j) in get_neighbors(m, *elem):
            diff = ord(m[i][j]) - ord(m[elem[0]][elem[1]])
            if diff > 1:
                continue
            if (i, j) not in visited and distances[(i, j)] > dist + 1:
                distances[(i, j)] = dist + 1
                if (i, j) == end:
                    pq = []
                    break
                heappush(pq, (dist + 1, (i, j)))

    res = distances[end]
    return res


def run(lines):
    for i in range(len(lines)):
        for j in range(len(lines[1])):
            if lines[i][j] == "S":
                start = (i, j)
                lines[i][j] = "a"
            if lines[i][j] == "E":
                end = (i, j)
                lines[i][j] = "z"

    res = dijkstra(lines, start, end)
    return res


def runp2(lines):
    starts = []
    for i in range(len(lines)):
        for j in range(len(lines[1])):
            if lines[i][j] == "S":
                lines[i][j] = "a"
            elif lines[i][j] == "E":
                lines[i][j] = "z"
                end = (i, j)
            elif lines[i][j] == "a":
                starts.append((i, j))
    min_dist = float("inf")
    for start in starts:
        res = dijkstra(lines, start, end)
        if res < min_dist:
            min_dist = res
    return min_dist


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

    sample_a_answer = 31
    sample_b_answer = 29

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
