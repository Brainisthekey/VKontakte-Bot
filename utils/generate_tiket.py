import json
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "data/tikets/Tiket.png"
FONT_PATH = "data/font/Roboto-Regular.ttf"
FONT_SIZE = 20
BLACK = (0, 0, 0, 255)
NAME_OFFSET = (257, 187)
EMAIL_OFFSET = (255, 218)
AVATAR_OFFSET = (472, 135)
IM_SIZE = (120,120)


def generate(name,email):

    # get an image
    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    # get a font
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # draw text, half opacity
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    # draw text, full opacity
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    response = requests.get(url='https://api.thecatapi.com/v1/images/search')
    avatar = json.loads(response.content)[0]['url']
    avatar_file_like = BytesIO(requests.get(avatar).content)
    avatar_file = Image.open(avatar_file_like)
    avatar_file.thumbnail(IM_SIZE)
    base.paste(avatar_file, AVATAR_OFFSET)
    #We need to save file for tests
    with open('data/tikets/ticket_example.png', 'wb') as file:
        base.save(file, 'png')
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)
    return temp_file
