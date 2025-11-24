from queue import Queue, PriorityQueue


class A_Star:

    def __init__(self, maze, start_cell=(1, 1)) -> None:
        self.maze = maze
        self.start_cell = start_cell
        self.goal_cell = (self.maze.rows, self.maze.cols)
        self.open_cells = PriorityQueue()
        self.g_cost = {cell: float("inf") for cell in maze.grid}
        self.g_cost[self.start_cell] = 0
        self.f_cost = {cell: float("inf") for cell in maze.grid}
        self.f_cost[self.start_cell] = self.Calculate_H_Cost(
            self.start_cell, self.goal_cell
        )

    def Calculate_H_Cost(self, current_cell, target_cell) -> int:
        current_x, current_y = current_cell
        target_x, target_y = target_cell
        return abs(current_x - target_x) + abs(current_y - target_y)

    def pathFinding(self):
        path = dict()
        child_cell = ()
        self.open_cells.put(
            (
                self.f_cost[self.start_cell],
                self.Calculate_H_Cost(self.start_cell, self.goal_cell),
                self.start_cell,
            )
        )
        while not self.open_cells.empty():
            current_cell = self.open_cells.get()[2]  # gets the current cell
            if current_cell == self.goal_cell:
                break
            for direction in "NSEW":  # exploring each direction of current cell
                if self.maze.maze_map[current_cell][direction] == 1:
                    x, y = current_cell
                    if direction == "N":
                        child_cell = (x - 1, y)
                    elif direction == "S":
                        child_cell = (x + 1, y)
                    elif direction == "E":
                        child_cell = (x, y + 1)
                    elif direction == "W":
                        child_cell = (x, y - 1)

                    child_g_cost = self.g_cost[current_cell] + 1
                    child_f_cost = child_g_cost + self.Calculate_H_Cost(
                        child_cell, self.goal_cell
                    )

                    if child_f_cost < self.f_cost[child_cell]:
                        self.g_cost[child_cell] = child_g_cost
                        self.f_cost[child_cell] = child_f_cost
                        self.open_cells.put(
                            (
                                child_f_cost,
                                self.Calculate_H_Cost(child_cell, self.goal_cell),
                                child_cell,
                            )
                        )
                        path[child_cell] = current_cell

        reversed_path = dict()
        cell = self.goal_cell
        while cell != self.start_cell:
            reversed_path[path[cell]] = cell
            cell = path[cell]
        return reversed_path


class BreadthFirstSearch:
    def __init__(self, maze, start_cell=(1, 1)) -> None:
        self.maze = maze
        self.start_cell = start_cell
        self.goal_cell = (self.maze.rows, self.maze.cols)
        self.open_cells = Queue()
        self.visited_cells = []

    def pathFinding(self):
        self.open_cells.put(self.start_cell)
        self.visited_cells.append(self.visited_cells)
        path = dict()
        search_path = []
        child_cell = ()
        while not self.open_cells.empty():
            current_cell = self.open_cells.get()
            if current_cell == self.goal_cell:
                break
            for direction in "ESNW":
                if self.maze.maze_map[current_cell][direction]:
                    x, y = current_cell
                    if direction == "E":
                        child_cell = (x, y + 1)
                    elif direction == "S":
                        child_cell = (x + 1, y)
                    elif direction == "N":
                        child_cell = (x - 1, y)
                    elif direction == "W":
                        child_cell = (x, y - 1)
                    if child_cell in self.visited_cells:
                        continue
                    self.open_cells.put(child_cell)
                    self.visited_cells.append(child_cell)
                    path[child_cell] = current_cell
                    search_path.append(child_cell)

        reversed_path = dict()
        cell = self.goal_cell
        while cell != self.start_cell:
            reversed_path[path[cell]] = cell
            cell = path[cell]
        return search_path, reversed_path


class DepthFirstSearch:
    def __init__(self, maze, start_cell=(1, 1)) -> None:
        self.maze = maze
        self.start_cell = start_cell
        self.goal_cell = (self.maze.rows, self.maze.cols)
        self.open_cells = []  # Stack Implementation
        self.visited_cells = []

    def pathFinding(self):
        self.open_cells.append(self.start_cell)
        self.visited_cells.append(self.visited_cells)
        path = dict()
        search_path = []
        child_cell = ()
        while len(self.open_cells) > 0:
            current_cell = self.open_cells.pop()
            search_path.append(current_cell)
            if current_cell == self.goal_cell:
                break
            for direction in "ESNW":
                if self.maze.maze_map[current_cell][direction]:
                    x, y = current_cell
                    if direction == "E":
                        child_cell = (x, y + 1)
                    elif direction == "S":
                        child_cell = (x + 1, y)
                    elif direction == "N":
                        child_cell = (x - 1, y)
                    elif direction == "W":
                        child_cell = (x, y - 1)
                    if child_cell in self.visited_cells:
                        continue
                    self.open_cells.append(child_cell)
                    self.visited_cells.append(child_cell)
                    path[child_cell] = current_cell

        reversed_path = dict()
        cell = self.goal_cell
        while cell != self.start_cell:
            reversed_path[path[cell]] = cell
            cell = path[cell]
        return search_path, reversed_path


class WallFollowing:
    def __init__(self, maze, start_cell=(1, 1)) -> None:
        self.maze = maze
        self.start_cell = start_cell
        self.goal_cell = (self.maze.rows, self.maze.cols)
        self.directions = {"forward": "N", "left": "W", "back": "S", "right": "E"}

    def RotateClockWise(self):
        keys = list(self.directions.keys())
        values = list(self.directions.values())
        # Rotates the List clockwise by popping the last item and placing it in the first slot
        values.insert(0, values.pop())
        # Reconstructs the direction dictionary with the rotated values
        self.directions = dict(zip(keys, values))

    def RotateAntiClockWise(self):
        keys = list(self.directions.keys())
        values = list(self.directions.values())
        # Rotates the List Anti clockwise by popping the first item and placing it in the last slot
        values.append(values.pop(0))
        # Reconstructs the direction dictionary with the rotated values
        self.directions = dict(zip(keys, values))

    def MoveForward(self, cell):
        x, y = cell
        if self.directions["forward"] == "E":
            return (x, y + 1), "E"
        elif self.directions["forward"] == "W":
            return (x, y - 1), "W"
        elif self.directions["forward"] == "N":
            return (x - 1, y), "N"
        elif self.directions["forward"] == "S":
            return (x + 1, y), "S"

    def pathFinding(self):
        path = ""
        current_cell = self.start_cell
        while True:
            if current_cell == self.goal_cell:
                break
            if self.maze.maze_map[current_cell][self.directions["left"]] == 0:
                if self.maze.maze_map[current_cell][self.directions["forward"]] == 0:
                    self.RotateClockWise()
                else:
                    current_cell, d = self.MoveForward(current_cell)  # type:ignore
                    path += d
            else:
                self.RotateAntiClockWise()
                current_cell, d = self.MoveForward(current_cell)  # type:ignore
                path += d

        # path2 is the path where it doesn't explore any dead end
        path2 = path
        while "EW" in path2 or "WE" in path2 or "NS" in path2 or "SN" in path2:
            path2 = path2.replace("EW", "")
            path2 = path2.replace("WE", "")
            path2 = path2.replace("NS", "")
            path2 = path2.replace("SN", "")
        return path2, path
