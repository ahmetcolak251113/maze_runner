from window import Window
from maze import Maze


def main():
    win = Window(800, 600)

    maze = Maze(20, 20, 20, 30, 20, 20, win, seed=0)
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
