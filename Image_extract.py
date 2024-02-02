import fitz
import io
from PIL import Image

file = "./pdfs/INSPECTION_REPORT.pdf"
pdf_file = fitz.open(file)

# Iterate over pdf pages
for page_index in range(len(pdf_file)):
    # get the page itself
    page_img = pdf_file[page_index]
    image_list = page_img.get_images()
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(page_img.get_images(), start=1):
        # get the XREF of the image
        xref = img[0]
        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]
        # load it to PIL
        image = Image.open(io.BytesIO(image_bytes))
        # save it to local disk
        image.save(open(f"./pdfs/images/page{page_index+1}_image{image_index}.{image_ext}", "wb"))