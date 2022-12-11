import math
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


class Monkey:
    def __init__(self, id, items, op, div, cond_true, cond_false):
        self.id = id
        self.items = items
        self.op = op
        self.div = div
        self.true_cond = cond_true
        self.false_cond = cond_false
        self.inspections = 0
        self.p2 = False
        self.lcm = 1

    def play(self, M):
        for i, old in enumerate(self.items):
            new_val = eval(self.op)
            if not self.p2:
                new_val = new_val // 3
            else:
                new_val %= self.lcm
            if (new_val % self.div) == 0:
                M[self.true_cond].items.append(new_val)
            else:
                M[self.false_cond].items.append(new_val)
        self.inspections += len(self.items)
        self.items = []


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n\n")

    M = []
    for monk in lines:
        for i, line in enumerate(monk.split("\n")):
            if i == 0:
                id = int(re.findall("-?\d+", line)[0])
            if i == 1:
                items = list(map(int, re.findall("-?\d+", line)))
            if i == 2:
                op = line.split(" = ")[1]
            if i == 3:
                div = int(re.findall("-?\d+", line)[0])
            if i == 4:
                true_cond = int(re.findall("-?\d+", line)[0])
            if i == 5:
                false_cond = int(re.findall("-?\d+", line)[0])

        M.append(Monkey(id, items, op, div, true_cond, false_cond))
    return M


def run(M: List[Monkey], p2=False):
    lcm = 1
    for m in M:
        lcm *= (lcm * m.div) // math.gcd(lcm, m.div)

    if p2:
        for m in M:
            m.p2 = True
            m.lcm = lcm

    for _ in range(10000 if p2 else 20):
        for m in M:
            m.play(M)

    inspections = sorted([m.inspections for m in M])
    total = inspections[-1] * inspections[-2]

    return total


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    lines = parse(filename)
    answer_b = run(lines, p2=True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 10605
    sample_b_answer = 2713310158
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
