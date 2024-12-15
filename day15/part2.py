import numpy as np
from itertools import chain

tile_to_int = {
    ".": 0,
    "#": 1,
    "[": 2,
    "]": 3
}
int_to_tile = {i: tile for tile, i in tile_to_int.items()}


def convert_map(map_lines: list[list[str]]) -> tuple[np.ndarray, tuple[int, int]]:
    h, w = len(map_lines), len(map_lines[0]) * 2
    map_array = np.zeros((h, w))
    for i in range(h):
        for j in range(w // 2):
            if map_lines[i][j] == "@":
                robot_pos = i, 2*j
                map_lines[i][j] = "."
            if map_lines[i][j] == "#":
                map_array[i, 2*j] = tile_to_int["#"]
                map_array[i, 2*j+1] = tile_to_int["#"]
            elif map_lines[i][j] == ".":
                map_array[i, 2*j] = tile_to_int["."]
                map_array[i, 2*j+1] = tile_to_int["."]
            elif map_lines[i][j] == "O":
                map_array[i, 2*j] = tile_to_int["["]
                map_array[i, 2*j+1] = tile_to_int["]"]
    return map_array, robot_pos


def parse_input(filename: str) -> None:
    with open(filename) as f:
        map_array = []
        moves = []
        parsing_map = True
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                parsing_map = False
                continue
            if parsing_map:
                map_array.append([c for c in line])
            else:
                moves.extend([c for c in line])

    map_array, robot_pos = convert_map(map_array)
    return map_array, robot_pos, moves


def gps_coords(i: int, j: int) -> int:
    return 100 * i + j


def coords_all_boxes(map_array: np.ndarray) -> int:
    box = tile_to_int["["]
    h, w = map_array.shape
    return sum(gps_coords(i, j) for i in range(h) for j in range(w) if map_array[i, j] == box)


def move_box(map_array: np.ndarray, box_pos: tuple[int, int], move: str) -> np.ndarray:
    print(f"Moving box {box_pos} with move {move}")
    i, j = box_pos
    if move == "^":
        map_array[i-1, j] = tile_to_int["["]
        map_array[i-1, j+1] = tile_to_int["]"]
        map_array[i, j] = tile_to_int["."]
        map_array[i, j+1] = tile_to_int["."]
    elif move == "<":
        map_array[i, j-1] = tile_to_int["["]
        map_array[i, j] = tile_to_int["]"]
        map_array[i, j+1] = tile_to_int["."]
    elif move == ">":
        map_array[i, j+1] = tile_to_int["["]
        map_array[i, j+2] = tile_to_int["]"]
        map_array[i, j] = tile_to_int["."]
    else:
        map_array[i+1, j] = tile_to_int["["]
        map_array[i+1, j+1] = tile_to_int["]"]
        map_array[i, j] = tile_to_int["."]
        map_array[i, j+1] = tile_to_int["."]
    return map_array


def rec_move_boxes(map_array: np.ndarray, boxes_pos: list[tuple[int, int]], move: str) -> tuple[np.ndarray, bool]:
    if move == "^":
        cells_to_check = []
        for (i, j) in boxes_pos:
            cells_to_check.extend([(i-1, j), (i-1, j+1)])
    elif move == "<":
        i, j = boxes_pos[0]
        cells_to_check = [(i, j-1)]
    elif move == ">":
        i, j = boxes_pos[0]
        cells_to_check = [(i, j+2)]
    else:
        cells_to_check = []
        for (i, j) in boxes_pos:
            cells_to_check.extend([(i+1, j), (i+1, j+1)])

    if any(map_array[*c] == tile_to_int["#"] for c in cells_to_check):
        print("Can't move boxes.")
        return map_array, False

    if all(map_array[*c] == tile_to_int["."] for c in cells_to_check):
        print("Can move boxes")
        for box_pos in boxes_pos:
            map_array = move_box(map_array, box_pos, move)
        return map_array, True

    else:
        print("Some more boxes in the way.")
        new_boxes = set()
        for c in cells_to_check:
            if map_array[*c] == tile_to_int["["]:
                new_boxes.add(c)
            elif map_array[*c] == tile_to_int["]"]:
                new_boxes.add((c[0], c[1]-1))
        new_map, did_move = rec_move_boxes(map_array, list(new_boxes), move)
        if did_move:
            for box_pos in boxes_pos:
                map_array = move_box(map_array, box_pos, move)
            return new_map, True
        else:
            return map_array, False

def do_move_robot(map_array: np.ndarray, pos: tuple[int, int], move: str) -> tuple[np.ndarray, tuple[int, int]]:
    i, j = pos
    h, w = map_array.shape
    if move == "^":
        cell_to_move = max(i-1, 0), j
    elif move == "<":
        cell_to_move = i, max(j-1, 0)
    elif move == ">":
        cell_to_move = i, min(j+1, w)
    else:
        cell_to_move = min(i+1, h), j

    # Nothing to do
    if pos == cell_to_move or map_array[*cell_to_move] == tile_to_int["#"]:
        print("Can't move")
        return map_array, pos

    # Empty cell: move there
    elif map_array[*cell_to_move] == tile_to_int["."]:
        print("Move to empty space.")
        return map_array, cell_to_move

    # Box: recurse and move there if it was possible
    elif map_array[*cell_to_move] == tile_to_int["["]:
        new_map, did_move = rec_move_boxes(map_array, [cell_to_move], move)
        if did_move:
            return new_map, cell_to_move
        else:
            return map_array, pos

    elif map_array[*cell_to_move] == tile_to_int["]"]:
        c_i, c_j = cell_to_move
        new_map, did_move = rec_move_boxes(map_array, [(c_i, c_j-1)], move)
        if did_move:
            return new_map, cell_to_move
        else:
            return map_array, pos

    else:
        raise ValueError("Unknown case.")


def do_moves_sequence(
    map_array: np.ndarray, robot_pos: tuple[int, int], moves: list[str]
) -> tuple[np.ndarray, tuple[int, int], list[np.ndarray], list[tuple[int, int]]]:
    all_maps = []
    all_positions = []
    for move in moves:
        all_maps.append(map_array.copy())
        all_positions.append(robot_pos)
        print(f"Move {move}")
        map_array, robot_pos = do_move_robot(map_array, robot_pos, move)
        print(map_array)
    return map_array, robot_pos, all_maps, all_positions


if __name__ == "__main__":
    map_array, robot_pos, moves = parse_input("input.txt")
    print(map_array)
    map_array, robot_pos, all_maps, all_positions = do_moves_sequence(
        map_array, robot_pos, moves
    )
    print(coords_all_boxes(map_array))
