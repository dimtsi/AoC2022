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


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    return lines


def snafu_to_real(line):
    real = 0
    for i, snaf in enumerate(line, 1):
        sig = len(line) - i
        if snaf.isnumeric():
            real += int(snaf) * (5 ** (sig))
        elif snaf == "-":
            real -= 5 ** (sig)
        elif snaf == "=":
            real -= 2 * 5 ** (sig)
    return real


def real_to_snafu(num):
    s = ""
    curr_n = num
    while True:
        rem = curr_n % 5
        if rem == 2:
            s += "2"
            curr_n = (curr_n - 2) // 5
        elif rem == 1:
            s += "1"
            curr_n = (curr_n - 1) // 5
        elif rem == 0:
            s += "0"
            curr_n = curr_n // 5
        elif rem == 3:
            s += "="
            curr_n = (curr_n + 2) // 5
        elif rem == 4:
            s += "-"
            curr_n = (curr_n + 1) // 5

        if curr_n == 0:
            break
    res = s[::-1]
    return res


def run(lines):
    total = 0
    for line in lines:
        total += snafu_to_real(line)
    print(total)
    res = real_to_snafu(total)
    print(res)
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = "2=-1=0"
    sample_b_answer = None

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
