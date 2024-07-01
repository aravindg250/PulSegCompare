import os
from pathlib import Path

#TubeMap Filepaths
TubeMapInitial = 'C:/Users/bennington/Desktop/research/pythonFiles/Input/TubeMapInitial/binary_arteries1.tif'
fileName = Path(TubeMapInitial).stem
print(os.path.basename(TubeMapInitial)) # prints 'binary_arteries1.tif'
print(Path(TubeMapInitial).stem) # prints 'binary_arteries1'
TubeMap_output_filepath = 'C:/Users/bennington/Desktop/research/pythonFiles/Output/TubeMapFinal/' + fileName + '.tif'


# Paths for input NRRD file and output NPY and TIFF files
nrrd_filepath = 'C:/Users/bennington/Desktop/research/pythonFiles/Input/SegmentationsNRRD/Threshold_Above.nrrd'
npy_filepath = 'C:/Users/bennington/Desktop/research/pythonFiles/Output/SegmentationOutput/output_seg.npy'
tiff_filepath = 'C:/Users/bennington/Desktop/research/pythonFiles/Output/SegmentationOutput/output_seg_resized.tif'