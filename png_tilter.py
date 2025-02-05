from PIL import Image
import numpy as np
import random

def shift_line(line, shift):
    return np.roll(line, shift, axis=0)

def process_image(input_path, output_path):
    # Open the image file
    img = Image.open(input_path)
    img_array = np.array(img)

    # Get image dimensions
    height, width, channels = img_array.shape

    # Create an empty array for the new image
    new_img_array = np.zeros_like(img_array)

    # Shift each line of pixels
    for i in range(height):
        shift = random.randint(-10, 10)
        new_img_array[i] = shift_line(img_array[i], shift)

    # Crop the center portion of the image
    start_x = 10
    end_x = width - 10
    cropped_img_array = new_img_array[:, start_x:end_x]

    # Convert the array back to an image
    new_img = Image.fromarray(cropped_img_array)



    # Save the new image
    new_img.save(output_path)

# Example usage
input_path = './png_tilter/input.jpg'
output_path = './png_tilter/output.jpg'
process_image(input_path, output_path)