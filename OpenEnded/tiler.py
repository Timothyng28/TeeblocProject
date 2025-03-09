from sahi.slicing import slice_coco

slice_coco(
    coco_annotation_file_path="dataset/result.json",
    image_dir="dataset",
    output_coco_annotation_file_name="tiled_dataset",
    output_dir="tiled_dataset",
    slice_height=5000,  # Adjust based on your target object size
    slice_width=1654,
    overlap_height_ratio=0.4,  # Some overlap helps with continuity
    overlap_width_ratio=0
)


import os
from PIL import Image

# Paths
sliced_images_dir = "tiled_dataset"  # Update to your output directory

# Convert all .png images to .jpg
for filename in os.listdir(sliced_images_dir):
    if filename.endswith(".png"):
        img_path = os.path.join(sliced_images_dir, filename)
        img = Image.open(img_path).convert("RGB")  # Convert to RGB (JPEG format)

        # Save as .jpg
        jpg_path = os.path.splitext(img_path)[0] + ".jpg"
        img.save(jpg_path, "JPEG", quality=95)  # Save with high quality

        # Optional: Delete the original PNG file
        os.remove(img_path)
        print(f"Converted: {filename} → {os.path.basename(jpg_path)}")

print("✅ All PNG files converted to JPG.")