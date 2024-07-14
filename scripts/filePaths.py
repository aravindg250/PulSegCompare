import os
from pathlib import Path

#TubeMap Filepaths
TubeMapInitial = 'C:/Users/bennington/Desktop/research_24/Comparisons/Input/TubeMapInitial/binary_arteries1_postprocessed.tif'
fileName = Path(TubeMapInitial).stem
print(os.path.basename(TubeMapInitial)) # prints 'binary_arteries1.tif'
print(Path(TubeMapInitial).stem) # prints 'binary_arteries1'
TubeMap_output_filepath = 'C:/Users/bennington/Desktop/research_24/Comparisons/Output/TubeMapFinal/binary_arteries1_postprocessed_white.tif'


# Paths for input NRRD file and output NPY and TIFF files
nrrd_filepath = 'C:/Users/bennington/Desktop/research_24/Comparisons/Input/SegmentationsNRRD/MouseSegmentation2.nrrd'
npy_seg_output = 'C:/Users/bennington/Desktop/research_24/Comparisons/Output/SegmentationOutput/seg2/mouse_output_seg.npy'
tif_seg_output_resized = 'C:/Users/bennington/Desktop/research_24/Comparisons/Output/SegmentationOutput/seg2/resized/mouse_output_seg_resized5.tif'
tif_seg_output_resized_white = 'C:/Users/bennington/Desktop/research_24/Comparisons/Output/SegmentationOutput/seg2/white/mouse_output_seg_resized_white5.tif'


#Overlay Paths
overlay_output_tif_path = 'C:/Users/bennington/Desktop/research_24/Comparisons/Output/OverlayOutput/seg2/mouse_overlay_output5.tif'