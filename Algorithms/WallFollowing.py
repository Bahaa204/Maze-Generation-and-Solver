from pyamaze import maze, agent, COLOR, textLabel
from MazeSolving import WallFollowing


def Wallfollowing(
    rows: int = 10,
    cols: int = 10,
    start_cell: tuple[int, int] = (1, 1),
    theme: str = "dark",
    loopPercent: int = 0,
    footprints: bool = True,
    color: COLOR | str = COLOR.cyan,
):
    x, y = start_cell
    Maze = maze(rows, cols)
    Maze.CreateMaze(x=Maze.rows, y=Maze.cols, loopPercent=loopPercent, theme=theme)

    Deadends_Agent = agent(
        parentMaze=Maze,
        x=x,
        y=y,
        shape="arrow",
        footprints=footprints,
        color=color,
    )

    Agent = agent(
        parentMaze=Maze,
        x=x,
        y=y,
        shape="arrow",
        footprints=footprints,
        color=COLOR.red,
    )

    Wallfollowing = WallFollowing(Maze, start_cell)
    no_deadends_path, deadends_path = Wallfollowing.pathFinding()

    Maze.tracePath({Deadends_Agent: deadends_path})
    Maze.tracePath({Agent: no_deadends_path})
    textLabel(
        Maze,
        title="Wall Following Algorithm: ",
        value=len(no_deadends_path) + 1,
    )

    Maze.run()


def main() -> None:
    Wallfollowing()


if __name__ == "__main__":
    main()
