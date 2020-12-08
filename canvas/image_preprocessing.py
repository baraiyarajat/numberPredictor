import cv2
import numpy as np
from base64 import b64decode
from PIL import Image, ImageFilter


#Converts dataURI string to a pixel array
def convert_image_to_byte(imagestr):


    image_b64 = imagestr
    binary = b64decode(image_b64)
    image = np.asarray(bytearray(binary), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

#Takes only the occupied area of the image and removes extra space
def remove_noise(byte_array):


    img = byte_array

    #Convert to gray, and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    #Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
    cnts = []

    #Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if cnts != []:
        cnt = sorted(cnts, key=cv2.contourArea)[-1]
    else:
        return None

    #Crop and save it
    x,y,w,h = cv2.boundingRect(cnt)
    dst = img[y:y+h, x:x+w]
    return dst

#Converts the image array into 28X28 pixel array || Resizing the image and Enhancing the pixels
def convert_into_required_size(pixel_array):


    im = Image.fromarray(pixel_array).convert('L')

    width = float(im.size[0])
    height = float(im.size[1])

    #creating white canvas of 28x28 pixels
    newImage = Image.new('L', (28, 28), (255))

    # checking which dimension is bigger
    if width > height:
        # Width is bigger. Width becomes 20 pixels.

        # resize height according to ratio width
        nheight = int(round((20.0 / width * height), 0))

        # rare case but minimum is 1 pixel
        if (nheight == 0):
            nheight = 1

        # resizing and sharpening
        img = im.resize((27, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        # calculate horizontal position
        wtop = int(round(((28 - nheight) / 2), 0))
        # paste resized image on white canvas
        newImage.paste(img, (1, wtop))
    else:
        # Height is bigger. Heigth becomes 20 pixels.

        # resize width according to ratio height
        nwidth = int(round((27.0 / height * width), 0))

        # rare case but minimum is 1 pixel
        if (nwidth == 0):
            nwidth = 1

        # resizing and sharpening
        img = im.resize((nwidth, 27), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        # caculate vertical pozition
        wleft = int(round(((28 - nwidth) / 2), 0))
        # paste resized image on white canvas
        newImage.paste(img, (wleft, 1))

    # get pixel values
    tv = list(newImage.getdata())

    # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    tva = [(255 - x) * (1) for x in tv]

    #Enhancing the pixel values
    for index in range(len(tva)):

        if tva[index] >=90:

            if tva[index]<=120:
                tva[index] *=2
            elif tva[index]<=150:
                tva[index] *=1.6
            elif tva[index] <=200:
                tva[index] *= 1.2

        else:
            tva[index] = 0

    return tva
