import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO
from OCR_utils import has_leading_number  # Make sure this is available

def OEsegmentation(images, filenames):
    """
    Runs a fixed YOLO model + OCR-based filtering on input images,
    extracts regions, and saves output to a fixed path.

    Args:
        images (List[np.ndarray]): List of image arrays (BGR format).
        filenames (List[str]): List of image filenames (used for saving).
    """

    # Fixed model and output path
    model_path = '/Users/timothy/projects/Teebloc/OpenEnded/runs/detect/train6/weights/best.pt'
    output_path = '/Users/timothy/projects/Teebloc/OpenEnded/finalScript/output'
    os.makedirs(output_path, exist_ok=True)

    # Load model once
    model = YOLO(model_path)

    # Placeholder image
    current_image = np.ones((1, 1654, 3), dtype=np.uint8) * 255
    counter = 1

    for image_np, jpg_file in zip(images, filenames):
        results = model(image_np)
        boxes = torch.tensor(results[0].boxes.xyxy)
        confs = torch.tensor(results[0].boxes.conf)
        classes = torch.tensor(results[0].boxes.cls)

        indices = torch.ops.torchvision.nms(boxes, confs, iou_threshold=0.01)
        boxes = boxes[indices].tolist()
        confs = confs[indices].tolist()
        classes = classes[indices].tolist()

        boxes.sort(key=lambda x: x[1])  # Sort by top y value
        top = 0
        base_file_name = os.path.splitext(jpg_file)[0]

        for box, conf, cls in zip(boxes, confs, classes):
            x1, y1, x2, y2 = map(int, box)
            if conf < 0.3:
                continue
            elif conf < 0.8:
                cropped = image_np[y1:y2, 0:x2]
                if cropped.size == 0 or not has_leading_number(cropped):
                    continue

            segment = image_np[top:y1, :]
            current_image = np.concatenate((current_image, segment), axis=0)

            out_path = os.path.join(output_path, f"{base_file_name}_{counter}.jpg")
            cv2.imwrite(out_path, current_image)
            print(f"✅ Saved image {counter}: {out_path}")

            current_image = np.ones((1, 1654, 3), dtype=np.uint8) * 255
            top = y1
            counter += 1

        # Append the remaining bottom part
        current_image = np.concatenate((current_image, image_np[top:, :]), axis=0)

    final_path = os.path.join(output_path, f"{base_file_name}_{counter}.jpg")
    cv2.imwrite(final_path, current_image)
    print(f"✅ Saved final image {counter}: {final_path}")
