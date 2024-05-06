import numpy as nm

import pytesseract

import cv2

from PIL import ImageGrab

def readInfo():
    #pathway to execute tesseract
    pytesseract.pytesseract.tesseract_cmd = '**Path to tesseract executable**'
    while(True):
        #capture the image in a loop 
        capture = ImageGrab.grab(bbox= (1000, 1000, 1000, 1000))

        tesstr = pytesseract.image_string(cv2.ctColor(nm.array(capture), cv2.COLOR_BGR2GRAY), lang="eng")
        print(tesstr)

readInfo()