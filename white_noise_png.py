import os
import random
from datetime import datetime
from PIL import Image

def generate_white_noise_png(width, height):
    # Create output directory if it doesn't exist
    output_dir = "./white_noise_png"
    os.makedirs(output_dir, exist_ok=True)

    # Generate white noise image
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pixels[x, y] = (r, g, b)

    # Save the image with a timestamp as the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"white_noise_{timestamp}.png")
    image.save(file_path)
    print(f"White noise image saved to {file_path}")

if __name__ == "__main__":
    # Example usage
    width = int(input("Enter the width of the image: "))
    height = int(input("Enter the height of the image: "))
    generate_white_noise_png(width, height)