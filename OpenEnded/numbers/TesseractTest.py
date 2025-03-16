from PIL import Image
import pytesseract
import os
import cv2
import numpy as np

IMAGE_PATH = "OpenEnded/pseudo_label/cropped/"
OUTPUT_PATH = "OpenEnded/numbers/temp/"

# Ensure OUTPUT_PATH exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Loop through all images in IMAGE_PATH
for image_file in os.listdir(IMAGE_PATH):
    if image_file.endswith('.jpg'):
        # Open an image file
        image_path = os.path.join(IMAGE_PATH, image_file)
        image = Image.open(image_path)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image).strip()

        # Print extracted text
        print(f"Extracted text from {image_file}: {text}")

        # Check if text is not empty and if the first character is a number
        if text and text[0].isdigit():
            # Convert PIL Image to OpenCV format
            image_cv = np.array(image)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV

            # Save the image in OUTPUT_PATH
            output_image_path = os.path.join(OUTPUT_PATH, image_file)
            cv2.imwrite(output_image_path, image_cv)
            print(f"Number detected and saved in {output_image_path}")
        else:
            print(f"No number detected in {image_file}")
