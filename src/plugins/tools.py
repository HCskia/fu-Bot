import base64
import json
import os
import random
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

music_data = "https://www.diving-fish.com/api/maimaidxprober/music_data"

def image_to_base64(img, format='PNG'):
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def image_to_base64_gif(imgPath):
    with open(imgPath, "rb") as f:
        base64_data = base64.b64encode(f.read())
        f.close()
    return base64_data

def hash(qq: int):
    days = int(time.strftime("%y", time.localtime(time.time()))) + 9 * int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
        time.strftime("%m", time.localtime(time.time())))
    return (days * qq) >> 8

def TextToImg(text):
    bgImg = Image.new("RGB", (1920, 1080), (255, 255, 255))
    bgImgDr = ImageDraw.Draw(bgImg)
    font = ImageFont.truetype(os.path.join("fonts", "simhei.ttf"), 15)
    imgSize = bgImgDr.multiline_textsize(text, font=font)
    newImg = bgImg.resize((imgSize[0] + 10, imgSize[1] + 10))
    newImgDr = ImageDraw.Draw(newImg)
    newImgDr.text((1, 1), text, font=font, fill="#000000")
    return newImg

def readJson(path):
    with open(path, 'r',encoding='utf-8') as f:
        tempData = json.load(f)
        f.close()
    return tempData

def writeJson(path,data):
    with open(path, 'w+', encoding="utf-8")as f:
        json.dump(data, f,ensure_ascii=False)
        f.close()
    return 0

def getRandomFile(path):
    FileList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            FileList.append(os.path.join(root, file))
    return FileList[random.randint(0, len(FileList)-1)]