class IdentifyNeighbors:

    def __init__(self, grid_dimensions, grid_numbers):
        """
        Initialize the class with grid dimensions and grid numbers.

        Parameters:
            grid_dimensions (tuple): (width, height) of the entire grid area.
            grid_numbers (int): Total number of grids.
        """
        self.grid_dimensions = grid_dimensions
        self.grid_numbers = grid_numbers

    def get_adjacent_grids(self, n, b):
        """
        Get the grid numbers adjacent to the grid labeled n in a b x b grid.

        Parameters:
            n (int): The grid number (1-indexed).
            b (int): The size of the grid (b x b).

        Returns:
            set: A set of adjacent grid numbers.
        """
        adjacent = set()
        
        # Check top neighbor
        if n > b:  # Not in the first row
            adjacent.add(n - b)
        
        # Check bottom neighbor
        if n <= b * (b - 1):  # Not in the last row
            adjacent.add(n + b)
        
        # Check left neighbor
        if (n - 1) % b != 0:  # Not in the first column
            adjacent.add(n - 1)
        
        # Check right neighbor
        if n % b != 0:  # Not in the last column
            adjacent.add(n + 1)
        
        return adjacent

    def compute_connected_set(self, start, b, valid_numbers):
        """
        Compute the full set of connected grids starting from a specific grid, 
        filtering to include only numbers in `valid_numbers`.

        Parameters:
            start (int): The starting grid number.
            b (int): The size of the grid (b x b).
            valid_numbers (set): The set of valid grid numbers to include.

        Returns:
            set: A set of connected grids starting from `start` that are in `valid_numbers`.
        """
        visited = set()  # Track visited grids
        to_visit = {start}  # Start with the given grid

        while to_visit:
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)
                # Add neighbors of the current grid that are in valid_numbers and not visited
                neighbors = self.get_adjacent_grids(current, b)
                to_visit.update(neighbors & valid_numbers - visited)

        return visited

    def compute_cluster_centers(self, clusters, b):
        """
        Compute the center point for each cluster of connected grids.

        Parameters:
            clusters (list[set]): List of sets of grid numbers representing clusters.
            b (int): The size of the grid (b x b).

        Returns:
            dict: A dictionary mapping cluster indices (starting from 1) to their center coordinates.
                Example: {1: (x_center, y_center), 2: (x_center, y_center), ...}
        """
        grid_width, grid_height = self.grid_dimensions
        cell_width = grid_width / b
        cell_height = grid_height / b

        cluster_centers = {}

        for i, cluster in enumerate(clusters, start=1):  # Start cluster labeling from 1
            # Compute the average x and y coordinates of all grids in the cluster
            x_coords = []
            y_coords = []

            for grid in cluster:
                row = (grid - 1) // b  # Row index (0-indexed)
                col = (grid - 1) % b  # Column index (0-indexed)
                center_x = (col + 0.5) * cell_width
                center_y = (row + 0.5) * cell_height
                x_coords.append(center_x)
                y_coords.append(center_y)

            # Calculate cluster center
            cluster_centers[i] = (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

        return cluster_centers
