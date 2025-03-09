import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import os

# Open file dialog to select an image
file_path = "dataset/train/images/0f7e5a9a-P5_Science_2023_SA2_Aitong_concatenated_oe.jpg"

# Load image
image = cv2.imread(file_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB (OpenCV loads in BGR)

# Get original dimensions
orig_h, orig_w = image.shape[:2]
print(f"Original size: {orig_w}x{orig_h}")

# Define target longest side
TARGET_LONGEST_SIDE = 5120

# Compute new dimensions while keeping aspect ratio
if orig_w > orig_h:
    new_w = TARGET_LONGEST_SIDE
    new_h = int((orig_h / orig_w) * new_w)
else:
    new_h = TARGET_LONGEST_SIDE
    new_w = int((orig_w / orig_h) * new_h)

# Resize image
resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)


output_path = os.path.join(os.path.dirname(file_path), "resized_image.jpg")

# Save the resized image
cv2.imwrite(output_path, resized_image)
print(f"✅ Resized image saved as: {output_path}")
