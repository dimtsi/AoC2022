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
        snapshot, rules = f.read().rstrip().split("\n\n")

    snapshot = snapshot.split("\n")  # type: ignore
    rules = rules.split("\n")  # type: ignore

    snapshot, idxs = snapshot[:-1], snapshot[-1]

    stacks = defaultdict(list)

    for i, idx in enumerate(idxs):
        if idx.isnumeric():
            for row in snapshot:
                row = row + " " * (len(idxs) - len(row))
                if row[i].isalpha():
                    stacks[int(idx)].append(row[i])

    stacks = {k: v[::-1] for k, v in stacks.items()}  # type: ignore
    rules = [list(map(int, re.findall("\d+", x))) for x in rules]  # type: ignore

    return stacks, rules


def move(state: Dict[int, List[str]], n_to_move, source, target, p2=False):
    to_pop = state[source][-n_to_move:]
    if not p2:
        to_pop = to_pop[::-1]
    state[source] = state[source][:-n_to_move]
    state[target].extend(to_pop)
    print()


def run(stacks, rules, p2=False):

    for n_to_move, source, target in rules:
        move(stacks, n_to_move, source, target, p2)

    res = "".join([stack[-1] for stack in stacks.values()])
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    l1, l2 = parse(filename)
    answer_a = run(l1, l2)
    l1, l2 = parse(filename)
    answer_b = run(l1, l2, True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = "CMZ"
    sample_b_answer = "MCD"

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
