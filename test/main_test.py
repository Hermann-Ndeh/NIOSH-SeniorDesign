import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main as main

class MainTest():

    def test_initialize_grid():
        grid, subgrids = main.MainClass.grid_init()
        assert grid.size == 10000, f"Total grid size is {grid.size}."
        assert len(grid) == 100, f"Total grid row length is {len(grid)}."
        assert len(subgrids) == 20, f"Each subgrid has a row length of {len(subgrids)}."
        assert all(len(row) == 100 for row in grid), f"Total grid column length is {(len(row) for row in grid)}."
        assert all(len(row) == 20 for row in subgrids), f"Each subgrid has a column length of {(len(row) for row in subgrids)}."
        assert (cell == 0 for row in subgrids for cell in row), f"The default value is incorrect."

    test_initialize_grid()
    print("grid_init function passed all tests.")