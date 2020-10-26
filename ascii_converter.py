import PIL.Image
from PIL import ImageFont, ImageDraw, Image
import sys
from bot import tweet_image, get_tweet_mention

chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
MAX_WIDTH = 1920
MAX_HEIGHT = 1920


def resize_img():
    i = 0
    img = Image.open('test.png')
    width = img.size[0]
    height = img.size[1]
    while i != 2:
        if height > MAX_HEIGHT:
            new_height = MAX_HEIGHT
            new_width = new_height * width / height
            img = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        if width > MAX_WIDTH:
            new_height = MAX_WIDTH
            new_width = new_height * width / height
            img = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        i += 1
    img.save('test.png')


def create_image_from_ascii(txt, _color):
    # get the size of the text
    nb_line = txt.count('\n')
    nb_char = 0
    while txt[nb_char]:
        if txt[nb_char] == '\n':
            break
        nb_char += 1
    if _color == "white":
        image = Image.new('RGB', (6 * nb_char, int((15 * nb_line))), color="white")
    else:
        image = Image.new('RGB', (6 * nb_char, int((15 * nb_line))), color="black")
    draw = ImageDraw.Draw(image)
    print((15 * nb_line) * (6 * nb_char))
    if _color == "white":
        draw.text((0, 0), txt, _BLACK)
    else:
        draw.text((0, 0), txt, _WHITE)
    image.save('test.png')
    resize_img()
    return draw


def img_resize(img):
    width, height = img.size
    aspect_ratio = height / width
    new_width = 300
    new_height = aspect_ratio * new_width * 0.42
    img = img.resize((new_width, int(new_height)))
    return img


def pixels_to_ascii(img):
    new_width, new_height = img.size
    pixels = img.getdata()
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image


def grayscale(img):
    return img.convert("L")


def main(argv):
    if len(argv) < 1:
        return
    tweet_id, color = get_tweet_mention()
    img = PIL.Image.open('img.jpeg')
    img = img_resize(img)
    img = grayscale(img)
    ascii_image = pixels_to_ascii(img)
    create_image_from_ascii(ascii_image, color)
    if len(argv) > 1 and len(argv[1]) > 0:
        with open(argv[1], "w") as f:
            f.write(ascii_image)
    #tweet_image(tweet_id)


main(sys.argv[1:])
