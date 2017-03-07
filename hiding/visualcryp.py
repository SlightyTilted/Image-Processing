# Written by Kyle
#
# A simple program that implements a variation of visual cryptography

import numpy as np
import cv2 as cv
import random



def main():
    global height, width, tempol, tempor, output
    img = cv.imread("Dory.ppm", 0)
    ret, img = cv.threshold(img, 127,255,cv.THRESH_BINARY)
    width, height = img.shape
    #Create 2 blank templates that are 4 times the size of original image
    tempol = np.zeros((width*2, height*2), np.uint8)
    tempor = np.zeros((width*2, height*2), np.uint8)
    output = np.zeros((width*2, height*2), np.uint8)

    tempol.fill(255)
    tempor.fill(255)

    cv.imshow("threshold", img)
    cv.waitKey(0)

    splitimga(img)
    splitimgb(img)

    smalll = cv.resize(tempol, (0,0), fx=0.3, fy =0.3)
    cv.imshow("left", smalll)
    cv.imwrite("leftimg.ppm",smalll)
    cv.waitKey(0)

    smallr = cv.resize(tempol, (0,0), fx=0.3, fy =0.3)
    cv.imshow("right", smallr)
    cv.imwrite("rightimg.ppm",smallr)
    cv.waitKey(0)

    combine()

    smallc = cv.resize(output, (0,0), fx=0.3, fy =0.3)
    cv.imshow("combined", smallc)
    cv.waitKey(0)
def splitimga(image):
    for i in range(0, height):
        for j in range(0, width):
            coin = random.randrange(0,2)
            pix = image[i][j]
            if pix == 0: #Black pixels
                if coin ==1:
                    #left image
                    tempol[2*i][2*j] =0
                    tempol[2*i+1][2*j]= 255
                    tempol[2*i][2*j+1] = 255
                    tempol[2*i+1][2*j+1] =0

                    #right image
                    tempor[2*i][2*j] =255
                    tempor[2*i+1][2*j]= 0
                    tempor[2*i][2*j+1] = 0
                    tempor[2*i+1][2*j+1] = 255
                if coin !=1:
                    #left image
                    tempol[2*i][2*j] =255
                    tempol[2*i+1][2*j]= 0
                    tempol[2*i][2*j+1] = 0
                    tempol[2*i+1][2*j+1] =255

                    #rightimage
                    tempor[2*i][2*j] =0
                    tempor[2*i+1][2*j]= 255
                    tempor[2*i][2*j+1] = 255
                    tempor[2*i+1][2*j+1] =0

def splitimgb(image):
    for i in range(0, height):
        for j in range(0, width):
            coin = random.randrange(0,2)
            pix = image[i][j]
            if pix == 255: #white pixels
                if coin ==1:
                    #left image
                    tempol[2*i][2*j] =255
                    tempol[2*i+1][2*j]= 0
                    tempol[2*i][2*j+1] = 0
                    tempol[2*i+1][2*j+1] =255

                    #right image
                    tempor[2*i][2*j] =255
                    tempor[2*i+1][2*j]= 0
                    tempor[2*i][2*j+1] = 0
                    tempor[2*i+1][2*j+1] = 255
                if coin !=1:
                    #left image
                    tempol[2*i][2*j] =0
                    tempol[2*i+1][2*j]= 255
                    tempol[2*i][2*j+1] = 255
                    tempol[2*i+1][2*j+1] =0

                    #rightimage
                    tempor[2*i][2*j] =0
                    tempor[2*i+1][2*j]= 255
                    tempor[2*i][2*j+1] = 255
                    tempor[2*i+1][2*j+1] =0

def combine():
    nwidth, nheight = output.shape
    for i in range(0,nheight):
        for j in range(0, nwidth):
            if (tempol[i][j] == 255) and (tempor[i][j] ==255):
                output[i][j]= 0
            elif (tempol[i][j] == 0) and (tempor[i][j] == 0):
                output[i][j]= 255
            elif(tempol[i][j] == 255) and (tempor[i][j] ==0):
                output[i][j]= 0
            elif(tempol[i][j] == 0) and (tempor[i][j] == 255):
                output[i][j]=0

main()
