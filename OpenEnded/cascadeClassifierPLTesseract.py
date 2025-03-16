import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO

# Set directory paths
data_path = '/Users/timothy/projects/Teebloc/OpenEnded'
pseudo_label_path = os.path.join(data_path, "pseudo_label")
jpg_path = os.path.join(data_path, "images")

# Ensure required directories exist
os.makedirs(os.path.join(pseudo_label_path, "cropped"), exist_ok=True)

# Load YOLO model
model = YOLO('/Users/timothy/projects/Teebloc/OpenEnded/runs/detect/train6/weights/best.pt')

def pseudo_label_images(image, image_filename, model):
    results = model(image)
    
    # Convert results to tensors
    boxes = torch.tensor(results[0].boxes.xyxy)
    confs = torch.tensor(results[0].boxes.conf)
    classes = torch.tensor(results[0].boxes.cls)

    # Remove overlapping predictions using NMS
    indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.01)
    boxes = boxes[indices].tolist()
    confs = confs[indices].tolist()
    classes = classes[indices].tolist()

    # Filter for low-confidence boxes (<= 0.75)
    filtered_data = []
    for box, conf, cls in zip(boxes, confs, classes):
        if conf > 0.6:  # Skip high confidence boxes
            continue
        filtered_data.append((box, conf, cls))

    # If there are no low-confidence bounding boxes, skip saving
    if len(filtered_data) == 0:
        print(f"No low confidence bounding boxes for {image_filename}. Skipping saving.")
        return

    # Define base file name for saving cropped images
    base_file_name = os.path.splitext(image_filename)[0]

    for i, (box, conf, cls) in enumerate(filtered_data):
        x1, y1, x2, y2 = map(int, box)

        # Crop the detected object
        cropped_image = image[y1:y2, x1:x2]

        # Save cropped image
        cropped_image_file_path = os.path.join(pseudo_label_path, "cropped", f"{base_file_name}_cropped_{i}.jpg")
        cv2.imwrite(cropped_image_file_path, cropped_image)
        print(f"Saved cropped image: {cropped_image_file_path}")

# Process each JPG file in the directory
for jpg_file in os.listdir(jpg_path):
    if jpg_file.endswith('.jpg'):  # Ensure it's an image file
        image_path = os.path.join(jpg_path, jpg_file)
        
        # Read image with OpenCV
        image_np = cv2.imread(image_path)
        if image_np is None:
            print(f"Error loading image: {image_path}. Skipping.")
            continue

        # Generate pseudo labels and save cropped images
        pseudo_label_images(image_np, jpg_file, model)
