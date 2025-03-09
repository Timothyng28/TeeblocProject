from ultralytics import YOLO
import cv2
import os
from pdf2image import convert_from_path
import numpy as np
import torch

# Set directory paths
data_path = "/Users/timothy/projects/Teebloc/whitespace"
output_dir = os.path.join(data_path, "OpenEndedjpg")  # This folder will store individual images
pdf_path = os.path.join(data_path, "pdf")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load YOLO model
model = YOLO('/Users/timothy/projects/Teebloc/whitespace/runs/detect/train6/weights/best.pt')

def crop(image, pdf_file, page_num, model):
    results = model(image)
    
    # Convert results to tensors
    boxes = torch.tensor(results[0].boxes.xyxy)
    confs = torch.tensor(results[0].boxes.conf)
    classes = torch.tensor(results[0].boxes.cls)
    
    # Remove overlapping predictions using Non-Maximum Suppression (NMS)
    indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.1)
    boxes = boxes[indices].tolist()
    confs = confs[indices].tolist()
    classes = classes[indices].tolist()

    if len(boxes) > 0:
        # If multiple boxes are detected, select the one with the highest confidence
        if len(boxes) > 1:
            print(f"Warning: More than 1 box found on page {page_num} of {pdf_file}. Selecting the most confident one.")
            max_conf_idx = confs.index(max(confs))
            box = boxes[max_conf_idx]
            predicted_class = classes[max_conf_idx]
        else:
            box = boxes[0]
            predicted_class = classes[0]

        # Only proceed if this is an open-ended image (predicted_class == 0)
        if predicted_class != 0:
            return None
        
        # Extract coordinates and convert to integers
        x1, y1, x2, y2 = map(int, box)

        # Add slight margin to the y-axis
        margin = 10
        y1 = max(0, y1 - margin)
        y2 = min(image.shape[0], y2 + margin)

        # Crop only in the y-axis while keeping the full width
        cropped_image = image[y1:y2, :]

        # Return the predicted class and the cropped image
        return (predicted_class, cropped_image)
    else:
        return None

# Process each PDF file
pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]

for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_path, pdf_file)
    images = convert_from_path(pdf_file_path)
    
    # Process each page in the PDF
    for page_num, image in enumerate(images):
        # Convert PIL image to numpy array for YOLO compatibility
        image_np = np.array(image)
        # Convert RGB to BGR (OpenCV uses BGR)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Generate cropped image using the crop function
        cropped_result = crop(image_np, pdf_file, page_num + 1, model)
        
        # If no prediction was made, crop() returns None, so skip this page
        if cropped_result is None:
            print(f"No open ended crop for page {page_num + 1} of {pdf_file}. Skipping.")
            continue
        
        # Save the open ended image individually as JPEG
        predicted_class, cropped_image = cropped_result
        output_filename = f"{os.path.splitext(pdf_file)[0]}_page{page_num+1}_open_ended.jpg"
        save_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(save_path, cropped_image)
        print(f"Saved open ended image: {save_path}")
