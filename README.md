# NIOSH-SeniorDesign

Drone Image Processing and Path Planning
Overview
This project processes drone-captured images to:
Convert images to gridded grayscale.
Identify hazards based on brightness thresholds.
Cluster hazards and plan efficient drone paths.
Visualize and animate drone paths.

Features
Dynamic Hazard Detection: Adjusts brightness thresholds based on image properties.
Clustered Path Planning: Groups hazards and computes paths using KMeans and nearest-neighbor algorithms.
Visualization and Animation: Saves static and animated visualizations of drone paths.

Installation
Clone the Repository
git clone <repository-url>
cd <repository-folder>

Install Dependencies
pip install -r requirements.txt


Usage
Place drone images in the drone_images/ folder (16-bit PNG format).
Run the script:
 python main.py


Output
Grayscale Images: Saved in grayscale_drone_images/.
Hazard Images: Saved in potential_hazards/.
Hazard Coordinates: Text files saved in hazard_grid_coordinates/.
Drone Paths: Visualized and animated paths saved in drone_paths/.

Requirements
Python Version: Python 3.8+
Python Libraries:
numpy
Pillow
matplotlib
scikit-learn

Output Description
Grayscale Images: Images with overlaid grids for hazard detection.
Hazard Maps: Highlighted images and hazard coordinates.
Drone Paths: Images and GIF animations of drone navigation.

License
This project is licensed under [Your License Here].

SOP (Standard Operating Procedure)
1. Preparing the Environment
Install Python 3.8 or later.
Clone the repository and navigate to its folder.
Install required libraries:
 pip install -r requirements.txt


2. Preparing Inputs
Save drone images in the drone_images/ folder.
Ensure images are in 16-bit grayscale PNG format.
3. Running the Script
Open a terminal or command prompt.
Execute the script:
 python main.py


4. Analyzing Outputs
Grayscale Images: grayscale_drone_images/
Hazard Maps:
Images in potential_hazards/.
Coordinates in hazard_grid_coordinates/.
Drone Paths:
Visualized paths in drone_paths/.
5. Troubleshooting
Issue: Missing output folders.
 Solution: The script automatically creates necessary folders.
Issue: Unexpected errors.
 Solution: Ensure input images are valid 16-bit PNG files.
6. Maintenance
Regularly update libraries:
 pip install --upgrade -r requirements.txt


Back up output folders before running new analyses.

requirements.txt
Create a file named requirements.txt in the root directory with the following content:
numpy
Pillow
matplotlib
scikit-learn




