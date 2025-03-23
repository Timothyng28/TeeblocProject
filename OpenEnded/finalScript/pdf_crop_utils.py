import cv2
import torch
import numpy as np
from pdf2image import convert_from_bytes
from ultralytics import YOLO

# Load YOLO model globally
model = YOLO('/Users/timothy/projects/Teebloc/whitespace/runs/detect/train6/weights/best.pt')

def cropOE(image, pdf_name, page_num):
    results = model(image)
    
    boxes = torch.tensor(results[0].boxes.xyxy)
    confs = torch.tensor(results[0].boxes.conf)
    classes = torch.tensor(results[0].boxes.cls)

    indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.1)
    boxes = boxes[indices].tolist()
    confs = confs[indices].tolist()
    classes = classes[indices].tolist()

    if not boxes:
        return None

    max_conf_idx = confs.index(max(confs))
    box = boxes[max_conf_idx]
    predicted_class = classes[max_conf_idx]

    if predicted_class != 0:
        return None

    x1, y1, x2, y2 = map(int, box)
    y1 = max(0, y1 - 10)
    y2 = min(image.shape[0], y2 + 10)

    return image[y1:y2, :]

def extract_open_ended_crops_from_pdf_bytes(pdf_bytes, pdf_name="unknown.pdf"):
    """
    Extracts cropped open-ended regions from a PDF loaded from memory (bytes).

    Args:
        pdf_bytes (bytes): The full PDF file in bytes (e.g. from open(file, 'rb').read()).
        pdf_name (str): Optional name for logging/debugging.

    Returns:
        List[np.ndarray]: Cropped image regions as NumPy arrays.
    """
    print(f"\n📄 Processing in-memory PDF: {pdf_name}")
    pages = convert_from_bytes(pdf_bytes)
    cropped_images = []

    for page_num, pil_image in enumerate(pages):
        image_np = np.array(pil_image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        cropped = cropOE(image_bgr, pdf_name, page_num + 1)

        if cropped is not None:
            cropped_images.append(cropped)
        else:
            print(f"  ⏭️ Page {page_num+1}: No valid open-ended region.")

    return cropped_images
