import io

from torchvision import transforms as transforms
from matplotlib import pyplot as plt
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

# Load the model globally to increase performance
model_path = "./best.pt"
model = YOLO(model_path)


def transform_image(image_bytes):
    im = Image.open(io.BytesIO(image_bytes))
    width, height = im.size
    scaled_down = im.resize((int(width/4), int(height/4)))
    im2arr = np.array(scaled_down)  # im2arr.shape: height x width x channel
    # print("im2arr: ", im2arr, "\n")
    # print("im2arr shape: ", im2arr.shape, "\n")

    return im2arr


def get_prediction(image_bytes):
    image_array = transform_image(image_bytes)
    results = model(image_array, stream=False)
    res_plotted = results[0].plot()
    image = Image.fromarray(res_plotted)
    return image
