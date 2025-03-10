from ultralytics import YOLO
import cv2
import os
import numpy as np
import torch

# Set directory paths
data_path = '/Users/timothy/projects/Teebloc/OpenEnded'
pseudo_label_path = os.path.join(data_path, "pseudo_label")
jpg_path = os.path.join(data_path, "images")

# Ensure required directories exist
os.makedirs(os.path.join(pseudo_label_path, "images"), exist_ok=True)
os.makedirs(os.path.join(pseudo_label_path, "annotations"), exist_ok=True)
os.makedirs(os.path.join(pseudo_label_path, "vis_img"), exist_ok=True)

# Load YOLO model
model = YOLO('/Users/timothy/projects/Teebloc/OpenEnded/runs/detect/train6/weights/best.pt')


def pseudo_label_images(image, image_filename, model):
    results = model(image)
    # convert results to tensors
    boxes = torch.tensor(results[0].boxes.xyxy)
    confs = torch.tensor(results[0].boxes.conf)
    classes = torch.tensor(results[0].boxes.cls)

    # remove overlapping predictions using NMS
    indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.01)
    boxes = boxes[indices].tolist()
    confs = confs[indices].tolist()
    classes = classes[indices].tolist()

    # Filter for low-confidence boxes (<= 0.75)
    filtered_data = []
    for box, conf, cls in zip(boxes, confs, classes):
        if conf > 0.75:  # Skip high confidence boxes
            continue
        filtered_data.append((box, conf, cls))

    # If there are no low-confidence bounding boxes, skip saving.
    if len(filtered_data) == 0:
        print(f"No low confidence bounding boxes for {image_filename}. Skipping saving.")
        return

    # Define file paths
    base_file_name = os.path.splitext(image_filename)[0]
    vis_image_file_path = os.path.join(pseudo_label_path, "vis_img", f"{base_file_name}_vis.jpg")


    # Create a copy of the image for visualization
    vis_image = image.copy()

    for box, conf, cls in filtered_data:
        x1, y1, x2, y2 = map(int, box)

        # Set color to red for all low-confidence boxes
        color = (0, 0, 255)

        # Draw bounding box on visualization image
        cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 2)
        
        # Add class ID and confidence text
        #label = f"{cls} {conf:.2f}"
        #cv2.putText(vis_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)

        # Normalize coordinates for YOLO format
        img_h, img_w = image.shape[:2]
        x_center = (x1 + x2) / 2 / img_w
        y_center = (y1 + y2) / 2 / img_h
        width = (x2 - x1) / img_w
        height = (y2 - y1) / img_h


    # Save the visualization image
    cv2.imwrite(vis_image_file_path, vis_image)
    print(f"Saved visualization image: {vis_image_file_path}")


# Process each JPG file in the directory
for jpg_file in os.listdir(jpg_path):
    if jpg_file.endswith('.jpg'):  # Ensure it's an image file
        image_path = os.path.join(jpg_path, jpg_file)
        
        # Read image with OpenCV
        image_np = cv2.imread(image_path)
        if image_np is None:
            print(f"Error loading image: {image_path}. Skipping.")
            continue

        # Generate pseudo labels
        pseudo_label_images(image_np, jpg_file, model)
