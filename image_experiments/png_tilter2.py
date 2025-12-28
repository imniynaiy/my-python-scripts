from PIL import Image
import random
import numpy as np

def shuffle_half_pixels(input_path, output_path):
    # Open image and convert to RGBA
    img = Image.open(input_path).convert('RGBA')
    arr = np.array(img)
    h, w, c = arr.shape

    # Flatten pixel indices
    indices = [(y, x) for y in range(h) for x in range(w)]
    random.shuffle(indices)
    half = len(indices) // 2
    chosen = indices[:half]

    # Extract chosen pixels
    pixels = [arr[y, x].copy() for y, x in chosen]
    random.shuffle(pixels)

    # Place shuffled pixels back
    for (y, x), pix in zip(chosen, pixels):
        arr[y, x] = pix

    # Save new image
    Image.fromarray(arr).save(output_path)

# Example usage
shuffle_half_pixels('./temp/png_tilter/output2.jpg', './temp/png_tilter/output_shuffled.png')