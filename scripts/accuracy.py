from PIL import Image
from filePaths import TubeMap_output_filepath
# Open the multi-image TIFF file
tif = Image.open(TubeMap_output_filepath)
# Access the first image in the stack
tif.seek(0)
print("Image 0 (First Slice):")

# Convert the image to grayscale if it's not already
if tif.mode != 'L':
    tif = tif.convert('L')

print("Image Mode:" + tif.mode) # 'L' for grayscale

# Get image dimensions
width, height = tif.size
print(f"Image Dimensions: {width} x {height}")
# Create an empty array to store results
binary_array = []

# Threshold value to distinguish black and white
threshold = 128

# Iterate through each pixel in the first image
for y in range(height):
    row = []
    for x in range(width):
        # Get pixel value
        pixel_value = tif.getpixel((x, y))
        # Determine if pixel is black (1) or white (0)
        if pixel_value < threshold:
            row.append(1)  # Black
        else:
            row.append(0)  # White
    binary_array.append(row)

# Print the binary array
for row in binary_array:
    print(row)

def print_image(tif):
    # Print all pixel values of the first image
    for y in range(height):
        for x in range(width):
            pixel_value = tif.getpixel((x, y))
            print(f"Pixel value at ({x}, {y}): {pixel_value}")

