import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize, medial_axis
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

# Find regions in one slice
def find_regions(slice_data):
    if isinstance(slice_data, np.ndarray):
        labeled_slice = label(slice_data)
        regions = regionprops(labeled_slice)
        return regions
    else:
        raise ValueError("Input to find_regions is not a NumPy array.")

# Convert pixel area to physical area (micrometers squared)
def pixel_area_to_physical_area(pixel_area, resolution):
    return pixel_area * (resolution ** 2)

# Find connected vessel areas in the stack
def find_connected_vessel_areas(stack):
    if isinstance(stack, np.ndarray):
        vessel_areas = []
        for slice_data in stack:
            regions = find_regions(slice_data)
            vessel_areas.extend([pixel_area_to_physical_area(region.area, resolution) for region in regions])
        return vessel_areas
    else:
        raise ValueError("Input to find_connected_vessel_areas is not a NumPy array.")

# Calculate average area per slice
def average_area_per_slice(stack):
    if isinstance(stack, np.ndarray):
        areas = []
        for slice_data in stack:
            regions = find_regions(slice_data)
            areas.extend([pixel_area_to_physical_area(region.area, resolution) for region in regions])
        return np.mean(areas) if areas else 0
    else:
        raise ValueError("Input to average_area_per_slice is not a NumPy array.")

# Convert pixel perimeter to physical perimeter (micrometers)
def pixel_perimeter_to_physical_perimeter(pixel_perimeter, resolution):
    return pixel_perimeter * resolution

# Calculate circularity index
def circularity_index(region):
    perimeter = pixel_perimeter_to_physical_perimeter(region.perimeter, resolution)
    area = pixel_area_to_physical_area(region.area, resolution)
    if perimeter == 0:
        return 0
    return 4 * np.pi * (area / (perimeter ** 2))

# Calculate eccentricity index
def eccentricity_index(region):
    return region.eccentricity

# Compare to segmentation (overlap and offset)
def compare_segmentation(segmentation_stack, generated_stack):
    if isinstance(segmentation_stack, np.ndarray) and isinstance(generated_stack, np.ndarray):
        overlap = np.logical_and(segmentation_stack, generated_stack)
        offset = np.sum(np.abs(segmentation_stack - generated_stack))
        return overlap, offset
    else:
        raise ValueError("Inputs to compare_segmentation are not NumPy arrays.")

# Find areas with ~75% similarity in overlap region
def find_similar_areas(overlap, threshold=0.75):
    if isinstance(overlap, np.ndarray):
        similarity = (overlap.sum(axis=0) / np.count_nonzero(overlap, axis=0)) >= threshold
        return similarity
    else:
        raise ValueError("Input to find_similar_areas is not a NumPy array.")

# Skeletonize and find center of vessels
def skeletonize_and_find_centers(stack):
    if isinstance(stack, np.ndarray):
        skeletons = np.zeros_like(stack)
        for i in range(stack.shape[0]):
            skeleton, _ = medial_axis(stack[i], return_distance=True)
            skeletons[i] = skeleton
        centers = np.argwhere(skeletons)
        return skeletons, centers
    else:
        raise ValueError("Input to skeletonize_and_find_centers is not a NumPy array.")

# Compare accuracy of vessel size
def compare_vessel_size(segmentation_stack, skeletons):
    if isinstance(segmentation_stack, np.ndarray) and isinstance(skeletons, np.ndarray):
        segmentation_size = np.count_nonzero(segmentation_stack)
        skeleton_size = np.count_nonzero(skeletons)
        accuracy = skeleton_size / segmentation_size if segmentation_size != 0 else 0
        return accuracy
    else:
        raise ValueError("Inputs to compare_vessel_size are not NumPy arrays.")

# Save TIFF stack
def save_tiff_stack(stack, path):
    images = [Image.fromarray((frame * 255).astype(np.uint8)) for frame in stack]
    images[0].save(path, save_all=True, append_images=images[1:])

# Save binary overlay image with accepted/disregarded areas
def save_overlay_image(image, accepted, path):
    overlay = Image.fromarray((image * 255).astype(np.uint8)).convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for region in accepted:
        for coord in region.coords:
            draw.point((coord[1], coord[0]), fill="green")
    overlay.save(path)

# Save histogram
def save_histogram(data, bins, title, path):
    plt.figure()
    plt.hist(data, bins=bins, edgecolor='black')
    plt.title(title)
    plt.savefig(path)
    plt.close()

# Save bar chart
def save_bar_chart(data, bins, title, xlabel, ylabel, path):
    plt.figure()
    plt.hist(data, bins=bins, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(path)
    plt.close()

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

    connected_vessel_areas = find_connected_vessel_areas(segmentation_stack)
    average_area = average_area_per_slice(segmentation_stack)
    regions = find_regions(segmentation_stack[0])
    circularities = [circularity_index(region) for region in regions]
    eccentricities = [eccentricity_index(region) for region in regions]
    overlap, offset = compare_segmentation(segmentation_stack, generated_stack)
    similar_areas = find_similar_areas(overlap)
    skeletons, centers = skeletonize_and_find_centers(overlap)
    accuracy = compare_vessel_size(segmentation_stack, skeletons)

    # Save visualization results
    save_tiff_stack(segmentation_stack, "segmentation_stack.tiff")
    save_tiff_stack(generated_stack, "generated_stack.tiff")
    save_tiff_stack(overlap.astype(np.uint8), "overlap_stack.tiff")
    save_tiff_stack(skeletons.astype(np.uint8), "skeletons_stack.tiff")
    
    save_overlay_image(segmentation_stack[0], regions, "accepted_regions_overlay.png")
    save_histogram(connected_vessel_areas, bins=20, title="Connected Vessel Areas Distribution", path="connected_vessel_areas_histogram.png")
    save_histogram(circularities, bins=20, title="Circularity Indices Distribution", path="circularity_histogram.png")
    save_histogram(eccentricities, bins=20, title="Eccentricity Indices Distribution", path="eccentricity_histogram.png")
    save_bar_chart([accuracy], bins=[0, 1], title="Vessel Size Comparison Accuracy", xlabel="Accuracy", ylabel="Frequency", path="accuracy_bar_chart.png")

    print(f"Connected Vessel Areas (in micrometers^2): {connected_vessel_areas}")
    print(f"Average Area per Slice (in micrometers^2): {average_area:.2f}")
    print(f"Circularity Indices: {circularities}")
    print(f"Eccentricity Indices: {eccentricities}")
    print(f"Total Overlap (number of overlapping pixels): {np.sum(overlap)}")
    print(f"Total Offset (absolute difference between stacks): {offset}")
    print(f"Number of Similar Areas (areas with ~75% similarity): {np.sum(similar_areas)}")
    print(f"Accuracy of Vessel Size Comparison: {accuracy:.2f}")

if __name__ == "__main__":
    main()
