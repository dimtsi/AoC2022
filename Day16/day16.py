import functools
import itertools
import os
from collections import Counter, defaultdict, deque
from datetime import datetime
from functools import reduce, lru_cache
from pprint import pprint
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
    Deque,
)
from copy import deepcopy
from heapq import heappop, heappush
import string

import re

import numpy as np

G: Dict[str, List[str]] = {}
R: Dict[str, int] = {}
DISTS: Dict = {}
MAX_SCORE = 0
VALID_VALVES: Set[str] = set()
PATHS = {}
DIST_REV = defaultdict(lambda: defaultdict(list))  # type: ignore


def parse(filename: str):
    global G
    global R
    G = {}
    R = {}
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

    for line in lines:
        try:
            s, v = line.split("; tunnels lead to valves ")
        except:
            s, v = line.split("; tunnel leads to valve ")
        rate = int(s.split("=")[1])
        id = s.split()[1]
        valves = v.split(", ")
        G[id] = valves
        R[id] = rate


@lru_cache(None)
def dijkstra(start: str, end: str):
    distances = defaultdict(lambda: float("inf"))  # type: ignore
    distances[start] = 0
    pq = [(0, start)]
    visited = set()
    origin = {}
    while pq:
        dist, elem = heappop(pq)
        if elem in visited:
            continue
        visited.add(elem)
        for child in G[elem]:
            if child not in visited and distances[child] > dist + 1:
                distances[child] = dist + 1
                if child == end:
                    origin[child] = elem
                    pq = []
                    break
                origin[child] = elem
                heappush(pq, (dist + 1, child))  # type: ignore

    res = distances[end]

    rev_path: Deque[str] = deque([])
    q = [end]
    while True:
        el = q.pop()
        if el != start:
            rev_path.appendleft(el)
            q.append(origin[el])
        else:
            break
    rev_path.appendleft(start)
    return res, list(rev_path)


STATES: Dict[Tuple[str, int], int] = {}


def max_flow(node, score, visited, time):
    global MAX_SCORE, VALID_VALVES, STATES, G, R, DISTS
    best_flow = score

    curr_flow = score + (30 - time) * R[node]
    visited.add(node)

    state = (node, time)

    if state in STATES and STATES[state] > curr_flow:
        return STATES[state]
    else:
        STATES[state] = curr_flow

    best_flow = curr_flow
    if time == 30:
        return best_flow

    unvisited = VALID_VALVES - visited
    candidates = [v for v in unvisited if DISTS[(node, v)] + time < 30]
    for cand in candidates:
        dist_to_cand = DISTS[(node, cand)]

        new_flow = max_flow(
            cand, curr_flow, deepcopy(visited), time + dist_to_cand + 1
        )  # , G, R, DISTS)
        if new_flow > best_flow:
            best_flow = new_flow
            if best_flow > MAX_SCORE:
                MAX_SCORE = best_flow

    return best_flow


def run(lines):
    global DISTS, VALID_VALVES
    for k in G.keys():
        for v in G.keys():
            DISTS[k, v] = dijkstra(k, v)[0]
    VALID_VALVES = set(G.keys())
    res = max_flow("AA", 0, set(), 0)
    print(res)
    return res


def get_curr_flow(open_valves):
    return sum(R[x] for x in open_valves)


def max_flow_p2():
    global MAX_SCORE, G, R

    max_flow = get_curr_flow(VALID_VALVES)

    start = [("AA", "AA", 1, 0, frozenset())]
    M = defaultdict(lambda: (-1, frozenset()))
    q = deque(start)
    i = 0

    while q:
        i += 1
        if i % 1000000 == 0:
            print(MAX_SCORE)
        you, eleph, t, score, opened = q.popleft()
        state = (you, eleph, t)

        m_score, m_opened = M[state]
        if m_score > score:
            continue
        if m_score == score:
            if m_opened.issuperset(opened):
                continue
        M[state] = (score, frozenset(opened))
        opened = set(opened)

        if t == 26:
            MAX_SCORE = max(MAX_SCORE, score)
            continue

        # All valves open. No need for additional search
        if set(opened).issuperset(VALID_VALVES):
            for t_i in range(t + 1, 27):
                new_score = score + max_flow
                new_state = (you, eleph, t_i, new_score, frozenset(opened))
                q.append(new_state)
            continue

        # You open valve
        if you in VALID_VALVES and you not in opened:
            you_opened = deepcopy(set(opened))
            you_opened.add(you)

            # Elephant also opens
            if eleph not in you_opened and eleph in VALID_VALVES:
                out_opened = deepcopy(you_opened) | {eleph}
                new_score = score + get_curr_flow(out_opened)
                new_state = (
                    you,
                    eleph,
                    t + 1,
                    new_score,
                    frozenset(out_opened),
                )
                q.append(new_state)

            # Traverse all elephant moves in next step while you open valve
            for eleph_new in G[eleph]:
                out_opened = you_opened
                new_score = score + get_curr_flow(out_opened)
                new_state = (
                    you,
                    eleph_new,
                    t + 1,
                    new_score,
                    frozenset(out_opened),
                )
                q.append(new_state)

        # Traverse all your moves in next step
        for you_new in G[you]:
            # Elephant opens valve
            if eleph in VALID_VALVES and eleph not in opened:
                out_opened = deepcopy(opened) | {eleph}
                new_score = score + get_curr_flow(out_opened)
                new_state = (
                    you_new,
                    eleph,
                    t + 1,
                    new_score,
                    frozenset(out_opened),
                )
                q.append(new_state)

            # Elephant moves as well
            for eleph_new in G[eleph]:
                out_opened = deepcopy(opened)
                new_score = score + get_curr_flow(out_opened)
                new_state = (
                    you_new,
                    eleph_new,
                    t + 1,
                    new_score,
                    frozenset(out_opened),
                )
                q.append(new_state)

    print(MAX_SCORE)
    return MAX_SCORE


def runp2(lines):
    global DISTS, VALID_VALVES, PATHS
    for k in G.keys():
        for v in G.keys():
            DISTS[k, v], PATHS[k, v] = dijkstra(k, v)
            DIST_REV[k][DISTS[k, v]].append(v)
    VALID_VALVES = set(k for k in G if R[k] != 0)
    res = max_flow_p2()
    print(res)
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)
    answer_b = runp2(lines)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 1651
    sample_b_answer = 1707

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

    submit_answer(answer_a, "a", datetime(2022, 12, 16))
    submit_answer(answer_b, "b", datetime(2022, 12, 16))
