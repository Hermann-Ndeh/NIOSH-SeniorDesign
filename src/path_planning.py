import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib import cm 

class ClusterPathPlanner:
    def __init__(self, centroids, num_groups):

        self.centroids = centroids
        self.num_groups = num_groups
        self.groups = None
        self.paths = None

    def split_clusters(self):
        # Convert centroid coordinates to an array for KMeans
        coords = np.array(list(self.centroids.values()))
        
        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=self.num_groups, random_state=42, n_init=10)
        labels = kmeans.fit_predict(coords)
        
        # Assign clusters to groups starting from 1
        self.groups = {i+1: [] for i in range(self.num_groups)}  # Group labels start from 1
        for node, label in zip(self.centroids.keys(), labels):
            self.groups[label + 1].append(node)  # Adjust label to start from 1
        
        return self.groups

    def nearest_neighbor_path(self, group):
        coords = {node: self.centroids[node] for node in group}
        unvisited = set(coords.keys())
        path = []
        current = next(iter(unvisited))  # Start with an random node
        path.append(current)
        unvisited.remove(current)

        while unvisited:
            # Find the nearest neighbor
            current_coords = coords[current]
            nearest = min(unvisited, key=lambda node: np.linalg.norm(np.array(coords[node]) - np.array(current_coords)))
            path.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        return path

    def plan_paths(self):
        if self.groups is None:
            raise ValueError("Groups have not been split. Call split_clusters() first.")

        self.paths = {}
        for group_id, group in self.groups.items():
            self.paths[group_id] = self.nearest_neighbor_path(group)
        
        return self.paths

    def plot_paths(self):
        if self.groups is None or self.paths is None:
            raise ValueError("Groups or paths are not available. Ensure both are computed.")
        
        colors = cm.get_cmap("tab10", self.num_groups)  # Use cm.get_cmap for compatibility
        coords = self.centroids

        plt.figure(figsize=(8, 6))
        
        # Plot each group and its path
        for group_id, group in self.groups.items():
            group_coords = [coords[node] for node in group]
            path = self.paths[group_id]

            # Plot nodes
            plt.scatter(
                [coords[node][0] for node in group], 
                [coords[node][1] for node in group], 
                label=f"Group {group_id}", 
                color=colors(group_id / self.num_groups)
            )

            # Plot paths
            path_coords = [coords[node] for node in path]
            path_coords.append(path_coords[0])  # Close the loop
            path_x, path_y = zip(*path_coords)
            plt.plot(path_x, path_y, color=colors(group_id / self.num_groups), linestyle="--")

        # Annotate nodes
        for node, (x, y) in coords.items():
            plt.text(x, y, str(node), fontsize=9, ha='right')

        plt.title("Cluster Groups and Nearest Neighbor Paths")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend()
        plt.grid(True)
        
        # Invert the Y-axis to make (0, 0) at the top-left corner
        plt.gca().invert_yaxis()  # Invert the y-axis
        
        return plt



    def print_paths(self):
        if self.paths is None:
            raise ValueError("Paths have not been planned. Call plan_paths() first.")
        
        for group_id, path in self.paths.items():
            print(f"Group {group_id} Path: {path}")