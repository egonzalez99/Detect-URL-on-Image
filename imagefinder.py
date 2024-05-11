import os
import cv2
import numpy as np
import pytesseract 
from PIL import ImageGrab
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from Crypto.Protocol.KDF import PBKDF2

def readInfo():
    #pathway to execute tesseract
    pytesseract.pytesseract.tesseract_cmd = 'c:\\Users\\geddi\\OneDrive\\Pictures\\Screenshots\\Screenshot-443.png'

    while(True):
        #capture the image in a loop 
        capture = ImageGrab.grab(bbox= (1000, 1000, 1000, 1000))

        text = pytesseract.image_to_string(cv2.cvtColor(np.array(capture), cv2.COLOR_BGR2GRAY), lang="eng")
        print(text, "quit the program by pressing 'q' ")
        #option to quit the program
        if( cv2.waitKey(25) & 0xFF == ord('q') ):
            break

readInfo()

# Generate a key using PBKDF2
def generate_key(password, salt):
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

# Encrypt data using AES-CBC mode
def encrypt_data(key, data):
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext

# Decrypt data using AES-CBC mode
def decrypt_data(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return unpadder.update(decrypted_data) + unpadder.finalize()

#write a ciphere with data afterwards. binary file that cant be read
password = b'password123'
salt = os.urandom(16)  # Generate a random salt
key = generate_key(password, salt)
data_to_encrypt = b"Hello User!"

iv, ciphertext = encrypt_data(key, data_to_encrypt)
print("IV:", iv)
print("Ciphertext:", ciphertext)

decrypted_data = decrypt_data(key, iv, ciphertext)
print("Decrypted Data:", decrypted_data.decode())

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
    image = ImageGrab.open(img, 'r')
 
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
    image = ImageGrab.open(img, 'r')
 
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