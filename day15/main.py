import numpy as np

tile_to_int = {
    ".": 0,
    "#": 1,
    "O": 2
}
int_to_tile = {i: tile for tile, i in tile_to_int.items()}

def convert_map(map_lines: list[list[str]]) -> tuple[np.ndarray, tuple[int, int]]:
    h, w = len(map_lines), len(map_lines[0])
    map_array = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            if map_lines[i][j] == "@":
                robot_pos = i, j
                map_lines[i][j] = "."
            map_array[i, j] = tile_to_int[map_lines[i][j]]
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
    box = tile_to_int["O"]
    h, w = map_array.shape
    return sum(gps_coords(i, j) for i in range(h) for j in range(w) if map_array[i, j] == box)


def do_move(map_array: np.ndarray, pos: tuple[int, int], move: str) -> tuple[np.ndarray, tuple[int, int]]:
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
    elif map_array[*cell_to_move] == tile_to_int["O"]:
        new_map, new_pos = do_move(map_array, cell_to_move, move)
        if new_pos == cell_to_move:
            print("Can't move box.")
            return map_array, pos
        else:
            # move the box to its new position and return
            print("Move box.")
            new_map[*new_pos] = tile_to_int["O"]
            new_map[*cell_to_move] = tile_to_int["."]
            return new_map, cell_to_move

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
        map_array, robot_pos = do_move(map_array, robot_pos, move)
    return map_array, robot_pos, all_maps, all_positions


if __name__ == "__main__":
    map_array, robot_pos, moves = parse_input("input.txt")
    map_array, robot_pos, all_maps, all_positions = do_moves_sequence(
        map_array, robot_pos, moves
    )
    print(coords_all_boxes(map_array))
