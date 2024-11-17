from PIL import Image, ImageDraw
import numpy as np

class IdentifyHazards:
    def __init__(self, image_path, potential_hazards_path, grid_size, min_threshold=0, max_threshold=65535):
        self.image_path = image_path
        self.potential_hazards_path = potential_hazards_path
        self.grid_size = grid_size
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.red_grid_count = 0  # Counter for red grids
        self.red_grids_cords = []  # Store info of red grids (label and center coordinates)
        self.red_grids = []
        

    def highlight_grids(self):
        image = Image.open(self.image_path)
        gray_image = image.convert('I;16')
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
                    # Highlight the original red grid
                    draw.rectangle([left, top, right, bottom], fill=(255, 0, 0, 30))
                    self.red_grid_count += 1  # Increment the counter for red grids

                    # Split the red grid into 8 smaller grids (2 rows x 4 columns)
                    small_cell_height = (bottom - top) // 4
                    small_cell_width = (right - left) // 4
                    
                    for i in range(4):  # 2 rows for splitting
                        for j in range(4):  # 4 columns for splitting
                            small_top = top + i * small_cell_height
                            small_left = left + j * small_cell_width
                            small_bottom = small_top + small_cell_height
                            small_right = small_left + small_cell_width

                            # Draw the smaller red grid
                            draw.rectangle([small_left, small_top, small_right, small_bottom], outline="black")

                    center_x = (left + right) // 2
                    center_y = (top + bottom) // 2

                    self.red_grids_cords.append({"label": label, "center": (center_x, center_y)})
                    self.red_grids.append(label)
                    # label += 1  # Increment label for the original grid

                draw.text((left + 5, top + 5), str(label), fill="white")
                label += 1  # Increment label for the next grid

        rgb_image.save(self.potential_hazards_path)
        
    def count_red_grids(self):
        return self.red_grid_count  # Return the count of red grids

    def grid_info(self):
        return self.red_grids_cords
    
    def red_grids_lists(self):
        return self.red_grids
    
    
