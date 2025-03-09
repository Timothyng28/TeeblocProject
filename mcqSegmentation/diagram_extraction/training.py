from ultralytics import YOLO
import torch
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
print(f"Using device: {device}")
model = YOLO('diagram_extraction/train3/weights/best.pt')
results = model.train(data="diagram_extraction/config.yaml", epochs=200,project = "diagram_extraction", verbose = True, device = device)
