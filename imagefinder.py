import numpy as np

import pytesseract
#OPENCV
import cv2

from PIL import ImageGrab

#generate data encryption to message
from crypto import random
from crypto.cipher import AES

from Crypto.Protocol.KDF import PBKDF2

def readInfo():
    #pathway to execute tesseract
    pytesseract.pytesseract.tesseract_cmd = '**Path to tesseract executable**'
    while(True):
        #capture the image in a loop 
        capture = ImageGrab.grab(bbox= (1000, 1000, 1000, 1000))

        text = pytesseract.image_string(cv2.cvtColor(np.array(capture), cv2.COLOR_BGR2GRAY), lang="eng")
        print(text, "quit the program by pressing 'q' ")
        #option to quit the program
        if( cv2.waitKey(25) & 0xFF == ord('q') ):
            break

readInfo()

#encryption of data
sample_key = random(16)
print(sample_key)

# salt = b'\xd3\x990\xe4\x89\x81t\xcfckl\xe2\xe3\xb9/\xe8'
password = "password123"

key = PBKDF2(password, sample_key, dkLen = 16)

message = b"Hello User!"

#create a key that will cipher the message with AES as our block being padded
cipher = AES.new(key, AES.MODE_CBC)
cipher_data = cipher.encrypt(pad(message, AES.block_size))

#write a ciphere with data afterwards. binary file that cant be read
with open('encryptrd.bih', 'wb') as f:
    f.write(cipher.iv)
    f.write(cipher_data)
#read the data in the file and decrypt it
with open('encryptrd.bih', 'wb') as f:
    iv = f.read(8)
    decrypt_data = f.read()

cipher = AES.new(key, AES.MODE_CBC, iv = iv)
reveal = unpad(cipher.decrypt(decrypt_data), AES.block_size)
print(reveal)

# Convert encoding data into 8-bit binary using ASCII
def genData(data):
 
        # list of binary codes
        # of given data
        newdata = []
 
        for i in data:
            newdata.append(format(ord(i), '08b'))
        return newdata
 
# pixelels are modified to the 8-bit binary data and returned
def modpixel(pixel, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pixel)
 
    for i in range(lendata):
 
        # Extracting 3 pixelels at a time
        pixel = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pixel[j]% 2 != 0):
                pixel[j] -= 1
 
            elif (datalist[i][j] == '1' and pixel[j] % 2 == 0):
                if(pixel[j] != 0):
                    pixel[j] -= 1
                else:
                    pixel[j] += 1
                # pixel[j] -= 1
 
        # Eighth pixelel of every set tells whether to stop
        # 0 means keep reading; 1 means the message is over
        if (i == lendata - 1):
            if (pixel[-1] % 2 == 0):
                if(pixel[-1] != 0):
                    pixel[-1] -= 1
                else:
                    pixel[-1] += 1
 
        else:
            if (pixel[-1] % 2 != 0):
                pixel[-1] -= 1
 
        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixelel in modpixel(newimg.getdata(), data):
 
        # Putting modified pixelels in the new image
        newimg.putpixelel((x, y), pixelel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Encode data into image
def encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')
 
    newimg = image.copy()
    encode_enc(newimg, data)
 
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
 
# Decode the data in the image
def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixelels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixelels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixelels[-1] % 2 != 0):
            return data
 
# Main Function
def main():
    a = int(input(":: Welcome to my project ::\n"
                        "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()
 
    elif (a == 2):
        print("Decoded Word :  " + decode())
    else:
        raise Exception("Enter correct input")
 
# Driver Code
if __name__ == '__main__' :
 
    # Calling main function
    main()