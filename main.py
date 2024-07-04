from scripts.nrrdTotif import nrrd_to_npy, npy_to_resized_tiff, change_region_to_white
from scripts.filePaths import *
from scripts.overlay import overlay_tifs
# New dimensions
new_width = 417
new_height = 415
region = (0, 0, 65, 55)  #(left, top, right, bottom) to be changed to white

# Convert NRRD to NPY
nrrd_to_npy(nrrd_filepath, npy_seg_output)

# Convert NPY to a single resized multi-page TIFF
npy_to_resized_tiff(npy_seg_output, tif_seg_output_resized, new_width, new_height)

# Change the region to white in all images
change_region_to_white(TubeMapInitial, TubeMap_output_filepath, region)
change_region_to_white(tif_seg_output_resized, tif_seg_output_resized_white, region)

# Overlay the TIFF stacks
reference_tif_path = tif_seg_output_resized_white
target_tif_path = TubeMap_output_filepath
output_tif_path = overlay_output_tif_path

overlay_tifs(reference_tif_path, target_tif_path, output_tif_path)
