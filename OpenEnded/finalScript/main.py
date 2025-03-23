import os
from pdf_crop_utils import extract_open_ended_crops_from_pdf_bytes
from OEsegmentation_utils import OEsegmentation

# === Setup paths ===
data_path = '/Users/timothy/projects/Teebloc/OpenEnded/finalScript'
input_path = os.path.join(data_path, "input")
output_path = os.path.join(data_path, "output")
os.makedirs(output_path, exist_ok=True)

# === Get all PDFs ===
pdf_files = [f for f in os.listdir(input_path) if f.endswith('.pdf')]

if not pdf_files:
    print("🚫 No PDF files found in input directory.")
else:
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_path, pdf_file)
        print(f"\n📄 Processing: {pdf_file}")

        # Read as bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # Step 1: Crop using YOLO
        cropped_images = extract_open_ended_crops_from_pdf_bytes(pdf_bytes, pdf_name=pdf_file)

        if not cropped_images:
            print(f"⚠️ No open-ended content detected in {pdf_file}")
            continue

        # Step 2: Generate synthetic filenames
        filenames = [f"{os.path.splitext(pdf_file)[0]}_page{i+1}.jpg" for i in range(len(cropped_images))]

        # Step 3: Run segmentation (includes OCR)
        OEsegmentation(cropped_images, filenames)

        print(f"✅ Done: {pdf_file}")
