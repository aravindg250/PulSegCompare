from scripts.filePaths import tif_seg_output_resized_white, TubeMap_output_filepath

# Open the TIFF stacks
reference_tif = Image.open(tif_seg_output_resized_white)
target_tif = Image.open(TubeMap_output_filepath)

resolution = 40 / 512



