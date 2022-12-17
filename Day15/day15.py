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
        lines: List[str] = f.read().strip().split("\n")

        S = {}
        for line in lines:
            sx, sy, bx, by = list(map(int, re.findall("-?\d+", line)))
            S[(sx, sy)] = (bx, by)
    return S


@lru_cache(None)
def manh(p1, p2):
    a_x, a_y = p1
    (
        b_x,
        b_y,
    ) = p2
    dist = abs(a_x - b_x) + abs(a_y - b_y)
    return dist


def interval(S, closest, target):
    dy = abs(S[1] - target)
    if dy >= closest:
        return None

    res = [S[0] - abs(dy - closest), S[0] + abs(dy - closest)]
    return res


def merge_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])

    out = []
    out.append(intervals[0])

    for curr in intervals[1:]:
        out_last_start, out_last_end = out[-1][0], out[-1][1]
        start = curr[0]
        if out_last_start <= start <= out_last_end + 1:
            out[-1][1] = max(out_last_end, curr[1])
        else:
            out.append(curr)
    return out


def run(lines, target):
    S = lines
    CLOSEST = {k: manh(k, v) for k, v in S.items()}

    cnt = 0
    intervals = []

    for s in S:
        interv = interval(s, CLOSEST[s], target)
        if interv:
            intervals.append(interv)
    final = merge_intervals(intervals)

    for final in final:
        cnt += len(range(*final))
    return cnt


def runp2(lines, bounds):
    S = lines
    CLOSEST = {k: manh(k, v) for k, v in S.items()}

    for i in range(bounds[1]):
        if i % int(1e5) == 0:
            print(i)
        intervals = []
        for s in S:
            interv = interval(s, CLOSEST[s], i)
            if interv:
                # if min(interv) <= bounds[0] and max(interv) >= bounds[1]:
                #     break
                # elif min(interv) < bounds[0]:
                #     interv = [bounds[0], interv[1]]
                # elif max(interv) > bounds[1]:
                #     interv = [interv[0], bounds[1]]
                intervals.append(interv)
        final = merge_intervals(intervals)
        if len(final) > 1:
            break
    res_y = final[0][1] + 1

    out = (res_y * int(4e6)) + i
    print(out)
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)

    target = target = 11 if "sample" in filename else int(2e6)
    answer_a = run(lines, target)

    linesp2 = parse(filename)
    answer_b = runp2(
        linesp2, [0, int(4e6)] if not "sample" in filename else [0, 20]
    )

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 26
    sample_b_answer = 56000011

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

    submit_answer(answer_a, "a", datetime(2022, 12, 15))
    submit_answer(answer_b, "b", datetime(2022, 12, 15))
