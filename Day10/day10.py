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
        # list(map(int, re.findall("-?\d+", line)))
    return lines


def run(lines):
    cycle = 1
    lines = deque(lines)
    wanted = [20, 60, 100, 140, 180, 220]
    wanted_vals = {}
    all_vals = {}
    total_val = 1
    skip_add = True

    while lines:
        if cycle in wanted:
            wanted_vals[cycle] = total_val * cycle
        all_vals[cycle] = total_val
        line = lines.popleft()
        if "noop" in line:
            cycle += 1
        elif "addx" in line:
            if skip_add:
                lines.appendleft(line)
                lines.appendleft("noop")
                skip_add = False
                continue
            val = int(line.split(" ")[1])
            cycle += 1
            total_val += val
            skip_add = True
    return sum(wanted_vals.values()), all_vals


def runp2(all_vals):
    row = ["." for _ in range(40)]
    for j in range(6):
        for i in range(40):
            spr = all_vals[j * 40 + i + 1]
            if i in [spr, spr - 1, spr + 1]:
                row[i] = "#"
        print("".join(row))
        row = ["." for _ in range(40)]
    return


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a, all_vals = run(lines)

    lines = parse(filename)
    answer_b = runp2(all_vals)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 13140
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

    # submit_answer(answer_a, "a")
    # submit_answer(answer_b, "b")
