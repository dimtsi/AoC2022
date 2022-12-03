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
from termcolor import colored
from copy import deepcopy
from heapq import heappop, heappush
import string
alphabet = list(string.ascii_lowercase)

alpha_map = {}

def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    return lines

def priority(lines: List[str]):
    total_priority = 0
    for line in lines:
        line = list(line)
        length = len(line)
        first, second = set(line[:(length // 2)]), set(line[(length // 2):])
        common = first & second
        assert len(common) == 1
        common = common.pop()

        if common.islower():
            priority = ord(common) - ord("a") + 1
        else:
            priority = ord(common) - ord("A") + 27

        total_priority += priority
    return total_priority

def priority_2(lines: List[str]):
    badges = []

    group = []
    for i, line in enumerate(lines, 1):
        group.append(set(line))
        if i % 3 == 0 and i != 0:
            a, b, c = group
            badges.append((a & b & c).pop())
            group = []

    total_priority = 0

    for badge in badges:
        if badge.islower():
            priority = ord(badge) - ord("a") + 1
        else:
            priority = ord(badge) - ord("A") + 27

        total_priority += priority
    return total_priority



def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = priority(lines)
    lines = parse(filename)
    answer_b =  priority_2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 157
    sample_b_answer = 70

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
