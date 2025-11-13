def CheckNeighbors(maze_map: dict[tuple[int, int], dict[str, int]]):
    neighbors = []

    for cell, neighbor in maze_map.items():
        for direction in neighbor:
            if maze_map[cell][direction] == 1:
                print(cell)
                break
        # print(f"Cell : {cell}, Neighbor: {neighbor}")

    return neighbors


def main() -> None:
    # giving it an empty maze
    CheckNeighbors({})


if __name__ == "__main__":
    main()
