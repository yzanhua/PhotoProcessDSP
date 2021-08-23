from abc import abstractclassmethod
from PIL import Image
import os
from math import sqrt
from config import colormap, all_colors
import numpy as np


"""
Open an image with name image_name.
The image should be put under the folder "OriginalPhotos/".

@param image_name: the name of the image under "OriginalPhotos/".
"""
def OpenImage(image_name):
    path = os.path.join("OriginalPhotos/", image_name)
    img = Image.open(path)
    img.load()
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
    return background


"""
@param img: PIL.Image.Image object, the image you would like to resize.
@param t_width: target width in pixel.
@param t_height: target height in pixel.
@output, PIL.Image.Image object, with target width and height.
"""
def Resize(img, t_width=300, t_height=300):
    img_resized = img.resize((t_width, t_height))
    return img_resized

"""
@param img: PIL.Image.Image object, the image you would like to resize.
@param percent: float in [0, 1].
@output, PIL.Image.Image object, with (new_width, new_height) = (org_width, org_height) * percent.
"""
def ResizePercentage(img, percent):
    t_width = int(img.width * percent)
    t_height = int(img.height * percent)
    return Resize(img, t_width, t_height)


def FindNearestColor(rgb):
    closest_color = min(all_colors, key=lambda c_name: np.linalg.norm(rgb - colormap[c_name]))
    return np.copy(colormap[closest_color]), closest_color 


def CheckInbound(x, y, img):
    if x < 0 or x >= img.width:
        return False
    if y < 0 or y >= img.height:
        return False  
    return True  


def GetNumpyFromImg(img):
    array = np.zeros((img.width, img.height, 3))
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            array[x, y] = np.array(pixels[x, y])
    return array


def Dithering(img):
    pixels = GetNumpyFromImg(img)
    record = [[None for _ in range(img.height)] for _ in range(img.width)]
    for y in range(img.height):
        for x in range(img.width):
            old_p = pixels[x, y]
            new_p, new_c = FindNearestColor(old_p)
            pixels[x,y] = new_p
            record[x][y] = new_c
            error = old_p - new_p
            if CheckInbound(x+1, y, img):
                pixels[x+1, y] += error * (7.0/16.0)
            if CheckInbound(x-1, y+1, img):
                pixels[x-1, y+1] += error * (3.0/16.0)
            if CheckInbound(x, y+1, img):
                pixels[x, y+1] += error * (5.0/16.0)
            if CheckInbound(x+1, y+1, img):
                pixels[x+1, y+1] += error * (1.0/16.0)
    
    return record
    

def DisplayRecord(record):
    width, height = len(record), len(record[0])
    data = np.zeros((height, width, 3),dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            data[y, x] = colormap[record[x][y]]
    img = Image.fromarray(data, 'RGB')
    img.show()


def SaveRecord(record, name):
    path = os.path.join("save/", name)
    with open(path, "w") as file:
        for x in range(len(record)):
            for y in range(len(record[0])):
                file.write(str(record[x][y]))
                file.write(" ")
            file.write("\n")


def ProcessImg(name, percent):
    img_name = name + ".png"
    save_name = name+".txt"
    img = OpenImage(img_name)
    img = ResizePercentage(img, percent)

    print(img_name, img.size)

    record = Dithering(img)
    SaveRecord(record, save_name)
    DisplayRecord(record)


if __name__== "__main__":
    name = "sikadi"
    ProcessImg("sikadi", 0.5)
    ProcessImg("42", 0.5)


