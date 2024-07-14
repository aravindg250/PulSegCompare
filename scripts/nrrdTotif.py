import nrrd
import numpy as np
from PIL import Image, ImageSequence
import os

# Load NRRD file
def nrrd_to_npy(nrrd_filepath, npy_filepath):
    data, header = nrrd.read(nrrd_filepath)
    axial_data = np.transpose(data, (2, 1, 0))
    np.save(npy_filepath, axial_data)
    print(f"NRRD data saved as NPY file at {npy_filepath}")

# Resize each slice in the NPY data and save as a single multi-page TIFF

def npy_to_resized_tiff(npy_filepath, tiff_filepath, new_width, new_height):
    data = np.load(npy_filepath)
    
    # Normalize the data to fit in uint8 range
    data = (data - data.min()) / (data.max() - data.min()) * 255
    data = data.astype(np.uint8)
    
    data = 255 - data
    
    # Get original dimensions
    original_depth, original_height, original_width = data.shape
    print(f"Original dimensions: {original_width} x {original_height} x {original_depth}")
    
    # Calculate padding
    pad_top = new_height - original_height
    pad_left = new_width - original_width
    print(f"Padding: top={pad_top}, left={pad_left}")

    half_pad_top = int(pad_top / 2)
    half_pad_left = int(pad_left / 2)
    print(f"Half padding: top={half_pad_top}, left={half_pad_left}")
    # Resize each slice
    resized_slices = []
    for i in range(data.shape[0]):
        frame = Image.fromarray(data[i])
        new_frame = Image.new("L", (new_width, new_height), color=255)  # 'L' mode for grayscale
        new_frame.paste(frame, (0, 0))  # Paste at top-left corner
        resized_slices.append(new_frame)
    
    # # Print every pixel value of the first slice
    # for i in range(resized_slices[0].size[1]):
    #     for j in range(resized_slices[0].size[0]):
    #         print(resized_slices[0].getpixel((j, i)), end=" ")
    #     print()
    
    # Ensure the file has the correct extension
    if not tiff_filepath.lower().endswith(('.tif', '.tiff')):
        raise ValueError("The output file must have a .tif or .tiff extension.")
    
    # Save all slices as a multi-page TIFF
    resized_slices[0].save(tiff_filepath, save_all=True, append_images=resized_slices[1:])
    print(f"All slices saved as a resized multi-page TIFF at {tiff_filepath}")

# Example usage
# npy_to_resized_tiff('path_to_input.npy', 'path_to_output.tiff', new_width, new_height)

def change_region_to_white(tiff_filepath, output_filepath, region):

    # Open the TIFF stack
    img = Image.open(tiff_filepath)
    
    # Create a list to hold all the modified frames
    modified_frames = []
    
    # Iterate through each frame in the TIFF stack
    for frame in ImageSequence.Iterator(img):
        # Convert frame to 'L' mode if it's not already (for grayscale)
        frame = frame.convert("L")
        
        # Create a copy of the frame to modify
        modified_frame = frame.copy()
        
        # Create a white region
        white_region = Image.new("L", (region[2] - region[0], region[3] - region[1]), color=255)
        
        # Paste the white region onto the modified frame
        modified_frame.paste(white_region, region)
        
        # Add the modified frame to the list
        modified_frames.append(modified_frame)
    
    # Save the modified frames as a new multi-page TIFF
    modified_frames[0].save(output_filepath, save_all=True, append_images=modified_frames[1:])
    print(f"All frames saved with the modified region to a multi-page TIFF at {output_filepath}")

