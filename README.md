# Sketch2Img

This app is a Python application that uses Stable Diffusion to create a simple user interface (Gradio) for generating images based on sketches using ComfyUI as the backend. 

## Examples

<img src="media/Screenshot (117) (1).png" alt="Example1">

<img src="media/Screenshot (118).png" alt="Example2">


## Prerequisites
Before running the application, make sure you have the following installed:

- Python 3.11 or more
- Gradio (pip install gradio)
- Pillow (pip install Pillow)
- Requests (pip install requests)

## Usage
1. Clone the repository
'''bash
git clone https://github.com/mehbayat/sketch2img.git
cd sketch2img
'''
2. 
```bash
python comfyui.py
```

This will launch the Gradio interface, allowing you to interact with the image generation process.

## Configuration

You can configure the application by modifying the constants in the `comfyui.py` file:

- `OUTPUT_PATH`: The path where generated images will be saved.
- `INPUT_PATH`: The path where input images are stored.
- `URL`: The URL of the backend server for communication.

## Dependencies

- Gradio
- Pillow
- Requests

Install the dependencies using:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Gradio](https://github.com/gradio-app/gradio)

Feel free to contribute to the project or report issues. Happy coding!
