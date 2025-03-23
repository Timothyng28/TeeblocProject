from paddleocr import PaddleOCR, draw_ocr
import os
import cv2
import numpy as np
from PIL import Image

# Paths
IMAGE_PATH = "OpenEnded/pseudo_label/cropped/"
OUTPUT_PATH = "OpenEnded/numbers/temp/"

# Ensure output directory exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Loop through all .jpg images in IMAGE_PATH
for image_file in os.listdir(IMAGE_PATH):
    if image_file.endswith('.jpg'):
        image_path = os.path.join(IMAGE_PATH, image_file)

        # Load image and convert to NumPy array
        image = Image.open(image_path).convert('RGB')
        image_np = np.array(image)  # Convert PIL to np.ndarray

        # Run OCR
        results = ocr.ocr(image_np, cls=True)

        # Extract text from first result if it exists
        if results and results[0]:
            text = results[0][0][1][0]
        else:
            text = ""

        # Print extracted text
        print(f"Extracted text from {image_file}: {text}")

        # Check if first character is a digit
        if text and text[0].isdigit():
            # Convert RGB to BGR for OpenCV saving
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

            # Save original image with a number
            output_path = os.path.join(OUTPUT_PATH, image_file)
            cv2.imwrite(output_path, image_bgr)
            print(f"Number detected and saved to {output_path}")

            # Visualization: draw bounding boxes
            boxes = [line[0] for line in results[0]]
            texts = [line[1][0] for line in results[0]]
            scores = [line[1][1] for line in results[0]]

            # You may need to update font path based on your OS
            font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"  # macOS example

            annotated_image = draw_ocr(image, boxes, texts, scores, font_path=font_path)
            annotated_image_bgr = cv2.cvtColor(np.array(annotated_image), cv2.COLOR_RGB2BGR)

            # Save visualization image
            vis_path = os.path.join(OUTPUT_PATH, f"vis_{image_file}")
            cv2.imwrite(vis_path, annotated_image_bgr)
            print(f"Visualization saved to {vis_path}")

        else:
            print(f"No number detected in {image_file}")
