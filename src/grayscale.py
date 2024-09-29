from typing import Any
import numpy as np
from PIL import Image


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
