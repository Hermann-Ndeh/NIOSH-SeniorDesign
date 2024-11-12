import cv2
import math

class NearestNeighbor:
    def __init__(self, data, image_path):
        self.data = data
        self.image = cv2.imread(image_path)
    
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
    
    def connect_neighbors(self):
        nearest_neighbors = self.get_nearest_neighbors()
        
        for neighbor in nearest_neighbors:
            # Find the centers of the current node and its nearest neighbor
            current_center = next(item['center'] for item in self.data if item['label'] == neighbor['label'])
            nearest_center = next(item['center'] for item in self.data if item['label'] == neighbor['nearest_neighbor_label'])
            
            # Draw a line between the current node and its nearest neighbor
            cv2.line(self.image, tuple(current_center), tuple(nearest_center), (0, 255, 0), 2)
        
        # Display the image with lines connecting nodes
        cv2.imshow("Connected Nearest Neighbors", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self, output_path):
        cv2.imwrite(output_path, self.image)
        # print(f"Image saved to {output_path}")
    