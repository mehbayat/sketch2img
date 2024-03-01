import json
import time
import logging
from pathlib import Path

import gradio as gr
from PIL import Image
import requests
import numpy as np
import settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def send_image(workflow):
    """
    Send image to the specified workflow.

    Parameters:
        workflow (str): The workflow to which the image is sent.
    """
    p = {"prompt": workflow}
    data = json.dumps(p).encode("utf-8")
    r = requests.post(settings.URL, data=data)


def get_latest_image(folder):
    """
    Get the path of the latest image in the specified folder.

    Parameters:
        folder (str): The output folder containing images.

    Returns:
        str: The path of the latest image.
    """
    folder_path = Path(folder)
    images = [f for f in folder_path.glob("*.png")]
    latest_image = str(max(images, key=lambda x: x.stat().st_ctime))
    return latest_image


def save_sketch_image(img):
    """
    Save the sketch image to the specified path.

    Parameters:
        img (dict): Dictionary containing the composite image.

    Raises:
        Exception: If the sum of the composite image is zero.
    """
    composite = img["composite"]
    if np.sum(composite) == 0:
        raise Exception

    pillow_image = Image.fromarray(composite)
    pillow_image.save(Path(settings.INPUT_PATH) / "color.png")

    if pillow_image.mode == "RGBA":
        background = Image.new("RGB", pillow_image.size, (255, 255, 255))
        background.paste(pillow_image, mask=pillow_image.split()[3])
        pillow_image = background

    sketch_input = Path(settings.INPUT_PATH) / "sketch_input.png"
    pillow_image.save(str(sketch_input))


def fn(sketch_image, positive_prompt, color_blend):
    """
    Process the sketch image and generate a new image.

    Parameters:
        sketch_image (dict): Dictionary containing the sketch image.
        positive_prompt (str): Positive prompt for the image generation.
        color_blend (float): Blend factor for color.

    Returns:
        str: The path of the generated image.
    """

    try:
        save_sketch_image(sketch_image)
    except Exception:
        gr.Warning("Sketch is empty")
        return str(Path(settings.MISSING_SKETCH))

    with open(settings.WORKFLOW_FILE, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)
        data["3"]["inputs"]["seed"] = random.randint(1, 999999999)
        data["51"]["inputs"]["seed"] = random.randint(1, 999999999)
        logging.info(f"Received seed_number: {seed_number}")

        data["6"]["inputs"]["text"] = (
            f"{positive_prompt}" + ", high quality, masterpiece, detailed"
        )
        logging.info(f'Received positive_prompt input: {data["6"]["inputs"]["text"]}')

        data["28"]["inputs"]["image"] = "sketch_input.png"
        data["56"]["inputs"]["blend_factor"] = color_blend

    previous_image = get_latest_image(settings.OUTPUT_PATH)

    send_image(data)

    while True:
        new_image = get_latest_image(settings.OUTPUT_PATH)
        if previous_image != new_image:
            return new_image
        time.sleep(1)


demo = gr.Interface(
    fn=fn,
    inputs=[
        gr.Paint(),
        gr.Textbox(value="Enter a prompt", label="Prompt"),
        gr.Slider(minimum=0.0, maximum=1.0, value=0.25, step=0.05, label="Color Blend"),
    ],
    outputs=["image"],
).queue()

demo.launch()
