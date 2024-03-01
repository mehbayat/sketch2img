# Sketch2Img

This app is a Python application that uses Gradio to create a simple user interface for generating images based on sketches using ComfyUI as the backend. 

## Screenshots
![ComfyUI Logo](images/comfyui_logo.png)

<img src="images/comfyui_logo.png" alt="ComfyUI Logo">


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

- ComfyUI - link
- Gradio - link

Feel free to contribute to the project or report issues. Happy coding!
