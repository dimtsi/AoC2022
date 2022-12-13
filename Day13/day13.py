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
        groups: List[str] = f.read().strip().split("\n\n")

    pairs = []
    for group in groups:
        v1, v2 = group.split("\n")
        pairs.append([eval(v1), eval(v2)])
    return pairs


def parse2(filename: str):
    with open(filename, "r") as f:
        groups: List[str] = f.read().strip().split("\n")

    pairs = [eval(line) for line in groups if line != ""]
    return pairs


def compare_lists(l1, l2):
    i = 0
    res = "eq"
    while l1 and l2:
        v1 = l1.pop(0)
        v2 = l2.pop(0)

        res = compare(v1, v2)
        if res == "eq":
            continue
        elif not res:
            return False
        else:
            return True
    if not l1 and not l2:
        return "eq"
    if not l1:
        return True
    if not l2 and res is not True:
        return False
    else:
        return True


def compare(v1, v2):
    type1, type2 = type(v1), type(v2)

    if type1 == int and type2 == list:
        v1 = [v1]
        return compare_lists(v1, v2)
    elif type2 == int and type1 == list:
        v2 = [v2]
        return compare_lists(v1, v2)
    elif type1 == int and type2 == int:
        if v1 > v2:
            return False
        elif v1 == v2:
            return "eq"
        else:
            return True
    elif type1 == list and type2 == list:
        if v1 == [] and v2 == []:
            return "eq"
        return compare_lists(v1, v2)
    else:
        assert False, (v1, v2)


def compare_result(v1, v2):
    result = compare(list(v1), list(v2))
    if result == "eq":
        return 0
    elif not result:
        return -1
    elif result is True:
        return 1
    else:
        raise Exception(f"result: {result}")


def run(lines):
    idxs = []
    for i, (v1, v2) in enumerate(lines):
        if i == 4:
            print()
        if compare(v1, v2):
            idxs.append(i + 1)
            print()

    return sum(idxs)


def runp2(lines):
    r = deepcopy(lines)
    r.append([[6]])
    r.append([[2]])

    sorted_l = sorted(
        r,
        key=functools.cmp_to_key(
            lambda x, y: compare_result(deepcopy(x), deepcopy(y))
        ),
    )

    idxs = []
    for idx, v in enumerate(reversed(sorted_l)):
        if v == [[6]] or v == [[2]]:
            idxs.append(idx + 1)
    res = idxs[0] * idxs[1]
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    linesp2 = parse2(filename)
    answer_b = runp2(linesp2)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 13
    sample_b_answer = 140

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
