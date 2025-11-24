from pyamaze import maze, agent, COLOR, textLabel
from MazeSolving import A_Star


def AStar(
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

    Agent = agent(
        parentMaze=Maze,
        x=x,
        y=y,
        shape=shape,
        filled=filled,
        footprints=footprints,
        color=color,
    )

    a_star = A_Star(Maze, start_cell)
    path = a_star.pathFinding()

    Maze.tracePath({Agent: path})
    textLabel(Maze, title="A* Algorithm: ", value=len(path) + 1)

    Maze.run()


def main() -> None:
    AStar()


if __name__ == "__main__":
    main()
