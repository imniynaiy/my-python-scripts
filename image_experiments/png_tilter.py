import numpy as np
from PIL import Image
import random

def shift_line(line, shift):
    return np.roll(line, shift, axis=0)

def shift_column(column, shift):
    return np.roll(column, shift, axis=0)

def shift_color(line, shift):
    return np.roll(line, shift, axis=1)

def process_image(input_path, output_path, variance=10, crop=10):
    # Open the image file
    img = Image.open(input_path)
    img_array = np.array(img)

    # Get image dimensions
    height, width, channels = img_array.shape

    # Create an empty array for the new image
    new_img_array = np.zeros_like(img_array)

    # Shift each line of pixels horizontally
    for i in range(height):
        shift = int(np.random.normal(0, variance))
        new_img_array[i] = shift_line(img_array[i], shift)

    # Shift each column of pixels vertically
    for j in range(width):
        shift = int(np.random.normal(0, variance))
        new_img_array[:, j] = shift_column(new_img_array[:, j], shift)

    # # Shift each line of pixels' color channels
    # for i in range(height):
    #     shift = int(np.random.normal(0, variance))
    #     new_img_array[i] = shift_color(new_img_array[i], shift)

    # Crop the center portion of the image
    start_x = crop
    end_x = width - crop
    start_y = crop
    end_y = height - crop
    cropped_img_array = new_img_array[start_y:end_y, start_x:end_x]

    # Convert the array back to an image
    new_img = Image.fromarray(cropped_img_array)

    # Save the new image
    new_img.save(output_path)

# Example usage
variance = 10
crop = 20
input_path = './temp/png_tilter/input.jpg'
output_path = './temp/png_tilter/output2.jpg'
process_image(input_path, output_path, variance, crop)