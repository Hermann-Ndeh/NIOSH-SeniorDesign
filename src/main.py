from grid_and_grayscale import DefineGrayScale
from red_hazards import IdentifyHazards
from nearest_neighbor import NearestNeighbor
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

def get_nearest_neighbor(grid_coords_folder, potential_hazards_folder, connected_images_folder):
    check_directory_exists(connected_images_folder)

    for filename in os.listdir(grid_coords_folder):
        if filename.endswith('.json'):
            json_path = os.path.join(grid_coords_folder, filename)
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            # Use the grayscale image with red nodes as the base image for drawing connectors
            grayscale_image_filename = filename.replace('.json', '.jpg')
            grayscale_image_path = os.path.join(potential_hazards_folder, grayscale_image_filename)
            
            # Check if the grayscale image with red nodes exists
            if not os.path.exists(grayscale_image_path):
                print(f"Grayscale image file {grayscale_image_path} does not exist.")
                continue

            # Initialize NearestNeighbor with the grayscale image path
            nn = NearestNeighbor(data, grayscale_image_path)
            nearest_neighbors = nn.get_nearest_neighbors()
            
            if filename == 'DJI_0554.json':
                for neighbor_info in nearest_neighbors:
                    print(f"{neighbor_info}")
            
            # Draw connectors and save the output image to the connected images folder
            nn.connect_neighbors()
            output_image_filename = filename.replace('.json', '_connected.jpg')
            output_image_path = os.path.join(connected_images_folder, output_image_filename)
            nn.save_image(output_image_path)

def main():
    image_folder = 'drone_images'
    grayscale_folder = 'grayscale_drone_images'
    potential_hazards_folder = 'potential_hazards'
    grid_coords_folder = 'hazard_grid_coordinates'
    connected_images_folder = 'connected_neighbors'

    process_image_files(image_folder, grayscale_folder, potential_hazards_folder, grid_coords_folder)
    get_nearest_neighbor(grid_coords_folder, potential_hazards_folder, connected_images_folder)

if __name__ == "__main__":
    main()
