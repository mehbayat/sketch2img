import json
import time
import logging
from pathlib import Path

import gradio as gr
from PIL import Image
import requests

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

OUTPUT_PATH = r"C:\Users\Mehrad Bayat\Desktop\ComfyUI_windows_portable\ComfyUI\output"
INPUT_PATH = r"C:\Users\Mehrad Bayat\Desktop\ComfyUI_windows_portable\ComfyUI\input"
URL = "http://127.0.0.1:8188/prompt"


def send_image(workflow):
    p = {'prompt': workflow}
    data = json.dumps(p).encode('utf-8')
    r = requests.post(URL, data=data)


def get_latest_image(folder):
    folder_path = Path(folder)
    images = [f for f in folder_path.glob("*.png")]
    latest_image = str(max(images, key=lambda x: x.stat().st_ctime))
    return latest_image


def fn(sketch_image, seed_number, positive_prompt):

    composite = sketch_image["composite"]
    pillow_image = Image.fromarray(composite)
    if pillow_image.mode == 'RGBA':
        background = Image.new('RGB', pillow_image.size, (255, 255, 255))
        background.paste(pillow_image, mask=pillow_image.split()[3])
        pillow_image = background

    sketch_input = Path(INPUT_PATH) / 'sketch_input.png'
    pillow_image.save(str(sketch_input))

    with (open('sketch2image_api.json', 'r', encoding='utf-8') as file_handle):
        data = json.load(file_handle)
        data["3"]["inputs"]["seed"] = seed_number
        logging.info(f"Received seed_number: {seed_number}")
        data["6"]["inputs"]["text"] = f"{positive_prompt}" + ", high quality, masterpiece, detailed"
        logging.info(f'Received positive_prompt input: {data["6"]["inputs"]["text"]}')

        try:
            data["28"]["inputs"]["image"] = 'sketch_input.png'
        except ValueError as e:
            print(e)

    previous_image = get_latest_image(OUTPUT_PATH)

    send_image(data)

    while True:
        new_image = get_latest_image(OUTPUT_PATH)
        if previous_image != new_image:
            return new_image
        time.sleep(1)


demo = gr.Interface(fn=fn, inputs=[
    gr.Paint(),
    gr.Number(value=1, label='Seed Number'),
    gr.Textbox(value='Enter a prompt', label='Prompt'),
    ],
    outputs=["image"]
)


demo.launch()


