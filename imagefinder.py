import numpy as np

import pytesseract
#OPENCV
import cv2

from PIL import ImageGrab

def readInfo():
    #pathway to execute tesseract
    pytesseract.pytesseract.tesseract_cmd = '**Path to tesseract executable**'
    while(True):
        #capture the image in a loop 
        capture = ImageGrab.grab(bbox= (1000, 1000, 1000, 1000))

        text = pytesseract.image_string(cv2.cvtColor(np.array(capture), cv2.COLOR_BGR2GRAY), lang="eng")
        print(text, "quit the program by pressing 'q' ")
        #option to quit the program
        if( cv2.woitKey(25) & 0xFF == ord('q') ):
            break

readInfo()