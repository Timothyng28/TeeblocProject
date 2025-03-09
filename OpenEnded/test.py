from ultralytics import YOLO
import cv2
import os

# Load YOLO model
model = YOLO('yolo11n.pt')  # Change to your model file

# Define image paths
image_path = "test.jpg"  # Change to your image file
save_path = os.path.join(os.getcwd(), "test_vis.jpg")  # Saves in current directory

# Load image
image = cv2.imread(image_path)

# Run YOLO inference
results = model(image)

# Draw bounding boxes
for box in results[0].boxes.xyxy.tolist():
    x1, y1, x2, y2 = map(int, box[:4])
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Save visualization
cv2.imwrite(save_path, image)
print(f"Saved visualization: {save_path}")
