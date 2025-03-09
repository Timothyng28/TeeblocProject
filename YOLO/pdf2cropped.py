from ultralytics import YOLO
import cv2
import os
from pdf2image import convert_from_path
import numpy as np


# Set directory paths
data_path = os.getcwd()
crop_path = os.path.join(data_path, "YOLO/crop_image")
pdf_path = os.path.join(data_path, "YOLO/pdf")

if not os.path.exists(crop_path):
    os.makedirs(crop_path)

model = YOLO('runs/detect/train3/weights/best.pt')

# Convert PDF pages into individual JPG images
pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]

def crop_images(image, pdf_file, page_num, model):
    results = model(image)
    boxes = results[0].boxes.xyxy.tolist()
    # Extract bounding boxes and confidence scores
    boxes = results[0].boxes.xyxy.tolist()
    confidences = results[0].boxes.conf.tolist()
    
    # Filter boxes with confidence greater than 70%
    filtered_boxes = [
        box for box, conf in zip(boxes, confidences) if conf > 0.7
    ]
    for crop_num, box in enumerate(filtered_boxes):
        x1, y1, x2, y2 = map(int, box)  
        crop_img = image[y1:y2, x1:x2]  

        # Define file name
        file_name = os.path.join(
            crop_path, 
            f"{os.path.splitext(pdf_file)[0]}_page_{page_num}_crop_{crop_num + 1}.jpg"
        )

        cv2.imwrite(file_name, crop_img)
        print(f"Saved: {file_name}")


for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_path, pdf_file)
    images = convert_from_path(pdf_file_path)
    for page_num, image in enumerate(images):
        # Convert the PIL image to a numpy array (for YOLO compatibility)
        image_np = np.array(image)

        # Convert RGB to BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Perform cropping
        crop_images(image_np, pdf_file, page_num + 1, model)


