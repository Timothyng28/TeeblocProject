from paddleocr import PaddleOCR
import cv2
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def has_leading_number(image_np: np.ndarray) -> bool:
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    results = ocr.ocr(image_rgb, cls=True)
    if results and results[0]:
        text = results[0][0][1][0].strip()
        return text and text[0].isdigit()
    return False
