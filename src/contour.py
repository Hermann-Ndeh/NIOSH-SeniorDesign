from PIL import Image, ImageDraw
import numpy as np
import json
from scipy.ndimage import label

# Load the image
image_path = "potential_hazards/DJI_0554.JPG"  # Replace with your image path
original_image = Image.open(image_path).convert("RGB")
image_np = np.array(original_image)

# Identify red-highlighted areas (only pixels where red is dominant)
red_mask = (image_np[:, :, 0] > 150) & (image_np[:, :, 1] < 100) & (image_np[:, :, 2] < 100)

# Label connected components only in red-highlighted areas
labeled_array, num_features = label(red_mask)

# Prepare data structures for output
cluster_centers = []
contours = []

# Loop over each detected label to calculate cluster centers and contours
for label_num in range(1, num_features + 1):
    mask = (labeled_array == label_num)
    
    # Get coordinates of points in the current cluster
    coords = np.column_stack(np.where(mask))
    
    # Calculate the center of the cluster
    if len(coords) > 0:
        cX, cY = np.mean(coords, axis=0).astype(int)
        cluster_centers.append({"center": (cX, cY)})
        
        # Create a simple bounding box for the current cluster as a contour (faster than detailed contours)
        min_x, min_y = coords.min(axis=0)
        max_x, max_y = coords.max(axis=0)
        bounding_box = [(min_y, min_x), (min_y, max_x), (max_y, max_x), (max_y, min_x), (min_y, min_x)]
        contours.append(bounding_box)

# Draw contours on the original image
image_with_contours = original_image.copy()
draw = ImageDraw.Draw(image_with_contours)

# Draw each bounding box around the clusters with green lines
for contour in contours:
    draw.line(contour, fill="green", width=2)  # Closed polygon

# Save modified image and JSON output
output_image_path = "potential_hazards/image_with_clusters.jpg"  # Replace with your desired save path
output_json_path = "potential_hazards/cluster_centers.json"  # Replace with your desired save path

# Save the image with green contours
image_with_contours.save(output_image_path)

# Save JSON with cluster center coordinates
with open(output_json_path, "w") as json_file:
    json.dump(cluster_centers, json_file)

print("Image with clusters saved at:", output_image_path)
print("Cluster centers JSON saved at:", output_json_path)
