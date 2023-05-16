import logging
import os
import io
import torch
import clip
from torchvision import transforms as transforms
from matplotlib import pyplot as plt, colors as matplot_colors
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
from storage import temp_file, upload_file
from google.cloud import vision

log = logging.getLogger("app.sub")
# Load the model globally to increase performance
model_path = "./component.pt"
model = YOLO(model_path)
vision_client = vision.ImageAnnotatorClient()



def transform_image(image_bytes):
    im = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = im.size
    scaled_down = im.resize((round(width/4), round(height/4)))
    log.debug(im)
    im2arr = np.array(scaled_down)  # im2arr.shape: height x width x channel

    return im2arr


def get_defects(image_bytes, filename):
    image_array = transform_image(image_bytes)
    results = model(image_array, stream=False, conf=0.4)
    res_plotted = results[0].plot()
    image = Image.fromarray(res_plotted)
    new_filename = temp_file(filename, image)
    uploaded_filepath = upload_file(new_filename)
    os.remove(new_filename)

    return uploaded_filepath


def get_materials(image_bytes):
    image_array = transform_image(image_bytes)
    material_list = ["Wood", "Metal", "Fabric", "Plastic"]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    image = preprocess(Image.fromarray(image_array)).unsqueeze(0).to(device)
    text = clip.tokenize(material_list).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
    log.debug("Label probs:", probs)

    maximum = np.max(probs[0])
    index = (np.where(probs[0] == maximum))[0][0]
    material_prediction = material_list[index]
    return material_prediction


def get_dimensions(image_bytes, filename):
    # Convert image bytes to numpy array
    image_array = transform_image(image_bytes)

    # Get the pixel size
    height, width_px, _ = image_array.shape

    # The actual with of the screen
    width_cm = 70

    ratio = width_cm/width_px

    # Load image, grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find minimum area rectangle
    rect = cv2.minAreaRect(largest_contour)

    # Calculate box vertices
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    # Calculate angle of rotation
    angle = rect[2]

    # Find real size
    predicted_width = round(rect[1][0]*ratio, 0)
    predicted_height = round(rect[1][1]*ratio, 0)

    # Draw rotated bounding box
    cv2.drawContours(image_array, [box], 0, (36, 255, 12), 2)
    text = f'w={predicted_width} cm, h={predicted_height} cm, angle={round(angle, 2)} deg'
    cv2.putText(image_array, text, tuple(box[1]), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (36, 255, 12), 2)

    # Convert image array back to PIL image and return
    image_result = Image.fromarray(
        cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    )
    # image_result.save("res.png")
    image_path = temp_file(filename, image_result)
    uploaded = upload_file(image_path)
    response = {
        "predicted_height": predicted_height,
        "predicted_width": predicted_width,
        **uploaded
    }
    os.remove(image_path)
    return response


def get_colors(image_bytes):
    # image_array = transform_image(image_bytes)
    predicted_image = vision.Image(content=image_bytes)

    response = vision_client.image_properties(image=predicted_image)
    props = response.image_properties_annotation
    colors = props.dominant_colors.colors
    hex_colors = []
    for color in colors[:2]:
        dec_red = color.color.red / 255
        dec_green = color.color.green / 255
        dec_blue = color.color.blue/ 255
        hex_color = matplot_colors.to_hex([dec_red, dec_green, dec_blue])
        hex_colors.append(hex_color)

    print(colors)
    return hex_colors






if __name__ == "__main__":
    data = open("./test.png", "rb")
    image_bytes = data.read()
    result = get_dimensions(image_bytes)
    log.debug(result)

