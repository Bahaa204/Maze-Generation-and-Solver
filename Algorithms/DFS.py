from pyamaze import maze, agent, COLOR, textLabel
from MazeSolving import DepthFirstSearch


def DFS(
    rows: int = 10,
    cols: int = 10,
    start_cell: tuple[int, int] = (1, 1),
    theme: str = "dark",
    loopPercent: int = 0,
    shape: str = "square",
    filled: bool = False,
    footprints: bool = True,
    color: COLOR | str = COLOR.cyan,
):
    x, y = start_cell
    Maze = maze(rows, cols)
    Maze.CreateMaze(x=Maze.rows, y=Maze.cols, loopPercent=loopPercent, theme=theme)

    SearchAgent = agent(
        parentMaze=Maze,
        x=x,
        y=y,
        shape=shape,
        filled=filled,
        footprints=footprints,
        color=color,
    )

    Agent = agent(
        parentMaze=Maze,
        x=x,
        y=y,
        shape=shape,
        filled=filled,
        footprints=footprints,
        color= COLOR.red,
    )

    dfs = DepthFirstSearch(Maze, start_cell)
    search_path, path = dfs.pathFinding()

    Maze.tracePath({SearchAgent: search_path})
    Maze.tracePath({Agent: path})
    textLabel(Maze, title="DFS Algorithm: ", value=len(search_path) + 1)

    Maze.run()


def main() -> None:
    DFS()


if __name__ == "__main__":
    main()
