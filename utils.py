import io
import logging
from storage import temp_file, upload_file
from pathlib import Path
from rembg import remove, new_session
from PIL import Image

model_name = "isnet-general-use"
session = new_session(model_name=model_name)

def remove_background(image_bytes, filename):
    input = Image.open(io.BytesIO(image_bytes))
    output = remove(input)

    temp_path = temp_file(filename, output, file_ext=".png")

    uploaded = upload_file(temp_path, file_ext=".png")

    return uploaded
