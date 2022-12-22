from collections import defaultdict

BORDERS_SAMPLE = {
    1: {
        "N": [(0, j) for j in range(8, 12)],
        "S": [(3, j) for j in range(8, 12)],
        "W": [(i, 8) for i in range(0, 4)],
        "E": [(i, 11) for i in range(0, 4)],
    },
    2: {
        "N": [(4, j) for j in range(0, 4)],
        "S": [(7, j) for j in range(0, 4)],
        "W": [(i, 0) for i in range(4, 8)],
        "E": [(i, 3) for i in range(4, 8)],
    },
    3: {
        "N": [(4, j) for j in range(4, 8)],
        "S": [(7, j) for j in range(4, 8)],
        "W": [(i, 4) for i in range(4, 8)],
        "E": [(i, 7) for i in range(4, 8)],
    },
    4: {
        "N": [(4, j) for j in range(8, 12)],
        "S": [(7, j) for j in range(8, 12)],
        "W": [(i, 8) for i in range(4, 8)],
        "E": [(i, 11) for i in range(4, 8)],
    },
    5: {
        "N": [(8, j) for j in range(8, 12)],
        "S": [(11, j) for j in range(8, 12)],
        "W": [(i, 8) for i in range(8, 12)],
        "E": [(i, 11) for i in range(8, 12)],
    },
    6: {
        "N": [(8, j) for j in range(12, 16)],
        "S": [(11, j) for j in range(12, 16)],
        "W": [(i, 12) for i in range(8, 12)],
        "E": [(i, 15) for i in range(8, 12)],
    },
}

# Targets: target_cube, target_border, reverse_idx, new_direction
TELEPORT_SAMPLE = {
    1: {
        "N": [2, "N", True, "S"],
        "S": [4, "N", False, "S"],
        "W": [3, "N", False, "S"],
        "E": [6, "E", True, "W"],
    },
    2: {
        "N": [1, "N", True, "S"],
        "S": [5, "S", True, "N"],
        "W": [6, "S", True, "N"],
        "E": [3, "W", False, "E"],
    },
    3: {
        "N": [1, "W", False, "E"],
        "S": [5, "W", True, "E"],
        "W": [2, "E", False, "W"],
        "E": [4, "W", False, "E"],
    },
    4: {
        "N": [1, "S", False, "N"],
        "S": [5, "N", False, "S"],
        "W": [3, "E", False, "W"],
        "E": [6, "N", True, "S"],
    },
    5: {
        "N": [4, "S", False, "N"],
        "S": [2, "S", True, "N"],
        "W": [3, "S", True, "N"],
        "E": [6, "W", False, "E"],
    },
    6: {
        "N": [4, "E", True, "W"],
        "S": [2, "W", True, "E"],
        "W": [5, "E", False, "W"],
        "E": [1, "E", True, "W"],
    },
}


BORDERS_INPUT = {
    1: {
        "N": [(0, j) for j in range(50, 100)],
        "S": [(49, j) for j in range(50, 100)],
        "W": [(i, 50) for i in range(0, 50)],
        "E": [(i, 99) for i in range(0, 50)],
    },
    2: {
        "N": [(0, j) for j in range(100, 149)],
        "S": [(49, j) for j in range(100, 149)],
        "W": [(i, 100) for i in range(0, 50)],
        "E": [(i, 149) for i in range(0, 50)],
    },
    3: {
        "N": [(50, j) for j in range(50, 100)],
        "S": [(99, j) for j in range(50, 100)],
        "W": [(i, 50) for i in range(50, 100)],
        "E": [(i, 99) for i in range(50, 100)],
    },
    4: {
        "N": [(100, j) for j in range(50, 100)],
        "S": [(149, j) for j in range(50, 100)],
        "W": [(i, 50) for i in range(100, 150)],
        "E": [(i, 99) for i in range(100, 150)],
    },
    5: {
        "N": [(100, j) for j in range(0, 50)],
        "S": [(149, j) for j in range(0, 50)],
        "W": [(i, 0) for i in range(100, 150)],
        "E": [(i, 49) for i in range(100, 150)],
    },
    6: {
        "N": [(150, j) for j in range(0, 50)],
        "S": [(199, j) for j in range(0, 50)],
        "W": [(i, 0) for i in range(150, 200)],
        "E": [(i, 49) for i in range(150, 200)],
    },
}

# Targets: target_cube, target_border, reverse_idx, new_direction
TELEPORT_INPUT = {
    1: {
        "N": [6, "W", False, "E"],
        "S": [3, "N", False, "S"],
        "W": [5, "W", True, "E"],
        "E": [2, "W", False, "E"],
    },
    2: {
        "N": [6, "S", False, "N"],
        "S": [3, "E", False, "W"],
        "W": [1, "E", False, "W"],
        "E": [4, "E", True, "W"],
    },
    3: {
        "N": [1, "S", False, "N"],
        "S": [4, "N", False, "S"],
        "W": [5, "N", False, "S"],
        "E": [2, "S", False, "N"],
    },
    4: {
        "N": [3, "S", False, "N"],
        "S": [6, "E", False, "W"],
        "W": [5, "E", False, "W"],
        "E": [2, "E", True, "W"],
    },
    5: {
        "N": [3, "W", False, "E"],
        "S": [6, "N", False, "S"],
        "W": [1, "W", True, "E"],
        "E": [4, "W", False, "E"],
    },
    6: {
        "N": [5, "S", False, "N"],
        "S": [2, "N", False, "S"],
        "W": [1, "N", False, "S"],
        "E": [4, "S", False, "N"],
    },
}


if __name__ == "__main__":
    res = {i: defaultdict(list) for i in range(1, 7)}  # type: ignore
    for side in TELEPORT_SAMPLE:
        for target, values in TELEPORT_SAMPLE[side].items():
            c, b, _, _ = values
            res[c][b].append(side)  # type: ignore
    from pprint import pprint

    pprint(res)
    print("\n\n")
    res = {i: defaultdict(list) for i in range(1, 7)}
    for side in TELEPORT_INPUT:
        for target, values in TELEPORT_INPUT[side].items():
            c, b, _, _ = values
            res[c][b].append(side)  # type: ignore
    pprint(res)
