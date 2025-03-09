import os
import fitz  

output_folder = "images"
pdf_folder = "pdf"

    # Iterate through all PDF files in the folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        pdf_document = fitz.open(pdf_path)

        # Iterate through each page in the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Load the page
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Render page to an image

            # Save the image as a JPEG
            image_filename = f"{os.path.splitext(pdf_file)[0]}_page_{page_num + 1}_CA.jpg"
            image_path = os.path.join(output_folder, image_filename)
            pix.save(image_path)

            print(f"Saved: {image_path}")

        pdf_document.close()

    

