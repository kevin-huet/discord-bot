from ascii_converter import *
import requests
import shutil

def save_image(url):
    response = requests.get(url, stream=True)
    with open('image.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def ascii_image_conversion():
    img = PIL.Image.open('image.png')
    img = img_resize(img)
    img = grayscale(img)
    ascii_image = pixels_to_ascii(img)
    create_image_from_ascii(ascii_image, "white")


def run(message):
    image_url = message.attachments[0].url
    emoji = '\N{THUMBS UP SIGN}'
    save_image(image_url)
    ascii_image_conversion()