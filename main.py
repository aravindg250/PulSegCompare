from scripts.nrrdTotif import nrrd_to_npy, npy_to_resized_tiff, change_region_to_white
from scripts.filePaths import TubeMapInitial, TubeMap_output_filepath, nrrd_filepath, npy_filepath, tiff_filepath

# New dimensions
new_width = 417
new_height = 415

region = (0, 0, 65, 55)  #(left, top, right, bottom) to be changed to white

# Convert NRRD to NPY
nrrd_to_npy(nrrd_filepath, npy_filepath)

# Convert NPY to a single resized multi-page TIFF
npy_to_resized_tiff(npy_filepath, tiff_filepath, new_width, new_height)

# Change the region to white in all images
change_region_to_white(TubeMapInitial, TubeMap_output_filepath, region)
