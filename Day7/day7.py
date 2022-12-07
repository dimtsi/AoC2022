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


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")
    return lines


class Node:
    def __init__(self, id, w=0, neighs=None, parent=None):
        self.id = id
        self.w = w
        self.children: List[str] = neighs or []
        self.parent = parent


TREE: Dict[str, Node] = {}
WEIGHTS: Dict[str, int] = {}


def node_weight(node: Node, nodes: Dict[str, Node]):
    print(node.id, node.children)
    if node.id in WEIGHTS:
        return WEIGHTS[node.id]

    child_weight = 0
    for child in node.children:
        w = node_weight(nodes[child], nodes)
        child_weight += w
    total_w = node.w + child_weight
    WEIGHTS[node.id] = total_w
    return total_w


def calc_all_weights():
    node_weight(TREE["/"], TREE)


def run(cmds, p2=False):
    curr_dir = None
    buff = deque(cmds)
    while buff:
        cmd_str = buff.popleft()
        if cmd_str.startswith("$"):
            is_command = True
        else:
            is_command = False
        cmd = cmd_str.split(" ")
        if is_command:
            if cmd[1] == "cd":
                if cmd[2] == "..":
                    curr_dir: Node = TREE[curr_dir.parent]
                else:
                    if not cmd[2] in TREE.keys():
                        TREE[cmd[2]] = Node(cmd[2])
                    curr_dir = TREE[
                        os.path.join(
                            curr_dir.id if curr_dir else "", TREE[cmd[2]].id
                        )
                    ]
        else:
            if cmd[0] == "dir":
                child_path = os.path.join(curr_dir.id, cmd[1])
                if not child_path in TREE.keys():
                    TREE[child_path] = Node(child_path)
                TREE[curr_dir.id].children.append(child_path)
                TREE[child_path].parent = curr_dir.id
            else:
                TREE[curr_dir.id].w += int(cmd[0])

    calc_all_weights()
    if not p2:
        res = sum([w for w in WEIGHTS.values() if w < 100000])
        return res
    else:
        unused = 7e7 - WEIGHTS["/"]
        cands = [(k, w) for k, w in WEIGHTS.items() if w > (3e7 - unused)]
        min_k = min(cands, key=lambda x: x[1])[1]
        return min_k


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    global TREE
    global WEIGHTS
    TREE = {}
    WEIGHTS = {}

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines)

    TREE = {}
    WEIGHTS = {}

    lines = parse(filename)
    answer_b = run(lines, p2=True)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 95437
    sample_b_answer = 24933642

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
