from ultralytics import YOLO
import torch
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
print(f"Using device: {device}")
model = YOLO('yolo11x.pt')
results = model.train(data="/Users/timothy/projects/Teebloc/OpenEnded/numbers/config-local.yaml", epochs=400, verbose = True, device = device, patience = 100, project = "OpenEnded/numbers", name = "OpenEnded/numbers/runs/detect")
