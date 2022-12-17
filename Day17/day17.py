import functools
from collections import deque
from copy import deepcopy
from typing import (
    List,
    Tuple,
    Optional,
)

from Day17.shapes import SHAPE, PLUS, L, DASH, I, SQ


class R:
    plus = PLUS
    l = L
    dash = DASH
    i = I
    sq = SQ

    @classmethod
    def order(cls):
        return [cls.dash, cls.plus, cls.l, cls.i, cls.sq]


def parse(filename: str):
    with open(filename, "r") as f:
        groups = f.read().strip()

    moves = list(groups)
    return deque(moves)


def print_grid(curr, space, max_H):

    sp = deepcopy(space)
    sp.update(set(curr.positions))
    for j in reversed(range(max(max_H, curr.max_y) + 1)):
        row = []
        for i in range(7):
            if (i, j) in sp:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))
    print("\n\n")


def run(lines, n, space, verb=False):
    max_h = 0
    moves = deepcopy(lines)

    q = deque(R.order())
    i = 0
    j = 0
    while i < n:
        eltype = q.popleft()
        q.append(eltype)

        curr = eltype(max_h)
        if verb:
            print()
            print_grid(curr, space, max_h)
            print()

        while True:
            next_move = moves.popleft()
            j += 1
            moves.append(next_move)
            if verb:
                print(f"before move: {next_move}")
                print_grid(curr, space, max_h)

            if next_move == "<":
                curr.left(space)
            elif next_move == ">":
                curr.right(space)
            else:
                raise Exception("Unknown Type")
            if verb:
                print("after move")
                print_grid(curr, space, max_h)
            can_go_down = curr.down(space)
            if verb:
                print(f"after down: {can_go_down}")
                print_grid(curr, space, max_h)

            if not can_go_down:
                space.update(set(curr.positions))
                i += 1
                max_h = max(max_h, curr.max_y)
                break

    return max_h + 1


def get_new_skyline(curr: SHAPE, skyline):
    new_skyline = skyline
    for x, y in curr.positions:
        if y > skyline[x]:
            skyline[x] = y
    return skyline


def runp2(lines, n, space, verb=False):
    max_h = 0
    moves = deepcopy(lines)
    M = {}
    skyline = [-1 for _ in range(7)]
    period = None

    q = deque(R.order())
    i = 0
    j = 0
    while not period:
        eltype = q.popleft()
        q.append(eltype)

        curr = eltype(max_h)
        if verb:
            print()
            print_grid(curr, space, max_h)
            print()

        while True:
            next_move = moves.popleft()
            j += 1
            moves.append(next_move)
            if verb:
                print(f"before move: {next_move}")
                print_grid(curr, space, max_h)

            if next_move == "<":
                can_move = curr.left(space)
            elif next_move == ">":
                can_move = curr.right(space)
            else:
                raise Exception("Unknown Type")
            if verb:
                print("after move")
                print_grid(curr, space, max_h)
            can_go_down = curr.down(space)
            if verb:
                print(f"after down: {can_go_down}")
                print_grid(curr, space, max_h)

            if not can_go_down:
                space.update(set(curr.positions))
                i += 1
                max_h = max(max_h, curr.max_y)
                skyline = get_new_skyline(curr, skyline)
                rel_skyline = [max_h - l for l in skyline]

                state_id = (tuple(rel_skyline), tuple(moves), curr.id)
                if state_id in M:
                    last_i = M[state_id]["idx"][-1][1]
                    last_h = M[state_id]["height"][-1][1]
                    M[state_id]["idx"].append([last_i, i])
                    M[state_id]["height"].append([last_h, max_h])
                    # We let 10 matches to look for pattern. Wont probably work for any dataset
                    if len(M[state_id]["idx"]) > 10:
                        idx_diffs = [
                            st[1] - st[0] for st in M[state_id]["idx"][1:]
                        ]
                        height_diffs = [
                            st[1] - st[0] for st in M[state_id]["height"][1:]
                        ]

                        if (
                            len(set(idx_diffs)) == 1
                            and len(set(height_diffs)) == 1
                        ):
                            period = idx_diffs[-1]
                            height_period = height_diffs[-1]
                else:
                    M[state_id] = {
                        "idx": [[0, i]],
                        "height": [[0, max_h]],
                        "state": frozenset(space),
                    }
                break

    target_n = n % period
    to_multiply = n // period

    multiplied = to_multiply * height_period

    res = run(deepcopy(lines), target_n, set())
    out = multiplied + res
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    lines = parse(filename)
    answer_a = run(lines, 2022, set())
    lines = parse(filename)
    answer_b = runp2(lines, 1000000000000, set())

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 3068
    sample_b_answer = 1514285714288

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
