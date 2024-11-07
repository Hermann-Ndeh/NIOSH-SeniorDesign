from grid_and_grayscale import DefineGrayScale
from red_hazards import IdentifyHazards
import os
import json


def check_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_image_files(image_folder, grayscale_folder, potential_hazards_folder, grid_coords_folder):
    # Check if output directories exist
    check_directory_exists(grayscale_folder)
    check_directory_exists(potential_hazards_folder)

    for filename in os.listdir(image_folder):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            grayscale_path = os.path.join(grayscale_folder, filename)
            potential_hazards_path = os.path.join(potential_hazards_folder, filename)
            basename, extension = os.path.splitext(filename)
            basename = f'{basename}.json'
            grid_coords_path = os.path.join(grid_coords_folder, basename)

            # Process grayscale
            grayscale = DefineGrayScale(image_path, grayscale_path, grid_size=(30, 30))
            grayscale.process_image()

            # Identify hazards
            potential_hazards = IdentifyHazards(
                grayscale_path, potential_hazards_path, 
                grid_size=(30, 30), min_threshold=10000, max_threshold=20000
            )
            potential_hazards.highlight_grids()
            num_red_grids = potential_hazards.count_red_grids()  
            # clusters = potential_hazards.find_clusters()  
            # potential_hazards.draw_clusters(clusters)
            print(f"{filename}: Number of red grids: {num_red_grids}")  
            grid_coords = potential_hazards.grid_info()
            # Save red grid information to a JSON file
            with open(grid_coords_path, "w") as json_file:
                json.dump(grid_coords, json_file, indent=4)
            
    

def main():
    image_folder = 'drone_images'
    grayscale_folder = 'grayscale_drone_images'
    potential_hazards_folder = 'potential_hazards'
    grid_coords_folder = 'hazard_grid_coordinates'

    process_image_files(image_folder, grayscale_folder, potential_hazards_folder, grid_coords_folder)

if __name__ == "__main__":
    main()
