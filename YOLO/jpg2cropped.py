from ultralytics import YOLO
import cv2
import os

model = YOLO('YOLO/runs/detect/train4/weights/best.pt')

data_path = os.getcwd()
images_path = os.path.join(data_path, "YOLO/images") 
crop_path = os.path.join(data_path, "YOLO/crop_image")

if not os.path.exists(crop_path):
    os.mkdir(crop_path)

for image_file in os.listdir(images_path):
    img_path = os.path.join(images_path, image_file)
    img = cv2.imread(img_path)
    results = model(img)
    boxes = results[0].boxes.xyxy.tolist()

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        crop_img = img[int(y1):int(y2), int(x1):int(x2)]
        file_name = os.path.join(crop_path, f"{image_file.rsplit('.', 1)[0]}_crop_{i}.jpg")
        cv2.imwrite(file_name, crop_img)