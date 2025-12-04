import random
import time
from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        if seed is not None:
            random.seed(seed)

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()

        if self.__num_cols > 0 and self.__num_rows > 0:
            self.__break_walls_r(0, 0)

        self.__reset_cells_visited()
        self.__break_entrance_and_exit()

    def solve(self) -> bool:
        self.__reset_cells_visited()
        if self.__num_cols <= 0 or self.__num_rows <= 0:
            return False
        return self.__solve_r(0, 0)

    def __create_cells(self):
        self.__cells = []
        for i in range(self.__num_cols):
            col = []
            for j in range(self.__num_rows):
                col.append(Cell(self.__win))
            self.__cells.append(col)

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y

        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        if self.__num_cols <= 0 or self.__num_rows <= 0:
            return

        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)

        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        current = self.__cells[i][j]
        current.visited = True

        while True:
            neighbors = []

            if i - 1 >= 0 and not self.__cells[i - 1][j].visited:
                neighbors.append((i - 1, j, "L"))
            if i + 1 < self.__num_cols and not self.__cells[i + 1][j].visited:
                neighbors.append((i + 1, j, "R"))
            if j - 1 >= 0 and not self.__cells[i][j - 1].visited:
                neighbors.append((i, j - 1, "U"))
            if j + 1 < self.__num_rows and not self.__cells[i][j + 1].visited:
                neighbors.append((i, j + 1, "D"))

            if len(neighbors) == 0:
                self.__draw_cell(i, j)
                return

            ni, nj, direction = random.choice(neighbors)
            next_cell = self.__cells[ni][nj]

            if direction == "L":
                current.has_left_wall = False
                next_cell.has_right_wall = False
            elif direction == "R":
                current.has_right_wall = False
                next_cell.has_left_wall = False
            elif direction == "U":
                current.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif direction == "D":
                current.has_bottom_wall = False
                next_cell.has_top_wall = False

            self.__draw_cell(i, j)
            self.__draw_cell(ni, nj)

            self.__break_walls_r(ni, nj)

    def __reset_cells_visited(self):
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def __solve_r(self, i, j) -> bool:
        self.__animate()

        current = self.__cells[i][j]
        current.visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        if (
            i - 1 >= 0
            and not current.has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            current.draw_move(self.__cells[i - 1][j], undo=False)
            if self.__solve_r(i - 1, j):
                return True
            current.draw_move(self.__cells[i - 1][j], undo=True)

        if (
            i + 1 < self.__num_cols
            and not current.has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            current.draw_move(self.__cells[i + 1][j], undo=False)
            if self.__solve_r(i + 1, j):
                return True
            current.draw_move(self.__cells[i + 1][j], undo=True)

        if (
            j - 1 >= 0
            and not current.has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            current.draw_move(self.__cells[i][j - 1], undo=False)
            if self.__solve_r(i, j - 1):
                return True
            current.draw_move(self.__cells[i][j - 1], undo=True)

        if (
            j + 1 < self.__num_rows
            and not current.has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            current.draw_move(self.__cells[i][j + 1], undo=False)
            if self.__solve_r(i, j + 1):
                return True
            current.draw_move(self.__cells[i][j + 1], undo=True)

        return False
