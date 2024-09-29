from typing import Any
import numpy as np
from PIL import Image
from PIL import ImageDraw
import networkx as nx
import math

class DefineGrayScale:
    def __init__(self, grid_size=5, num_grids=400):
        self.grid_size = grid_size
        self.num_grids = num_grids
        self.image_side = int(np.sqrt(self.num_grids)) * self.grid_size
        self.image_array = np.zeros((self.image_side, self.image_side), dtype=np.uint8)
        self.grid_values = np.zeros((int(self.image_side / self.grid_size), int(self.image_side / self.grid_size)), dtype=np.uint8)
        self.red_coordinates = []
        
    def generate_grayscale(self) -> Any:
        for i in range(0, self.image_side, self.grid_size):
            for j in range(0, self.image_side, self.grid_size):
                grayscale_value = np.random.randint(0, 256) 
                self.image_array[i:i + self.grid_size, j:j + self.grid_size] = grayscale_value
                self.grid_values[i // self.grid_size, j // self.grid_size] = grayscale_value

        image = Image.fromarray(self.image_array)

        # image.show()  
        image.save('img/grayscale_grid_image.png')

        print("Grayscale values for each grid:")
        print(self.grid_values)
        return image

    def mark_hazards(self):
        image = self.generate_grayscale()
        image_rgb = Image.new("RGB", image.size)
        image_rgb.paste(image)

        image_rgb_array = np.array(image_rgb)

        for i in range(0, self.image_side, self.grid_size):
            for j in range(0, self.image_side, self.grid_size):
                grid_value = self.image_array[i, j]
                
                if 0 <= grid_value <= 64:
                    image_rgb_array[i:i + self.grid_size, j:j + self.grid_size] = [255, 0, 0]  # Set to red

        result_image = Image.fromarray(image_rgb_array)

        # result_image.show()
        result_image.save('img/colored_grids_image.png')
        self.separate_red_pixels(image_rgb_array)

    def separate_red_pixels(self, image_rgb_array):
        white_image_array = np.full(image_rgb_array.shape, 255, dtype=np.uint8)

        for i in range(0, self.image_side, self.grid_size):
            for j in range(0, self.image_side, self.grid_size):
                grid_value = self.image_array[i, j]

                if 0 <= grid_value <= 64:
                    white_image_array[i:i + self.grid_size, j:j + self.grid_size] = [255, 0, 0]
                    self.red_coordinates.append((j, i))

        result_image = Image.fromarray(white_image_array)

        result_image.save('img/red_separated_image.png')

        print("Red pixel coordinates:")
        print(self.red_coordinates)

        self.connect_isolated_red_pixels(image_rgb_array)

    def connect_isolated_red_pixels(self, image_rgb_array):
        red_edge_positions = {}

        for x, y in self.red_coordinates:
            top_edge_center = (x + self.grid_size // 2, y)
            bottom_edge_center = (x + self.grid_size // 2, y + self.grid_size)
            left_edge_center = (x, y + self.grid_size // 2)
            right_edge_center = (x + self.grid_size, y + self.grid_size // 2)

            red_edge_positions[(x, y)] = [top_edge_center, bottom_edge_center, left_edge_center, right_edge_center]

        result_image = Image.fromarray(image_rgb_array)
        draw = ImageDraw.Draw(result_image)

        for (x1, y1), edges1 in red_edge_positions.items():
            closest_distance = float('inf')
            closest_edge1 = None
            closest_edge2 = None
            closest_node = None
            
            for (x2, y2), edges2 in red_edge_positions.items():
                if (x1, y1) != (x2, y2):
                    for edge1 in edges1:
                        for edge2 in edges2:
                            distance = math.sqrt((edge1[0] - edge2[0]) ** 2 + (edge1[1] - edge2[1]) ** 2)
                            if distance < closest_distance:
                                closest_distance = distance
                                closest_edge1, closest_edge2 = edge1, edge2
                                closest_node = (x2, y2)

            if closest_node:
                draw.line([closest_edge1, closest_edge2], fill=(0, 0, 255), width=1)

        result_image.save('img/connected_red_pixels.png')
