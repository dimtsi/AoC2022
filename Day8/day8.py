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


def get_neighbors(
    matrix: List[List[int]], i: int, j: int, diagonal: bool = False
) -> List[Tuple[int, int]]:
    neighbors = []

    num_rows = len(matrix)
    num_cols = len(matrix[i])

    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < num_rows:
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < num_cols:
        neighbors.append((i, j + 1))
    # diagonal
    if diagonal:
        if i - 1 >= 0 and j - 1 >= 0:
            neighbors.append((i - 1, j - 1))
        if i - 1 >= 0 and j + 1 < num_cols:
            neighbors.append((i - 1, j + 1))
        if i + 1 < num_rows and j - 1 >= 0:
            neighbors.append((i + 1, j - 1))
        if i + 1 < num_rows and j + 1 < num_cols:
            neighbors.append((i + 1, j + 1))
    return neighbors


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    res = []
    for line in lines:
        row = list(line)
        res.append([int(x) for x in row])
    return res


def get_neighbors_and_values(
    matrix: List[List[int]], i: int, j: int, diagonal=False
) -> Tuple[List[Tuple[int, int]], List[int]]:

    neighbors = get_neighbors(matrix, i, j, diagonal)
    vals = [matrix[x][y] for (x, y) in neighbors]
    return neighbors, vals


def run(grid, p2=False):
    VISIBLE = [[True for j in range(len(grid[i]))] for i in range(len(grid))]

    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            VISIBLE[i][j] = False

    # FROM LEFT
    row_mins_l = defaultdict(lambda: 1e10)
    row_mins_r = defaultdict(lambda: 1e10)
    col_mins_t = grid[0]
    col_mins_b = grid[-1]

    for i in range(len(grid)):
        row_mins_l[i], row_mins_r[i] = grid[i][0], grid[i][-1]
        for j in range(len(grid[0])):
            if grid[i][j] > row_mins_l[i]:
                row_mins_l[i] = grid[i][j]
                VISIBLE[i][j] = True
        for j in reversed(range(len(grid[0]))):
            if grid[i][j] > row_mins_r[i]:
                row_mins_r[i] = grid[i][j]
                VISIBLE[i][j] = True

    for j in range(len(grid[0])):
        for i in range(len(grid)):
            if grid[i][j] > col_mins_t[j]:
                col_mins_t[j] = grid[i][j]
                VISIBLE[i][j] = True
        for i in reversed(range(len(grid))):
            if grid[i][j] > col_mins_b[j]:
                col_mins_b[j] = grid[i][j]
                VISIBLE[i][j] = True

    vis_res = []
    for i in range(len(grid)):
        print(VISIBLE[i])
        for j in range(len(grid[0])):
            if VISIBLE[i][j]:
                vis_res.append((i, j))
    print(vis_res)
    print(len(vis_res))
    return len(vis_res)


def runp2(grid, p2=False):

    L_DISTS = [[0 for j in range(len(grid[i]))] for i in range(len(grid))]
    R_DISTS = [[0 for j in range(len(grid[i]))] for i in range(len(grid))]
    T_DISTS = [[0 for j in range(len(grid[i]))] for i in range(len(grid))]
    B_DISTS = [[0 for j in range(len(grid[i]))] for i in range(len(grid))]

    max_dist = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            to_comp = grid[i][0:j]
            for el in reversed(to_comp):
                L_DISTS[i][j] += 1
                if el >= grid[i][j]:
                    break

            to_comp = grid[i][j + 1 :]
            for el in to_comp:
                R_DISTS[i][j] += 1
                if el >= grid[i][j]:
                    break

    for j in range(len(grid[0])):
        for i in range(len(grid)):
            to_comp = [grid[k][j] for k in range(0, i)]
            for el in reversed(to_comp):
                T_DISTS[i][j] += 1
                if el >= grid[i][j]:
                    break

            to_comp = [grid[k][j] for k in range(i + 1, len(grid))]
            for el in to_comp:
                B_DISTS[i][j] += 1
                if el >= grid[i][j]:
                    break

    ALL_DISTS = [[1 for j in range(len(grid[i]))] for i in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dist = (
                L_DISTS[i][j] * R_DISTS[i][j] * T_DISTS[i][j] * B_DISTS[i][j]
            )
            if dist > max_dist:
                max_dist = dist
            ALL_DISTS[i][j] = dist
    print(ALL_DISTS)
    return max_dist


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = runp2(lines, p2=True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 21
    sample_b_answer = 8

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
