import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from io import StringIO

from io import BytesIO

from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def process_image(url, name_image):
    # Download image to open and remove errors
    new_name = 'image-' + name_image
    f = open('images/'+new_name+'.jpg','wb')
    f.write(requests.get(url).content)
    f.close()

    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'

    return pytesseract.image_to_string(image)

def _get_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# perform a image cleaning to enhance constrast and borders
def cleanImage(image, stage = 0):
    V = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # applying topHat/blackHat operations
    topHat = cv2.morphologyEx(V, cv2.MORPH_TOPHAT, kernel)
    blackHat = cv2.morphologyEx(V, cv2.MORPH_BLACKHAT, kernel)
    # add and subtract between morphological operations
    add = cv2.add(V, topHat)
    subtract = cv2.subtract(add, blackHat)
    if (stage == 1):
        return subtract
    T = threshold_local(subtract, 29, offset=35, method="gaussian", mode="mirror")
    thresh = (subtract > T).astype("uint8") * 255
    if (stage == 2):
        return thresh
    # invert image 
    thresh = cv2.bitwise_not(thresh)
    return thresh