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

    bps = []
    for bp in groups:
        val = int(re.findall("-?\d+", bp)[0])
        bps.append(val)
    return bps


def run(lines):
    zero_orig_idx = lines.index(0)

    deck = deque([(i, n) for i, n in enumerate(lines)])

    for idx, move in enumerate(lines):
        pos = deck.index((idx, move))
        deck.remove((idx, move))
        target = (pos + move) % len(deck)
        deck.insert(target, (idx, move))

    zero_idx = deck.index((zero_orig_idx, 0))

    a = deck[(zero_idx + 1000) % len(deck)][1]
    b = deck[(zero_idx + 2000) % len(deck)][1]
    c = deck[(zero_idx + 3000) % len(deck)][1]

    res = a + b + c
    print(res)
    print()
    return res


def runp2(lines):
    zero_orig_idx = lines.index(0)

    new_list = [n * 811589153 for n in lines]
    deck = deque([(i, n * 811589153) for i, n in enumerate(lines)])

    for _ in range(10):
        for idx, move in enumerate(new_list):
            pos = deck.index((idx, move))
            deck.remove((idx, move))
            target = (pos + move) % len(deck)
            deck.insert(target, (idx, move))

    zero_idx = deck.index((zero_orig_idx, 0))

    a = deck[(zero_idx + 1000) % len(deck)][1]
    b = deck[(zero_idx + 2000) % len(deck)][1]
    c = deck[(zero_idx + 3000) % len(deck)][1]

    res = a + b + c
    print(res)
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

    sample_a_answer = 3
    sample_b_answer = 1623178306

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
    #
    submit_answer(answer_a, "a", datetime(2022, 12, 20))
    submit_answer(answer_b, "b", datetime(2022, 12, 20))
