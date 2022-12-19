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
        id, *costs = list(map(int, re.findall("-?\d+", bp)))
        bps.append(costs)
    return bps


def get_qual(strategy, n_rounds):
    # IntegerSeq
    (
        ore_T_ore,
        clay_T_ore,
        obs_T_ore,
        obs_T_clay,
        geode_T_ore,
        geod_T_obs,
    ) = strategy

    curr_ore, curr_clay, curr_obs, curr_geod = 0, 0, 0, 0
    ore_robs, clay_robs, obs_robs, geod_robs = 1, 0, 0, 0

    state = (
        1,
        ore_robs,
        clay_robs,
        obs_robs,
        geod_robs,
        curr_ore,
        curr_clay,
        curr_obs,
        curr_geod,
    )
    q = deque([state])
    max_geods = 0
    cnt_visited = 0
    visited = set()
    time_to_state = {}
    cnt_visit = 0

    min_time_for_obs = defaultdict(lambda: float("inf"))
    min_time_for_geod = defaultdict(lambda: float("inf"))

    while q:
        state = q.popleft()
        (
            t,
            ore_robs,
            clay_robs,
            obs_robs,
            geod_robs,
            curr_ore,
            curr_clay,
            curr_obs,
            curr_geod,
        ) = state
        if state in visited:
            cnt_visit += 1
            continue

        visited.add(state)
        new_ore = curr_ore + ore_robs
        new_clay = curr_clay + clay_robs
        new_obs = curr_obs + obs_robs
        new_geod = curr_geod + geod_robs

        if t == n_rounds:
            max_geods = max(max_geods, new_geod)
            continue

        if new_geod == 0 and min_time_for_geod and t > min_time_for_geod[1]:
            continue

        if new_geod > 0 and min_time_for_geod[new_geod] < t:
            continue
        else:
            min_time_for_geod[new_geod] = t

        q.append(
            (
                t + 1,
                ore_robs,
                clay_robs,
                obs_robs,
                geod_robs,
                new_ore,
                new_clay,
                new_obs,
                new_geod,
            )
        )

        # build ore
        if curr_ore >= ore_T_ore:
            q.append(
                (
                    t + 1,
                    ore_robs + 1,
                    clay_robs,
                    obs_robs,
                    geod_robs,
                    new_ore - ore_T_ore,
                    new_clay,
                    new_obs,
                    new_geod,
                )
            )
        # build clay
        if curr_ore >= clay_T_ore:
            q.append(
                (
                    t + 1,
                    ore_robs,
                    clay_robs + 1,
                    obs_robs,
                    geod_robs,
                    new_ore - clay_T_ore,
                    new_clay,
                    new_obs,
                    new_geod,
                )
            )

        # build obs
        if curr_ore >= obs_T_ore and curr_clay >= obs_T_clay:
            q.append(
                (
                    t + 1,
                    ore_robs,
                    clay_robs,
                    obs_robs + 1,
                    geod_robs,
                    new_ore - obs_T_ore,
                    new_clay - obs_T_clay,
                    new_obs,
                    new_geod,
                )
            )

        # build geode
        if curr_ore >= geode_T_ore and curr_obs >= geod_T_obs:
            q.append(
                (
                    t + 1,
                    ore_robs,
                    clay_robs,
                    obs_robs,
                    geod_robs + 1,
                    new_ore - geode_T_ore,
                    new_clay,
                    new_obs - geod_T_obs,
                    new_geod,
                )
            )

    print(cnt_visit)
    return max_geods


