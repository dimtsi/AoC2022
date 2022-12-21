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
from sympy import symbols, Eq, solve, Symbol


def parse(filename: str):
    with open(filename, "r") as f:
        groups: List[str] = f.read().strip().split("\n")

    rules = {}
    for line in groups:
        id, rule = line.split(": ")
        r = rule.split(" ")
        nums = re.findall("-?\d+", rule)
        if len(nums) > 0:
            rules[id] = int(nums[0])
        else:
            rules[id] = r  # type: ignore
    return rules


def rule_res(id, rules, cache):
    if id in cache:
        return cache[id]
    val = rules[id]
    if isinstance(val, int):
        res = val
    elif isinstance(val, Symbol):
        res = val
    else:
        x, op, y = val

        if op == "*":
            res = rule_res(x, rules, cache) * rule_res(y, rules, cache)
        elif op == "+":
            res = rule_res(x, rules, cache) + rule_res(y, rules, cache)
        elif op == "-":
            res = rule_res(x, rules, cache) - rule_res(y, rules, cache)
        elif op == "/":
            res = rule_res(x, rules, cache) / rule_res(y, rules, cache)
        else:
            assert False

    cache[id] = res
    return res


def run(rules):
    r = deepcopy(rules)

    eq1, _, eq_2 = r["root"]

    out = rule_res("root", r, {})
    print(int(out))
    return int(out)


def runp2(rules):
    r = deepcopy(rules)
    x = Symbol("x")
    r["root"][1] = "-"
    r["humn"] = x
    cache = {}

    eq = Eq(rule_res("root", r, cache), 0)

    out = solve(eq)[0]
    print(int(round(out)))
    return int(out)


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

    sample_a_answer = 152
    sample_b_answer = 301

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
    submit_answer(answer_a, "a", datetime(2022, 12, 21))
    submit_answer(answer_b, "b", datetime(2022, 12, 21))
