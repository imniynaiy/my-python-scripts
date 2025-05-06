import os
import random
from datetime import datetime
from PIL import Image
import colorsys

def generate_white_noise_png(width, height, box_size):
    # Create output directory if it doesn't exist
    output_dir = "./white_noise_png"
    os.makedirs(output_dir, exist_ok=True)

    # Adjust width and height to be multiples of box_size
    width = (width // box_size) * box_size
    height = (height // box_size) * box_size

    # Generate white noise image using HLS color systsem
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    for x in range(0, width, box_size):
        for y in range(0, height, box_size):
            h = random.randint(0, 360)  # Hue: 0-360
            l = random.randint(0, 100)  # Lightness: 0-100
            s = random.randint(0, 100)  # Saturation: 0-100

            # Convert HLS to RGB
            r, g, b = [int(c * 255) for c in colorsys.hls_to_rgb(h / 360, l / 100, s / 100)]

            for i in range(box_size):
                for j in range(box_size):
                    if x + i < width and y + j < height:
                        pixels[x + i, y + j] = (r, g, b)

    # Save the image with a timestamp as the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"white_noise_{timestamp}.png")
    image.save(file_path)
    print(f"White noise image saved to {file_path}")

if __name__ == "__main__":
    # Example usage
    width = int(input("Enter the width of the image: "))
    height = int(input("Enter the height of the image: "))
    box_size = int(input("Enter the size of the colored boxes: "))
    generate_white_noise_png(width, height, box_size)