'''
Author: Kyle

simple steganographic system for ppm files. The algorithm works by reading in a gray scale image and in row 100, removing the least
significat values from the pixels in this row, and then taking the supplied message, converting it to binary, and appending these
bits one by one to the pixels in row 100.

'''
import cv2 as cv
import sys
import numpy as np
import binascii

def main():
    global height, width

    img_file = 'Dory.ppm'
    dory = cv.imread(img_file, 0);
    height, width = dory.shape[::-1]
    column = 100
    message = sys.argv[1]
    encodedIm =encode(message, dory)

    binaryMessage =decode(encodedIm)

    encodedMessage = int(binaryMessage,2)
    decodedMessage =binascii.unhexlify('%x' % encodedMessage)
    print("The message you supplied has been decoded as:")
    print(decodedMessage)
#END OF MAIN


def encode(message, image):
    global hidecolumn, length
    encImage = image.copy()
    global blue
    binary = bin(int(binascii.hexlify(message),16))
    #print(binary)
    mes_len = len(binary)
    length = mes_len
    hidecolumn = 100
    counter =0;
    for i in range(0,mes_len):
        if counter==0 or counter==1:
            counter= counter +1
            continue
        pixVal = encImage[hidecolumn][i]
        pixValbin = bin(pixVal)
        #print(pixValbin)

        pixVal = pixVal >>1
        pixValbin = bin(pixVal)
        #print(pixValbin)

        #print(binary[i])

        counter= counter +1
        temp = str(pixValbin) + binary[i]
        #pixVal = pixVal + int(binary[i])
        #print(temp)
        #print(int(temp,2))
        #print("\n")

        adder = int(temp,2)
        encImage[hidecolumn][i] = adder

    colorEnc = cv.cvtColor(encImage, cv.COLOR_GRAY2RGB)
    cv.imshow("Encoded Image",colorEnc)
    cv.waitKey(0)
    cv.imwrite("EncodedDory.png", colorEnc)
    return encImage
    #print(blue)

def decode (image):
    binaryString ="0b"
    counter =0
    for i in range(2, length):
        pixVal = image[hidecolumn][i]
        pixValbin = bin(pixVal)
        counter = counter +1
        binlen = len(pixValbin)
        binaryString = binaryString + str(pixValbin[binlen-1])
        #print(pixValbin[binlen-1])
    return binaryString
main()
