import os
import torch
from ultralytics import YOLO

# Ensure PyTorch uses CUDA (GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load YOLO model
model = YOLO('yolo11x.pt')

# Train YOLO using CUDA
results = model.train(
    data="config.yaml",  
    epochs=200,  
    verbose=True,  
    device=device,
    rect=True,  
    imgsz=5000,  
    batch=4,   
)
