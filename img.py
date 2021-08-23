from abc import abstractclassmethod
from PIL import Image
import os

"""
Open an image with name image_name.
The image should be put under the folder "OriginalPhotos/".

@param image_name: the name of the image under "OriginalPhotos/".
"""
def OpenImage(image_name):
    path = os.path.join("OriginalPhotos/", image_name)
    img = Image.open(path)
    return img


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


if __name__== "__main__":
    img = OpenImage("42.png")
    img_resized = ResizePercentage(img, 0.6)
    img_resized = ResizePercentage(img, 0.5)
    img_resized.show()
    print(img.size)
    print(img_resized.size)
    print(type(img_resized))
