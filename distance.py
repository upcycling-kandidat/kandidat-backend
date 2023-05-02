
from predict import transform_image
import cv2 
#from google.colab.patches import cv2_imshow
from PIL import Image
import math
import numpy as np

def get_distance(image_bytes):
    # Convert image bytes to numpy array
    image_array = transform_image(image_bytes)

    # Get the pixel size
    height, width_px, _ = image_array.shape

    # The actual with of the screen
    width_cm = 68

    ratio = width_cm/width_px

    # Load image, grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    predicted_width = round(rect[1][0]*ratio,2)
    predicted_height = round(rect[1][1]*ratio,2)

    # Draw rotated bounding box
    cv2.drawContours(image_array,[box],0,(36,255,12),2)
    cv2.putText(image_array, "w={} cm, h={} cm, angle={} deg".format(predicted_width, predicted_height, round(angle,2)), tuple(box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)

    # Convert image array back to PIL image and return
    image_result = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    image_result.save("res.png")
    return image_result, predicted_width, predicted_height

if __name__ == "__main__":
    data = open("./test.png", "rb")
    image_bytes = data.read()
    result = get_distance(image_bytes)
    print(result)