def get_qual_p2(strategy, n_rounds):

    MAX_ADDITIONAL_GEOD_AT_K = [
        (i * (i + 1)) // 2 for i in reversed(range(n_rounds + 1))
    ]  # Integer Seq
    (
        ore_T_ore,
        clay_T_ore,
        obs_T_ore,
        obs_T_clay,
        geode_T_ore,
        geod_T_obs,
    ) = strategy

    curr_ore, curr_clay, curr_obs, curr_geod = 0, 0, 0, 0
    ore_robs, clay_robs, obs_robs, geod_robs = 1, 0, 0, 0

    state = (
        1,
        ore_robs,
        clay_robs,
        obs_robs,
        geod_robs,
        curr_ore,
        curr_clay,
        curr_obs,
        curr_geod,
    )
    q = deque([state])
    max_geods = 0

    visited = set()
    time_to_state = {}

    min_time_for_obs = defaultdict(lambda: float("inf"))
    min_time_for_geod = defaultdict(lambda: float("inf"))

    DP = {}

    while q:
        state = q.pop()
        (
            t,
            ore_robs,
            clay_robs,
            obs_robs,
            geod_robs,
            curr_ore,
            curr_clay,
            curr_obs,
            curr_geod,
        ) = state

        if state in visited:
            continue

        dp_state = (t, ore_robs, clay_robs, obs_robs, geod_robs)

        visited.add(state)

        new_ore = curr_ore + ore_robs
        new_clay = curr_clay + clay_robs
        new_obs = curr_obs + obs_robs
        new_geod = curr_geod + geod_robs

        max_geods = max(new_geod, max_geods)

        if t == n_rounds:
            continue

        t_rem = n_rounds - t + 2
        max_potential = (
            new_geod + geod_robs * t_rem + MAX_ADDITIONAL_GEOD_AT_K[t + 1]
        )

        if max_potential <= max_geods:
            continue

        need_ore = (clay_T_ore + obs_T_ore + geode_T_ore) * 2 >= new_ore
        need_clay = obs_T_clay * 2 >= new_clay
        need_obs = geod_T_obs * 2 >= new_obs

        # build geode
        if curr_ore >= geode_T_ore and curr_obs >= geod_T_obs:
            q.append(
                (
                    t + 1,
                    ore_robs,
                    clay_robs,
                    obs_robs,
                    geod_robs + 1,
                    new_ore - geode_T_ore,
                    new_clay,
                    new_obs - geod_T_obs,
                    new_geod,
                )
            )

        # build obs
        if curr_ore >= obs_T_ore and curr_clay >= obs_T_clay and need_obs:
            q.append(
                (
                    t + 1,
                    ore_robs,
                    clay_robs,
                    obs_robs + 1,
                    geod_robs,
                    new_ore - obs_T_ore,
                    new_clay - obs_T_clay,
                    new_obs,
                    new_geod,
                )
            )

        # build clay
        if curr_ore >= clay_T_ore and need_clay:
            q.append(
                (
                    t + 1,
                    ore_robs,
                    clay_robs + 1,
                    obs_robs,
                    geod_robs,
                    new_ore - clay_T_ore,
                    new_clay,
                    new_obs,
                    new_geod,
                )
            )

        # build ore
        if curr_ore >= ore_T_ore and need_ore:
            q.append(
                (
                    t + 1,
                    ore_robs + 1,
                    clay_robs,
                    obs_robs,
                    geod_robs,
                    new_ore - ore_T_ore,
                    new_clay,
                    new_obs,
                    new_geod,
                )
            )

        q.append(
            (
                t + 1,
                ore_robs,
                clay_robs,
                obs_robs,
                geod_robs,
                new_ore,
                new_clay,
                new_obs,
                new_geod,
            )
        )

    return max_geods


def run(lines, p2=False):
    total = 0
    scores = []
    for i, line in enumerate((lines[:3] if p2 else lines)):
        if not p2:
            score = get_qual(line, 24)
        else:
            score = get_qual_p2(line, 32)
            scores.append(score)
            print(i, scores)
        total += (i + 1) * score
    print(total, scores)

    if p2:
        top3 = list(reversed(scores))[:3]
        ans = reduce(lambda x, y: x * y, top3)
        print(ans)
        return ans
    return total


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    linesp2 = parse(filename)
    answer_b = run(lines, p2=True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 33
    sample_b_answer = 3472

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

    submit_answer(answer_a, "a", datetime(2022, 12, 19))
    submit_answer(answer_b, "b", datetime(2022, 12, 19))
