from scripts.nrrdTotif import nrrd_to_npy, npy_to_resized_tiff, change_region_to_white
from scripts.filePaths import TubeMapInitial, TubeMap_output_filepath, nrrd_filepath, npy_seg_output, tif_seg_output

# New dimensions
new_width = 417
new_height = 415
<<<<<<< HEAD
=======
tif_seg_output9 = 'C:/Users/bennington/Desktop/research_24/Comparisons/Output/SegmentationOutput/output_seg_resized9.tif'
>>>>>>> b73344158e395eb1f4cc30b90b6f353bf6964fff
region = (0, 0, 65, 55)  #(left, top, right, bottom) to be changed to white

# Convert NRRD to NPY
nrrd_to_npy(nrrd_filepath, npy_seg_output)



# Convert NPY to a single resized multi-page TIFF
<<<<<<< HEAD
npy_to_resized_tiff(npy_seg_output, tif_seg_output, new_width, new_height)
=======
npy_to_resized_tiff(npy_seg_output, tif_seg_output9, new_width, new_height)
>>>>>>> b73344158e395eb1f4cc30b90b6f353bf6964fff

# Change the region to white in all images
change_region_to_white(TubeMapInitial, TubeMap_output_filepath, region)
