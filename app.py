import json
import time
import logging
from pathlib import Path

import gradio as gr
from PIL import Image
import requests
import numpy as np
import settings

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def send_image(workflow):
    p = {'prompt': workflow}
    data = json.dumps(p).encode('utf-8')
    r = requests.post(settings.URL, data=data)


def get_latest_image(folder):
    folder_path = Path(folder)
    images = [f for f in folder_path.glob("*.png")]
    latest_image = str(max(images, key=lambda x: x.stat().st_ctime))
    return latest_image


def save_sketch_image(img):
    composite = img["composite"]
    if np.sum(composite) == 0:
        raise Exception
    
    pillow_image = Image.fromarray(composite)
    if pillow_image.mode == 'RGBA':
        background = Image.new('RGB', pillow_image.size, (255, 255, 255))
        background.paste(pillow_image, mask=pillow_image.split()[3])
        pillow_image = background

    sketch_input = Path(settings.INPUT_PATH) / 'sketch_input.png'
    pillow_image.save(str(sketch_input))


def fn(sketch_image, seed_number, positive_prompt):
    try:
        save_sketch_image(sketch_image)
    except Exception:
        return str(Path(settings.MISSING_SKETCH))

    with open(settings.WORKFLOW_FILE, 'r', encoding='utf-8') as file_handle:
        data = json.load(file_handle)
        data["3"]["inputs"]["seed"] = seed_number
        logging.info(f"Received seed_number: {seed_number}")
        
        data["6"]["inputs"]["text"] = f"{positive_prompt}" + ", high quality, masterpiece, detailed"
        logging.info(f'Received positive_prompt input: {data["6"]["inputs"]["text"]}')

        data["28"]["inputs"]["image"] = 'sketch_input.png'

    previous_image = get_latest_image(settings.OUTPUT_PATH)

    send_image(data)

    while True:
        new_image = get_latest_image(settings.OUTPUT_PATH)
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


