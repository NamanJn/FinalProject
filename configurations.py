import os

# cv2.imshow image size increase (x-axis) 
width_multiple_to_increase = 2

# cv2.imshow image size increase (y-axis) 
height_multiple_to_increase = 2



# frames_per_second
fps = 10

# directories
# contour images directory
contour_images_dir = "contour_imgs"

# corrected data directory
corrected_data_dir = "corrected_data"

# validation_results_directory
validation_results_dir = "validation_results"

# debugging images directory
debug_images_dir = "debug_imgs"

# raw images directory
raw_imgs_dir = "raw_imgs"

# data directory
data_dir = "data"

# complex video directory
complex_video_dir = "complex_collision_vids"

# simple video directory
simple_collision_dir = "simple_collision_vids"

# simple video directory
collision_dir = "collision_vids"

# results output directory
output_dir = "output"
# data set column names
col_names = ['frame_number', 'fly', 'positionx', 'positiony', 'area', 'grayscale', 'width']

# column values for collision rows
collision_value = 50

# File paths
# this file contains the data of the number of contours per frame.
rle_data_file = os.path.join(data_dir, "csv.csv")

# this file contains the position data of the number of contours per frame.

data_file = os.path.join(data_dir, "data.csv")

# This is to create the simple and complex collisions.
interCollisionTime = 2 # This is in seconds