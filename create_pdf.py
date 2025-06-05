# create a pdf from a folder of jpgs. the content is organized by the subfolder name.
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def create_pdf_from_jpgs(root_folder, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    for subfolder in sorted(os.listdir(root_folder)):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            # Add section title
            c.setFont("Helvetica-Bold", 24)
            c.drawString(72, height - 72, subfolder)
            c.showPage()

            # Add images
            for img_file in sorted(os.listdir(subfolder_path)):
                if img_file.lower().endswith('.jpg'):
                    img_path = os.path.join(subfolder_path, img_file)
                    img = Image.open(img_path)
                    img_width, img_height = img.size

                    # Scale image to fit A4
                    scale = min(width / img_width, height / img_height)
                    new_width = img_width * scale
                    new_height = img_height * scale

                    x = (width - new_width) / 2
                    y = (height - new_height) / 2

                    c.drawImage(ImageReader(img), x, y, new_width, new_height)
                    c.showPage()

    c.save()

if __name__ == "__main__":
    # Change these paths as needed
    folder_with_jpgs = "/xxx/xxx/xxx"  # Replace with your folder path
    output_pdf_path = "output.pdf"
    create_pdf_from_jpgs(folder_with_jpgs, output_pdf_path)