# create a pdf from a folder of jpgs. the content is organized by the subfolder name.
import os
import sys
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
def create_pdf_from_jpgs(root_folder, output_pdf):
    image_files = []
    for subfolder in sorted(os.listdir(root_folder)):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            for img_file in sorted(os.listdir(subfolder_path)):
                if img_file.lower().endswith('.png'):
                    img_path = os.path.join(subfolder_path, img_file)
                    image_files.append(img_path)

    if not image_files:
        return

    # Open the first image to get its size
    first_img = Image.open(image_files[0])
    pdf_pages = []
    for img_path in image_files:
        img = Image.open(img_path)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        pdf_pages.append(img)

    pdf_pages[0].save(
        output_pdf,
        save_all=True,
        append_images=pdf_pages[1:],
        resolution=100.0,
    )

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_pdf.py <folder_with_jpgs> <output_pdf_path>")
        sys.exit(1)

    folder_with_jpgs = sys.argv[1]
    output_pdf_path = sys.argv[2]
    create_pdf_from_jpgs(folder_with_jpgs, output_pdf_path)