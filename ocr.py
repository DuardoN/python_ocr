import requests
import os

def process_image(url, name_image):
    # Download image to open and remove errors
    new_name = 'image-' + name_image + '.jpg'
    f = open('images/'+new_name,'wb')
    f.write(requests.get(url).content)
    f.close()

    # Open image and proccess
    command = "python3 ocr_tests.py --image images/" + new_name
    data = os.popen(command).read()

    return data