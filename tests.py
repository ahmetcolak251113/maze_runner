import unittest
from maze import Maze


def snapshot_walls(m: Maze):
    cells = m._Maze__cells
    num_cols = len(cells)
    num_rows = len(cells[0]) if num_cols > 0 else 0

    snap = []
    for i in range(num_cols):
        col = []
        for j in range(num_rows):
            c = cells[i][j]
            col.append((c.has_left_wall, c.has_right_wall, c.has_top_wall, c.has_bottom_wall))
        snap.append(tuple(col))
    return tuple(snap)


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        self.assertEqual(len(m1._Maze__cells[0]), num_rows)

    def test_break_entrance_and_exit(self):
        num_cols = 4
        num_rows = 3
        m = Maze(0, 0, num_rows, num_cols, 10, 10)

        m._Maze__cells[0][0].has_top_wall = True
        m._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall = True

        m._Maze__break_entrance_and_exit()

        self.assertFalse(m._Maze__cells[0][0].has_top_wall)
        self.assertFalse(m._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_seed_makes_same_maze(self):
        m1 = Maze(0, 0, 10, 12, 10, 10, seed=0)
        m2 = Maze(0, 0, 10, 12, 10, 10, seed=0)
        self.assertEqual(snapshot_walls(m1), snapshot_walls(m2))

    def test_reset_cells_visited(self):
        m = Maze(0, 0, 6, 7, 10, 10, seed=0)

        for i in range(len(m._Maze__cells)):
            for j in range(len(m._Maze__cells[0])):
                m._Maze__cells[i][j].visited = True

        m._Maze__reset_cells_visited()

        for i in range(len(m._Maze__cells)):
            for j in range(len(m._Maze__cells[0])):
                self.assertFalse(m._Maze__cells[i][j].visited)

    def test_solve_returns_true(self):
        m = Maze(0, 0, 8, 8, 10, 10, seed=0)
        self.assertTrue(m.solve())


if __name__ == "__main__":
    unittest.main()
