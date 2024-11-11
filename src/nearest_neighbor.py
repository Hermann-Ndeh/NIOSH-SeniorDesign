import numpy as np
import math

class NearestNeighbor:
    def __init__(self, data):
        self.data = data
    
    def get_euclidean_distance(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def get_nearest_neighbors(self):
        nearest_neighbors = []
    
        for i, current_item in enumerate(self.data):
            nearest = None
            min_distance = float('inf')
            
            for j, other_item in enumerate(self.data):
                if i != j:
                    distance = self.get_euclidean_distance(current_item['center'], other_item['center'])
                    if distance < min_distance:
                        min_distance = distance
                        nearest = other_item
            
            # Store the result for the current node
            nearest_neighbors.append({
                "label": current_item["label"],
                "nearest_neighbor_label": nearest["label"] if nearest else None,
                "distance": min_distance
            })
        
        return nearest_neighbors
    
    