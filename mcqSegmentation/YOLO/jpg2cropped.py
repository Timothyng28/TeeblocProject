from ultralytics import YOLO
import cv2
import os
from PIL import Image
import numpy as np

# Load YOLO model
model = YOLO('mcqSegmentation/YOLO/runs/detect/train4/weights/best.pt')

# Set directory paths
data_path = os.getcwd()
images_path = os.path.join(data_path, "mcqSegmentation/YOLO/images") 
crop_path = os.path.join(data_path, "mcqSegmentation/YOLO/crop_image")

# Create crop directory if not exists
if not os.path.exists(crop_path):
    os.makedirs(crop_path)

# Process each image in the directory
for image_file in os.listdir(images_path):
    img_path = os.path.join(images_path, image_file)
    
    # Load image using PIL
    try:
        pil_img = Image.open(img_path)
        print(f"Loaded image using PIL with size: {pil_img.size}")
        
        # Convert PIL image to NumPy array
        img = np.array(pil_img)
        
        # Convert RGB to BGR (OpenCV format)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        print(f"Converted to OpenCV format with shape: {img.shape}")
    except Exception as e:
        print(f"Error: Failed to load image using PIL from {img_path}: {e}")
        continue
    
    # Run YOLO on the entire image
    try:
        results = model.predict(source=img, imgsz=img.shape[:2], conf=0.25)
        print(f"Detection results for {image_file}: {results}")
        print(f"Number of boxes detected: {len(results[0].boxes.xyxy)}")
    except Exception as e:
        print(f"Error: YOLO failed on image {img_path}: {e}")
        continue
    
    # Extract bounding boxes
    boxes = results[0].boxes.xyxy.tolist()

    # Crop and save each detected box
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers

        # Crop the image
        crop_img = img[y1:y2, x1:x2]

        # Save the cropped image
        file_name = os.path.join(crop_path, f"{image_file.rsplit('.', 1)[0]}_crop_{i}.jpg")
        cv2.imwrite(file_name, crop_img)
        print(f"Saved cropped image: {file_name}")
