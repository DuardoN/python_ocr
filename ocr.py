import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from io import StringIO

from io import BytesIO

def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    return pytesseract.image_to_string(image)


def _get_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))
