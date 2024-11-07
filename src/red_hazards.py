from PIL import Image, ImageDraw
import numpy as np

class IdentifyHazards:
    def __init__(self, image_path, potential_hazards_path, grid_size=(20, 20), min_threshold=0, max_threshold=65535):
        self.image_path = image_path
        self.potential_hazards_path = potential_hazards_path
        self.grid_size = grid_size
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.red_grid_count = 0  # Counter for red grids
        self.red_grids_info = []  # Store info of red grids (label and center coordinates)

    def highlight_grids(self):
        image = Image.open(self.image_path)
        gray_image = image.convert('L')
        grayscale_array = np.array(gray_image, dtype=np.float32) * (65535 / 255)

        height, width = grayscale_array.shape
        cell_height = height // self.grid_size[0]
        cell_width = width // self.grid_size[1]

        rgb_image = gray_image.convert('RGB')
        draw = ImageDraw.Draw(rgb_image, 'RGBA')

        label = 1  # Starting label for grid numbering

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                top = row * cell_height
                left = col * cell_width
                bottom = (row + 1) * cell_height
                right = (col + 1) * cell_width

                grid_cell = grayscale_array[top:bottom, left:right]

                std_value = np.std(grid_cell)

                if self.min_threshold <= std_value <= self.max_threshold:
                    draw.rectangle([left, top, right, bottom], fill=(255, 0, 0, 80))
                    self.red_grid_count += 1  # Increment the counter for red grids

                    # Calculate the center coordinates of the grid cell
                    center_x = (left + right) // 2
                    center_y = (top + bottom) // 2

                    # Append label and center coordinates to red_grids_info
                    self.red_grids_info.append({"label": label, "center": (center_x, center_y)})

                # Label the grid
                draw.text((left + 5, top + 5), str(label), fill="white")
                label += 1  # Increment label for the next grid

        rgb_image.save(self.potential_hazards_path)
        
    def count_red_grids(self):
        return self.red_grid_count  # Return the count of red grids
    def grid_info(self):
        return self.red_grids_info
