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


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

    l = [list(map(int, re.findall("\d+", x))) for x in lines]
    return l


def part1(lines: List[List[int]]):
    valid = 0
    for line in lines:
        min1, max1, min2, max2 = line
        if (min1 <= min2 and max1 >= max2) or (min2 <= min1 and max2 >= max1):
            valid += 1
    return valid


def part2(lines: List[List[int]]):
    non_overlapping = 0
    for line in lines:
        min1, max1, min2, max2 = line
        if (max1 < min2) or (max2 < min1):
            non_overlapping += 1
    res = len(lines) - non_overlapping
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = part1(lines)
    lines = parse(filename)
    answer_b = part2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 2
    sample_b_answer = 4

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
