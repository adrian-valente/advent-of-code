def parse_input(filename):
    with open(filename) as f:
        lines = []
        unique_frequencies = set()
        for line in f:
            if len(line.strip()) > 0:
                lines.append([c for c in line.strip()])
        return lines


def get_positions_per_freq(lines):
    positions_per_freq = dict()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c != ".":
                if c not in positions_per_freq:
                    positions_per_freq[c] = []
                positions_per_freq[c].append((i, j))
    return positions_per_freq


def get_antinodes_per_freq_model1(positions_per_freq, height, width):
    antinodes_per_freq = {freq: set() for freq in positions_per_freq}
    for freq, positions in positions_per_freq.items():
        for i, p1 in enumerate(positions):
            for p2 in positions[i+1:]:
                a1 = 2 * p1[0] - p2[0], 2 * p1[1] - p2[1]
                if (0 <= a1[0] < height) and (0 <= a1[1] < width):
                    antinodes_per_freq[freq].add(a1)
                a2 = 2 * p2[0] - p1[0], 2 * p2[1] - p1[1]
                if (0 <= a2[0] < height) and (0 <= a2[1] < width):
                    antinodes_per_freq[freq].add(a2)
    return antinodes_per_freq

def get_antinodes_per_freq_model2(positions_per_freq, height, width):
    antinodes_per_freq = {freq: set() for freq in positions_per_freq}
    for freq, positions in positions_per_freq.items():
        if len(positions) <= 1:
            continue
        for i, p1 in enumerate(positions):
            antinodes_per_freq[freq].add(p1)
            for j, p2 in enumerate(positions[i+1:]):
                if j == len(positions) - 1:
                    antinodes_per_freq[freq].add(p2)
                k = 1
                cont = True
                while cont:
                    a1 = p1[0] + k * (p2[0] - p1[0]), p1[1] + k * (p2[1] - p1[1])
                    a2 = p1[0] - k * (p2[0] - p1[0]), p1[1] - k * (p2[1] - p1[1])
                    cont = False
                    if (0 <= a1[0] < height) and (0 <= a1[1] < width):
                        antinodes_per_freq[freq].add(a1)
                        cont = True
                    if (0 <= a2[0] < height) and (0 <= a2[1] < width):
                        antinodes_per_freq[freq].add(a2)
                        cont = True
                    k += 1
    return antinodes_per_freq

def total_antinodes(antinodes_per_freq):
    return len(set.union(*antinodes_per_freq.values()))


if __name__ == "__main__":
    lines = parse_input("input.txt")
    positions_per_freq = get_positions_per_freq(lines)
    height, width = len(lines), len(lines[0])
    antinodes_per_freq = get_antinodes_per_freq_model1(positions_per_freq, height, width)
    print(total_antinodes(antinodes_per_freq))
    antinodes_per_freq = get_antinodes_per_freq_model2(positions_per_freq, height, width)
    print(antinodes_per_freq)
    print(total_antinodes(antinodes_per_freq))