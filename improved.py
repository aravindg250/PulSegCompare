from scripts.filePaths import tif_seg_output_resized_white, TubeMap_output_filepath
import numpy as np
from skimage import io
from scipy import ndimage
from PIL import Image, ImageSequence

def skeletonize_tiff_stack(file_path, output_path):
    # Open the multi-layer TIF stack using Pillow
    with Image.open(file_path) as img:
        skeletonized_stack = []

        # Iterate over each frame in the TIFF stack
        for frame in ImageSequence.Iterator(img):
            # Convert the frame to a numpy array
            image = np.array(frame)
            
            # Convert the image to binary (black: 0, white: 1)
            binary_image = (image == 0).astype(int)
            
            # Label connected components in the binary image
            labeled_array, num_features = ndimage.label(binary_image)
            
            # Create an empty image for the skeletonized version
            skeletonized_image = np.ones_like(image) * 255  # initialize as white background

            for region_label in range(1, num_features + 1):
                # Extract the black region and calculate the center of mass
                region = (labeled_array == region_label)
                center_of_mass = ndimage.center_of_mass(region)

                # Convert center of mass coordinates to integer for pixel location
                center_y, center_x = map(int, center_of_mass)
                
                # Place a black dot (0) at the center of each black region
                skeletonized_image[center_y, center_x] = 0

            # Append the skeletonized slice to the output stack
            skeletonized_stack.append(skeletonized_image)

    # Convert list of images to numpy array for saving as TIF
    skeletonized_stack = np.array(skeletonized_stack, dtype=np.uint8)
    io.imsave(output_path, skeletonized_stack)

# Example usage
skeletonize_tiff_stack(tif_seg_output_resized_white, 'output_skeletonized_file.tif')
