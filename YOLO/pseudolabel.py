from ultralytics import YOLO
import cv2
import os
from pdf2image import convert_from_path
import numpy as np


# Set directory paths
data_path = os.getcwd()
pseudo_label_path = os.path.join(data_path, "YOLO/pseudo_label")
pdf_path = os.path.join(data_path, "YOLO/pdf")

if not os.path.exists(pseudo_label_path):
    os.makedirs(pseudo_label_path)

# Load YOLO model
model = YOLO('runs/detect/train3/weights/best.pt')

# Convert PDF pages into individual JPG images
pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]

def pseudo_label_images(image, pdf_file, page_num, model):
    results = model(image)
    boxes = results[0].boxes.xyxy.tolist()  # Bounding box coordinates
    confs = results[0].boxes.conf.tolist()  # Confidence scores
    classes = results[0].boxes.cls.tolist()  # Class predictions

    # Define base file name for the page
    base_file_name = os.path.splitext(pdf_file)[0]
    image_file_name = f"{base_file_name}_page_{page_num}.jpg"
    txt_file_name = f"{base_file_name}_page_{page_num}.txt"
    vis_image_file_name = f"{base_file_name}_page_{page_num}_vis.jpg"  # Visualization image

    # Save the image
    image_file_path = os.path.join(pseudo_label_path, image_file_name)
    cv2.imwrite(image_file_path, image)
    print(f"Saved image: {image_file_path}")

    # Draw bounding boxes on a copy of the image
    vis_image = image.copy()

    # Save the annotations
    txt_file_path = os.path.join(pseudo_label_path, txt_file_name)
    with open(txt_file_path, 'w') as txt_file:
        for box, conf, cls in zip(boxes, confs, classes):
            # Filter out low-confidence detections
            if conf < 0.6:
                continue

            x1, y1, x2, y2 = map(int, box)  # Convert to integer for drawing
            class_id = int(cls)
            
            # assign colour to bounding box based on confidence
            if conf >= 0.8:
                color = (0, 255, 0)  # Green for high confidence
            else:
                color = (0, 0, 255)  # Green for bounding boxes

            cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 2)
            
            # Add label and confidence on top of the bounding box
            label = f"{class_id} {conf:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(vis_image, label, (x1, y1 - 10), font, 0.5, color, 2)

            img_h, img_w = image.shape[:2]
            x_center = (x1 + x2) / 2 / img_w
            y_center = (y1 + y2) / 2 / img_h
            width = (x2 - x1) / img_w
            height = (y2 - y1) / img_h

            # Write annotation in YOLO format
            txt_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    print(f"Saved annotations: {txt_file_path}")

    # Save the visualization image
    vis_image_file_path = os.path.join(pseudo_label_path, "vis_img")
    vis_image_file_path = os.path.join(vis_image_file_path, vis_image_file_name)
    cv2.imwrite(vis_image_file_path, vis_image)
    print(f"Saved visualization image: {vis_image_file_path}")


# Process each PDF file
for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_path, pdf_file)
    images = convert_from_path(pdf_file_path)
    for page_num, image in enumerate(images):
        # Convert the PIL image to a numpy array (for YOLO compatibility)
        image_np = np.array(image)

        # Convert RGB to BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Generate pseudo labels
        pseudo_label_images(image_np, pdf_file, page_num + 1, model)
