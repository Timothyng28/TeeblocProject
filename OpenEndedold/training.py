import os
import torch
from ultralytics import YOLO

# Ensure PyTorch uses CUDA (GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load YOLO model
model = YOLO('yolo11n.pt')

# Train YOLO using CUDA
results = model.train(
    data="/Users/timothy/projects/Teebloc/OpenEnded/config.yaml",  
    epochs=15,  
    verbose=True,  
    device=device,  # Force CUDA
    rect=True,  
    imgsz=4096,  
    batch=4,  
    project="/Users/timothy/projects/Teebloc/OpenEnded/runs"
)
