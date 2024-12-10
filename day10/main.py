import numpy as np

Position = tuple[int, int]

def get_int(c: str) -> int:
    return int(c) if c != "." else -1

def parse_input(filename: str) -> np.ndarray:
    with open(filename, 'r') as f:
        lines = []
        for line in f:
            lines.append(
                [get_int(c) for c in line.strip()]
            )
    return np.array(lines)

class Graph:
    trailheads: list[Position]
    edges: dict[Position, list[Position]]
    heights: np.ndarray

    def __init__(self, map: np.ndarray):
        self.heights = map
        self.edges = {}
        self.trailheads = []
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                self.edges[(i, j)] = []
                if map[i, j] == 0:
                    self.trailheads.append((i, j))
                if i > 0 and map[i-1, j] == map[i, j] + 1:
                    self.edges[(i, j)].append((i-1, j))
                if i < map.shape[0] - 1 and map[i+1, j] == map[i, j] + 1:
                    self.edges[(i, j)].append((i+1, j))
                if j > 0 and map[i, j-1] == map[i, j] + 1:
                    self.edges[(i, j)].append((i, j-1))
                if j < map.shape[1] - 1 and map[i, j+1] == map[i, j] + 1:
                    self.edges[(i, j)].append((i, j+1))

    def dfs(self, head: Position, visited: set[Position]) -> set[Position]:
        """Returns the set of summits (height 9) attained."""
        if self.heights[head[0], head[1]] == 9:
            return set([head])
        summits_attained = set()
        for edge in self.edges[head]:
            dest = edge
            if dest not in visited:
                visited.add(dest)
                summits_attained.update(self.dfs(dest, visited))
        return summits_attained

    def count_hiking_summits(self) -> int:
        total = 0
        for head in self.trailheads:
            total += len(self.dfs(head, {head}))
        return total

    def dfs_total_paths(self, head: Position) -> int:
        if self.heights[head[0], head[1]] == 9:
            return 1
        total_paths = 0
        for edge in self.edges[head]:
            dest = edge
            total_paths += self.dfs_total_paths(dest)
        return total_paths

    def count_hiking_paths(self) -> int:
        total = 0
        for head in self.trailheads:
            total += self.dfs_total_paths(head)
        return total

if __name__ == '__main__':
    map = parse_input('input.txt')
    graph = Graph(map)
    print(len(graph.trailheads))
    print(graph.trailheads)
    print(graph.count_hiking_paths())
