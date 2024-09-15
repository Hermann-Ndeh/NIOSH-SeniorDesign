from optimal_number_of_drones import OptimalNumberOfDrones
from optimal_drone_path import OptimalPath
from gsd_calculation import GSD

# import numpy as np

class MainClass:
    def __init__(self):
        self.optimal_number_of_drones = OptimalNumberOfDrones()
        self.optimal_drone_path = OptimalPath()
        self.gsd_calculation = GSD()

    def grid_init():
        grid_size = 100
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        grid_size = len(grid)
        subgrids = []

        for i in range(0, grid_size, 5):
            for j in range(0, grid_size, 5):
                subgrid = [row[j:j + 5] for row in grid[i:i + 5]]
                subgrids.append(subgrid)

        return subgrids
        # grid = np.zeros((100, 100), dtype=int)
        # subgrids = grid.reshape(20, 5, 20, 5).swapaxes(1, 2).reshape(20, 20, 5, 5)
        # return grid, subgrids


if __name__ == "__main__":
    main = MainClass()