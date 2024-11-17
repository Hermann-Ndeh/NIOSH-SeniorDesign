from grid_and_grayscale import DefineGrayScale
from red_hazards import IdentifyHazards
from neighbors import IdentifyNeighbors
from path_planning import ClusterPathPlanner
from PIL import Image
import numpy as np
import os

def check_directory_exists(directory):
    """Ensure the directory exists, create it if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_image_files(image_folder, grayscale_folder, potential_hazards_folder, grid_coords_folder, drone_paths_folder, row_and_column_grids, number_of_groups):
    # Check if output directories exist
    check_directory_exists(grayscale_folder)
    check_directory_exists(potential_hazards_folder)
    check_directory_exists(grid_coords_folder)
    check_directory_exists(drone_paths_folder)

    for filename in os.listdir(image_folder):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            grayscale_path = os.path.join(grayscale_folder, filename)
            potential_hazards_path = os.path.join(potential_hazards_folder, filename)
            basename, extension = os.path.splitext(filename)
            basename = f'{basename}.txt'
            grid_coords_path = os.path.join(grid_coords_folder, basename)
            drone_paths = os.path.join(drone_paths_folder, filename)

            # Process grayscale
            grayscale = DefineGrayScale(image_path, grayscale_path, grid_size=(row_and_column_grids, row_and_column_grids))
            grayscale.process_image()  # Ensure DefineGrayScale does the grayscale conversion

            # Calculate dynamic thresholds
            min_threshold, max_threshold = calculate_dynamic_thresholds(grayscale_path)

            # Identify hazards with the dynamically calculated thresholds
            potential_hazards = IdentifyHazards(
                grayscale_path,
                potential_hazards_path,
                grid_size=(row_and_column_grids, row_and_column_grids),
                min_threshold=min_threshold,
                max_threshold=max_threshold
            )

            potential_hazards.highlight_grids()
            num_red_grids = potential_hazards.count_red_grids()  
            print(f"{filename}: Number of red grids: {num_red_grids}")  
            grid_coords = potential_hazards.grid_info()
            grid_coords_dictionary = {item['label']: item['center'] for item in grid_coords}

            with open(grid_coords_path, "w") as text_file:
                for key, value in grid_coords_dictionary.items():
                    text_file.write(f"{key}: {value}\n")
            
            red_grids = potential_hazards.red_grids_lists()

            neighbors = IdentifyNeighbors((row_and_column_grids, row_and_column_grids), red_grids)

            # Convert red grids to a set for quick filtering
            valid_numbers = set(red_grids)
            processed = set()  # Track visited numbers and avoid duplicate sets
            connected_sets = {}  # Store connected sets
            label_counter = 1  # Start from 1

            for number in red_grids:
                if number not in processed:
                    connected_set = neighbors.compute_connected_set(number, row_and_column_grids, valid_numbers)
                    
                    label = label_counter
                    connected_sets[label] = connected_set
                    
                    label_counter += 1
                    
                    processed.update(connected_set)

            # Output results
            list_of_clusters = []
            for label, connected_set in connected_sets.items():
                list_of_clusters.append(connected_set)  # Add the entire connected set to the list

            cluster_centers = {}
            key = 1

            for set_ in list_of_clusters:
                # Get the first element from the set (in this case the smallest element)
                first_element = min(set_)
                
                # If the element exists in the input_dict, add it to the new dictionary
                if first_element in grid_coords_dictionary:
                    cluster_centers[key] = grid_coords_dictionary[first_element]
                    key += 1 

            path_planner = ClusterPathPlanner(cluster_centers, number_of_groups)
            path_planner.split_clusters()
            path_planner.plan_paths()
            path_planner.print_paths()
            defined_paths = path_planner.plot_paths()

            # Ensure the drone_paths folder exists before saving the plot
            check_directory_exists(drone_paths_folder)
            defined_paths.savefig(drone_paths)

def main():
    image_folder = 'drone_images'
    grayscale_folder = 'grayscale_drone_images'
    potential_hazards_folder = 'potential_hazards'
    grid_coords_folder = 'hazard_grid_coordinates'
    drone_paths_folder = 'drone_paths'
    row_and_column_grids = 30
    number_of_groups = 5

    process_image_files(image_folder, grayscale_folder, potential_hazards_folder, grid_coords_folder, drone_paths_folder, row_and_column_grids, number_of_groups)

def calculate_dynamic_thresholds(grayscale_path, base_min=10000, base_max=20000):
    # Load the grayscale image
    image = Image.open(grayscale_path).convert('I')  # 'I' for 16-bit grayscale
    image_array = np.array(image)

    # Calculate the average brightness (scaled to 0-65535 for 16-bit)
    avg_brightness = np.mean(image_array)

    # Adjust min and max thresholds based on brightness
    adjustment_factor = avg_brightness / 65535  # Normalize to 0-1

    # Calculate dynamic min and max thresholds
    min_threshold = int(base_min * (1 - adjustment_factor))
    max_threshold = int(base_max * (1 - adjustment_factor))

    return min_threshold, max_threshold

if __name__ == "__main__":
    main()