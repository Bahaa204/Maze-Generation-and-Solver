from pyamaze import maze, agent, COLOR
from solving import CheckNeighbors

"""
    NOTE: X is the vertical axis and Y is the horizontal axis here

    Maze Generator: PyaMaze by Learning Orbits (https://youtu.be/McMU-WuJwG0)
    
    By default the maze has a size of 10x10, you can change that by specifying it as a parameter e.g: maze(10,20).
    
    By default the maze start location is on the bottom right cell and the goal or the end of the maze is the first cell in the top left(highlighted in green). Any cell can be chosen as the start cell and the goal can be specified to a cell after creating the maze object e.g: Maze.CreateMaze(x=5, y=2) this sets the cell (5,2) to be the goal of the maze.
    
    An agent can be placed on the maze and it can represent the virtual object just to indicate the cell selected in Maze or they can be the physical agents (like robots). their default starting position is the last cell in the grid(bottom right) and it can be specified
    They can have two shapes (square or arrow)
   
   
   An agent can trace a path by using the Maze.tracePath() where it takes the 3 parameters.
   The first being a dictionary that has its keys to be th agents and the values being the path i.e {Agent: path}.
   The Path can be either an dict or a list or a string with the direction like "NES" where N: North, E: East, W:west, S:South
     
"""


# Creating the maze object
Maze = maze()

# Creating the maze and setting the goal to be the bottom right cell(the last cell in the grid)
Maze.CreateMaze(loadMaze=r"maze--2025-11-09--17-03-47.csv", x=Maze.rows, y=Maze.cols)

# Placing the agent at the first cell of the grid
Agent = agent(parentMaze=Maze, footprints=True, x=1, y=1)

print(Maze.maze_map)
Maze.tracePath({Agent: Maze.path})
Maze.run()
