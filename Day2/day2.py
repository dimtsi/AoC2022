from collections import Counter, defaultdict, deque
from dataclasses import dataclass
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


@dataclass
class VILLAIN:
    ROCK: str = "A"
    PAPER: str = "B"
    SCISSORS: str = "C"


@dataclass
class HERO:
    ROCK: str = "X"
    PAPER: str = "Y"
    SCISSORS: str = "Z"


@dataclass
class HERO_2:
    LOSE: str = "X"
    DRAW: str = "Y"
    WIN: str = "Z"


MAP = {
    VILLAIN.ROCK: HERO.ROCK,
    VILLAIN.PAPER: HERO.PAPER,
    VILLAIN.SCISSORS: HERO.SCISSORS,
}

TO_WIN = {
    VILLAIN.ROCK: HERO.PAPER,
    VILLAIN.PAPER: HERO.SCISSORS,
    VILLAIN.SCISSORS: HERO.ROCK,
}

TO_LOSE = {
    VILLAIN.PAPER: HERO.ROCK,
    VILLAIN.ROCK: HERO.SCISSORS,
    VILLAIN.SCISSORS: HERO.PAPER,
}


def parse(filename: str):
    with open(filename, "r") as f:
        lines: List[str] = f.read().strip().split("\n")

    strategy = [line.strip().split(" ") for line in lines]

    return strategy


def val_score(val):
    if val == HERO.ROCK:
        return 1
    if val == HERO.PAPER:
        return 2
    if val == HERO.SCISSORS:
        return 3


def score_of_round(villain: str, hero: str):
    score = 0
    villain = MAP[villain]
    if villain == hero:
        return 3
    if hero == HERO.ROCK:
        if villain == HERO.SCISSORS:
            score = 6
    elif hero == HERO.PAPER:
        if villain == HERO.ROCK:
            score = 6
    elif hero == HERO.SCISSORS:
        if villain == HERO.PAPER:
            score = 6
    return score


def score_of_round_p2(elf: str, hero: str):
    if hero == HERO_2.WIN:
        hero_select = TO_WIN[elf]
        score = 6
    elif hero == HERO_2.LOSE:
        hero_select = TO_LOSE[elf]
        score = 0
    else:
        hero_select = MAP[elf]
        score = 3

    score += val_score(hero_select)
    return score


def play(strategy: List[List[str]]):
    total_score = 0
    for elf, hero in strategy:
        total_score += val_score(hero)
        total_score += score_of_round(elf, hero)
    return total_score


def play2(strategy: List[List[str]]):
    total_score = 0
    for elf, hero in strategy:
        total_score += score_of_round_p2(elf, hero)
    return total_score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    strategy = parse(filename)
    answer_a = play(strategy)
    answer_b = play2(strategy)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 15
    sample_b_answer = 12

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
