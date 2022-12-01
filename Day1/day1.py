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


def parse(filename: str):
    with open(filename, "r") as f:
        elves: List[str] = f.read().strip().split("\n\n")

    cals_per_elf = []
    for elf in elves:
        cals = [int(x) for x in elf.split("\n")]
        cals_per_elf.append(cals)
    return cals_per_elf


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    cals_per_elf = parse(filename)
    total_cals_per_elf = [sum(x) for x in cals_per_elf]
    answer_a = max(total_cals_per_elf)

    top_3 = sorted(total_cals_per_elf)[::-1][:3]
    answer_b = sum(top_3)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 24000
    sample_b_answer = 45000

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
