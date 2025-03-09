from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
# from qwen_vl_utils import process_vision_info
from PIL import Image
import requests
import torch

device = torch.device("mps" if torch.backends.mps.is_built() else "cpu")

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct", torch_dtype='auto', device_map="auto"
)

min_pixels = 256 * 28 * 28 
max_pixels = 640 * 28 * 28

processor = AutoProcessor.from_pretrained( "Qwen/Qwen2.5-VL-7B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels)

image_path = "sample.jpg"
image = Image.open(image_path)

# Messages format for text-to-image generation
messages = messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": image,
            },
            {
                "type": "text",
                "text": "Use tables for data presentation and image to represent diagams in the picture. label tables with (1), (2), (3) and (4) as class = 'options' . Please create an HTML page based on the provided text and diagram. "
            },
            {
                "type": "text",
                "text": "Here is an example of a good output: <html><body><p>...</p>  <img src = 'image1.jpg alt = 'image1'>  <p>...</p>  <table>...</table>  <p>...</p>   <table>...</table> </body></html>"
            }
        ],
    }
]

# Preparation for inference
text = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

inputs = processor(
    text=[text],
    images=[image],  # Directly pass the PIL image here
    padding=True,
    return_tensors="pt",
)

inputs = inputs.to(device)

# Perform inference: Generate the output
generated_ids = model.generate(**inputs, max_new_tokens=2048)


# Trim the output to exclude input tokens
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]

# Decode and print the result
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
output_text = output_text[0]
occurrences = output_text.count('<div class="image"><img/></div>')
for i in range(1, occurrences + 1):
    output_text = output_text.replace(f'<div class="image"><img/></div>', f'<img src="image{i}.jpg" alt="image{i}"/>', 1)
output_text = output_text.replace('\n', '').strip()
print(output_text)