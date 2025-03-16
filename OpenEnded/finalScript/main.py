from ultralytics import YOLO
import cv2
import os
import numpy as np
import torch

# Set directory paths
data_path = '/Users/timothy/projects/Teebloc/OpenEnded/finalScript'
output_path = os.path.join(data_path, "output")
input_path = os.path.join(data_path, "input")  # in jpg

# Ensure required directories exist
os.makedirs(output_path, exist_ok=True)

# Load YOLO model
model = YOLO('/Users/timothy/projects/Teebloc/OpenEnded/runs/detect/train6/weights/best.pt')

# Create a white placeholder image
current_image = np.ones((1, 1654, 3), dtype=np.uint8) * 255  # Fixed width 1654px



# Counter for naming output images
counter = 1  

# Loop through each image in the input directory
for jpg_file in os.listdir(input_path):
    if jpg_file.endswith('.jpg'):
        image_path = os.path.join(input_path, jpg_file)

        # Read image with OpenCV
        image_np = cv2.imread(image_path)
        if image_np is None:
            print(f"Error loading image: {image_path}. Skipping.")
            continue

        # Run the model on the image
        results = model(image_np)

        # Convert results to tensors
        boxes = torch.tensor(results[0].boxes.xyxy)
        confs = torch.tensor(results[0].boxes.conf)
        classes = torch.tensor(results[0].boxes.cls)

        # Remove overlapping predictions using NMS
        indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.01)
        boxes = boxes[indices].tolist()
        confs = confs[indices].tolist()
        classes = classes[indices].tolist()

        # Sort bounding boxes by vertical position (y1)
        boxes.sort(key=lambda x: x[1])

        # Initialize top boundary
        top = 0

        # Loop through bounding boxes and extract regions
        for i, (box, conf, cls) in enumerate(zip(boxes, confs, classes)):
            if conf < 0.6:  # Confidence threshold
                continue

            x1, y1, x2, y2 = map(int, box)

            # Crop from the current top to the next bounding box's top
            next_image = image_np[top:y1, :]
            current_image = np.concatenate((current_image, next_image), axis=0)

            # Define output file path
            base_file_name = os.path.splitext(jpg_file)[0]
            output_file_path = os.path.join(output_path, f"{base_file_name}_{counter}.jpg")

            # Save the concatenated image after each step
            cv2.imwrite(output_file_path, current_image)
            print(f"✅ Saved image {counter}: {output_file_path}")
            current_image = np.ones((1, 1654, 3), dtype=np.uint8) * 255  # Fixed width 1654px

            # Update top to the current bounding box's top
            top = y1

            # Increment the counter for unique filenames
            counter += 1

        # Add the remaining bottom part of the image (from last bounding box to bottom)
        current_image = image_np[top:, :]

# Save the final remaining concatenation
output_file_path = os.path.join(output_path, f"{base_file_name}_{counter}.jpg")
cv2.imwrite(output_file_path, current_image)
print(f"✅ Saved final image {counter}: {output_file_path}")
