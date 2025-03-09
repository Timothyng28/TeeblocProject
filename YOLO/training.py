from ultralytics import YOLO
import torch
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
print(f"Using device: {device}")
model = YOLO('YOLO/runs/detect/train3/weights/best.pt')
results = model.train(data="YOLO/config.yaml", epochs=200, verbose = True, device = device, project = "YOLO/runs/detect")
