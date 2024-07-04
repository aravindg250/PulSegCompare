from PIL import Image
import numpy as np

def overlay_tiffs(reference_path, target_path, output_path):
    # Open the TIFF stacks
    reference_tif = Image.open(reference_path)
    target_tif = Image.open(target_path)

    # Check if the number of frames in both stacks are the same
    assert reference_tif.n_frames == target_tif.n_frames, "The number of frames in the stacks must be the same."

    for i in range(reference_tif.n_frames):
        reference_tif.seek(i)
        target_tif.seek(i)

        # Convert the images to numpy arrays
        reference_frame = np.array(reference_tif)
        target_frame = np.array(target_tif)

        # Check if the dimensions of the frames are the same
        assert reference_frame.shape == target_frame.shape, "The dimensions of the frames must be the same."

        # Create an RGB image for the overlay
        overlay_frame = np.zeros((reference_frame.shape[0], reference_frame.shape[1], 3), dtype=np.uint8)

        # Define colors
        green = [0, 255, 0]
        red = [255, 0, 0]

        # Set the overlay colors based on conditions
        overlay_frame[(reference_frame == 0) & (target_frame == 255)] = green
        overlay_frame[(reference_frame == 255) & (target_frame == 0)] = red
        overlay_frame[(reference_frame == 255) & (target_frame == 255)] = [255, 255, 255]
        overlay_frame[(reference_frame == 0) & (target_frame == 0)] = [0, 0, 0]

        # Convert overlay to an Image object and save it
        overlay_image = Image.fromarray(overlay_frame)

        # Save the overlay frame to a new TIFF stack
        if i == 0:
            overlay_image.save(output_path, save_all=True, append_images=[overlay_image])
        else:
            overlay_image.save(output_path, save_all=True, append_images=[overlay_image], append=True)



