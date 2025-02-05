import sys
import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_jpeg(pdf_path, output_dir):
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历PDF的每一页
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        
        # 获取输出文件名
        output_filename = f"page_{page_num + 1}.jpeg"
        output_path = os.path.join(output_dir, output_filename)
        
        # 使用Pillow保存为JPEG
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(output_path, "JPEG")
    
    print(f"Successfully converted {pdf_path} to JPEG files in {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <pdf_path> <output_dir>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    pdf_to_jpeg(pdf_path, output_dir)
