from ultralytics import YOLO
import cv2
import os
from pdf2image import convert_from_path
import numpy as np
import torch


# Set directory paths
data_path = "/Users/timothy/projects/Teebloc/whitespace"
concatenated_path = os.path.join(data_path, "concatenated")
pdf_path = os.path.join(data_path, "pdf")

if not os.path.exists(concatenated_path):
    os.makedirs(concatenated_path)

# Load YOLO model
model = YOLO('/Users/timothy/projects/Teebloc/whitespace/runs/detect/train6/weights/best.pt')

# Convert PDF pages into individual JPG images
pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]

def crop(image, pdf_file, page_num, model):
    results = model(image)
    
    # Convert results to tensors
    boxes = torch.tensor(results[0].boxes.xyxy)
    confs = torch.tensor(results[0].boxes.conf)
    classes = torch.tensor(results[0].boxes.cls)
    
    # remove overlapping predictions
    indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.1)
    boxes = boxes[indices].tolist()
    confs = confs[indices].tolist()
    classes = classes[indices].tolist()

    # Since only one box is expected, get the first (and only) box
    if len(boxes) > 0:
        # If multiple boxes are detected (unexpected), select the most confident one
        if len(boxes) > 1:
            print(f"Warning: More than 1 box found on page {page_num} of {pdf_file}. Selecting the most confident one.")
            # Select the box with the highest confidence score
            max_conf_idx = confs.index(max(confs))
            box = boxes[max_conf_idx]
            predicted_class = classes[max_conf_idx]
        else:
            # Only one box as expected
            box = boxes[0]
            predicted_class = classes[0]

        # Skip cover pages (predicted_class == 2)
        if predicted_class == 2 or predicted_class == 3 or predicted_class == 1:
            return None
        
        # Extract coordinates and convert to integers
        x1, y1, x2, y2 = map(int, box)

        # Add slight margin to the y-axis
        margin = 10
        y1 = max(0, y1 - margin)
        y2 = min(image.shape[0], y2 + margin)

        # Crop only the y-axis, keeping full width
        cropped_image = image[y1:y2, :]

        # Return the cropped image
        return (predicted_class, cropped_image)
    else:
        return None

# Process each PDF file
for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_path, pdf_file)
    images = convert_from_path(pdf_file_path)
    concatenated_mcq = None  # Initialize concatenated image for each PDF file
    concatenated_oe = None
    concatenated_ans = None
    
    for page_num, image in enumerate(images):
        # Convert the PIL image to a numpy array (for YOLO compatibility)
        image_np = np.array(image)

        # Convert RGB to BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Generate cropped image using the crop function
        cropped_image = crop(image_np, pdf_file, page_num + 1, model)
        
        # If no prediction was made, crop() returns None, so skip this page
        if cropped_image is None:
            print(f"No crop for page {page_num + 1} of {pdf_file}. Skipping.")
            continue
        
        # If this is the first cropped image, initialize the concatenated image
        if cropped_image[0] == 0:
            if concatenated_oe is None:
                concatenated_oe = cropped_image[1]
            else:
                # Concatenate the new cropped image below the current concatenated image
                concatenated_oe = np.vstack((concatenated_oe, cropped_image[1]))
        elif cropped_image[0] == 1:
            if concatenated_mcq is None:
                concatenated_mcq = cropped_image[1]
            else:
                # Concatenate the new cropped image below the current concatenated image
                concatenated_mcq = np.vstack((concatenated_mcq, cropped_image[1]))
        elif cropped_image[0] == 3:
            if concatenated_ans is None:
                concatenated_ans = cropped_image[1]
            else:
                # Concatenate the new cropped image below the current concatenated image
                concatenated_ans = np.vstack((concatenated_ans, cropped_image[1]))
    # Save the concatenated image for this PDF file
    def save_concatenated_image(concatenated_image, pdf_file, concatenated_path, image_type):
        if concatenated_image is not None:
            concatenated_file_name = f"{os.path.splitext(pdf_file)[0]}_concatenated_{image_type}.jpg"
            concatenated_file_path = os.path.join(concatenated_path, concatenated_file_name)
            cv2.imwrite(concatenated_file_path, concatenated_image)
            print(f"Saved concatenated image: {concatenated_file_path}")
    save_concatenated_image(concatenated_mcq, pdf_file, concatenated_path, "mcq")
    save_concatenated_image(concatenated_oe, pdf_file, concatenated_path, "oe")
    save_concatenated_image(concatenated_ans, pdf_file, concatenated_path, "ans")

