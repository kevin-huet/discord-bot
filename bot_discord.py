import discord
import random
import requests
import shutil
import PIL
import yaml
import imgur
import io
import aiohttp
import random
from ascii_converter import img_resize, grayscale, pixels_to_ascii, create_image_from_ascii

TOKEN = ''

client = discord.Client()


def init():
    global TOKEN
    a_yaml_file = open("config.yaml")
    parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    TOKEN = parsed_yaml_file['token']


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


@client.event
async def on_message(message):
    channel = message.channel
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!lastascii'):
        await channel.send(file=discord.File('test.png'))

    if message.content.startswith('!ascii'):
        image_url = message.attachments[0].url
        emoji = '\N{THUMBS UP SIGN}'
        save_image(image_url)
        ascii_image_conversion()
        await message.add_reaction(emoji)
        await channel.send('{0.author.mention}'.format(message), file=discord.File('test.png'))

    if message.content.startswith('!help'):
        await message.author.send('Usage:\n!ascii + image')

    if message.content.startswith('!stonks'):
        await channel.send('{0.author.mention}'.format(message), file=discord.File('stonk.jpg'))

    if message.content.startswith('!notstonks'):
        await channel.send('{0.author.mention}'.format(message), file=discord.File('notstonks.png'))

    if message.content.startswith('?search'):
        array = message.content
        array = array.split(' ')
        if len(array) > 1:
            array[0] = ""
            value = " ".join(array)
            print(value)
            image = imgur.search_image(value)
            if isinstance(image, str):
                await channel.send('no result found')
            else:
                await channel.send(image['results'][0]['url'])


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


init()
imgur.init()
client.run(TOKEN)
