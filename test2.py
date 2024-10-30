import numpy as np
from PIL import Image
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize
import pandas as pd
import matplotlib.pyplot as plt
from scripts.filePaths import *

# Define the resolution (micrometers per pixel)
resolution = 40 / 512  # Example: 40 microns over 512 pixels, adjust as needed

# Function to load TIFF stack
def load_tiff_stack(tiff_path):
    print(f"Attempting to load TIFF stack from: {tiff_path}")
    try:
        img = Image.open(tiff_path)
        frames = []
        while True:
            frame = np.array(img)
            if frame.ndim == 2:  # Ensure it is a 2D image
                print(f"Loaded frame of type: {type(frame)} and shape: {frame.shape}")
                frames.append(frame)
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        print(f"Error loading TIFF stack: {e}")
        return None
    print(f"Total frames loaded: {len(frames)}")
    return np.stack(frames, axis=0)

# Ensure binary images
def ensure_binary(image):
    if isinstance(image, np.ndarray):
        print(f"Ensuring binary for image of shape: {image.shape}")
        return (image > 0).astype(np.uint8)
    else:
        raise ValueError("Input to ensure_binary is not a NumPy array.")

# Skeletonize and find centerlines for one slice
def skeletonize_and_find_centerlines(slice_data):
    skeleton = skeletonize(slice_data > 0)  # Ensure binary input for skeletonization
    centers = np.argwhere(skeleton)
    return centers

# Function to extract centerlines of each vessel in each slice and put in a table
def extract_centerlines_table(stack):
    if isinstance(stack, np.ndarray):
        table_data = []
        for slice_index, slice_data in enumerate(stack):
            centers = skeletonize_and_find_centerlines(slice_data)
            for center in centers:
                table_data.append({
                    "Slice": slice_index,
                    "X": center[1],  # Column index
                    "Y": center[0]   # Row index
                })
        centerlines_table = pd.DataFrame(table_data)
        return centerlines_table
    else:
        raise ValueError("Input to extract_centerlines_table is not a NumPy array.")

# Function to visualize centerlines table using Matplotlib
def visualize_centerlines_table(centerlines_table):
    if not isinstance(centerlines_table, pd.DataFrame):
        raise ValueError("Input to visualize_centerlines_table is not a pandas DataFrame.")
    
    num_slices = centerlines_table["Slice"].nunique()
    cols = 5
    rows = (num_slices // cols) + (1 if num_slices % cols != 0 else 0)
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 3))
    axes = axes.flatten()
    
    for slice_idx in range(num_slices):
        ax = axes[slice_idx]
        slice_data = centerlines_table[centerlines_table["Slice"] == slice_idx]
        ax.scatter(slice_data["X"], slice_data["Y"], s=1)
        ax.set_title(f'Slice {slice_idx}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.invert_yaxis()  # To match image coordinates
        ax.axis('equal')
    
    # Remove empty subplots
    for idx in range(num_slices, len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    plt.show()

# Main function to run all steps
def main():
    # Overlay the TIFF stacks
    reference_tif_path = tif_seg_output_resized_white
    target_tif_path = TubeMap_output_filepath

    segmentation_path = reference_tif_path
    generated_path = target_tif_path
    
    segmentation_stack = load_tiff_stack(segmentation_path)
    generated_stack = load_tiff_stack(generated_path)

    # Ensure the stacks are loaded correctly
    if isinstance(segmentation_stack, np.ndarray):
        print(f"Loaded segmentation stack of type: {type(segmentation_stack)} and shape: {segmentation_stack.shape}")
    else:
        raise ValueError("Failed to load segmentation stack as a NumPy array.")

    if isinstance(generated_stack, np.ndarray):
        print(f"Loaded generated stack of type: {type(generated_stack)} and shape: {generated_stack.shape}")
    else:
        raise ValueError("Failed to load generated stack as a NumPy array.")

    # Ensure stacks are binary
    segmentation_stack = ensure_binary(segmentation_stack)
    generated_stack = ensure_binary(generated_stack)

    # Extract centerlines table
    centerlines_table = extract_centerlines_table(segmentation_stack)
    
    # Visualize centerlines table
    visualize_centerlines_table(centerlines_table)

if __name__ == "__main__":
    main()
