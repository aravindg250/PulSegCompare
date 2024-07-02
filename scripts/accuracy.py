from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
from filePaths import tif_seg_output, TubeMap_output_filepath


# Open the TIFF stacks
reference_tif = Image.open(tif_seg_output)
target_tif = Image.open(TubeMap_output_filepath)

# Check if the number of frames in both stacks are the same
assert reference_tif.n_frames == target_tif.n_frames, "The number of frames in the stacks must be the same."

pixel_differences = []
# mse_differences = []
# ssim_differences = []
percent_differences = []


for i in range(reference_tif.n_frames):
    reference_tif.seek(i)
    target_tif.seek(i)

    # Convert the images to numpy arrays
    reference_frame = np.array(reference_tif)
    target_frame = np.array(target_tif)

    # Check if the dimensions of the frames are the same
    assert reference_frame.shape == target_frame.shape, "The dimensions of the frames must be the same."

    # Calculate the difference
    difference = target_frame - reference_frame
    # Pixel Differences per Slice: Number of differing pixels.
    pixel_difference = np.sum(difference != 0)
    
    # MSE Differences per Slice: Mean Squared Error.
    mse_difference = np.mean(np.square(difference))
    # SSIM Differences per Slice: Structural Similarity Index.
    ssim_difference = ssim(reference_frame, target_frame, data_range=target_frame.max() - target_frame.min(), multichannel=True)
    
    # Calculate total number of pixels in the slice
    total_pixels = reference_frame.shape[0] * reference_frame.shape[1]

    percent_differences.append((pixel_difference / total_pixels) * 100)
    pixel_differences.append(pixel_difference)
    # mse_differences.append(mse_difference)
    # ssim_differences.append(ssim_difference)
    # total_pixel_differences.append(total_pixel_difference)

# ------------------------------------------------
# Print the results
# print("Pixel Differences per Slice:")
# print(pixel_differences)
# print("Total Pixels per Slice:")
# print(total_pixels)
# print("Percent Differences per Slice:")
# print(percent_differences)
# ------------------------------------------------
total_pixel_difference = 0
for i in range(len(pixel_differences)):
    # print("Slice", i, "Pixel Difference:", pixel_differences[i])
    total_pixel_difference += pixel_differences[i]
    
avg_pixel_difference = total_pixel_difference / len(pixel_differences)
print("Average Pixel Difference:")
print(avg_pixel_difference)
# ------------------------------------------------
total_percent_difference = 0
for i in range(len(percent_differences)):
    # print("Slice", i, "Percent Difference:", percent_differences[i])
    total_percent_difference += percent_differences[i]
    
avg_percent_difference = total_percent_difference / len(percent_differences)
print("Average Percent Difference:")
print(avg_percent_difference)

'''
histagram of slice errors
finding the size fo the vessel 

'''