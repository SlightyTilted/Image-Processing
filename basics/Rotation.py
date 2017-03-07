
#simple algorithm that takes in an image and a angle of rotation and saves the rotated image for viewing
#
#Author: Kyle Marais
#
#Help provided by Sean Devenport
#

import numpy as np
import sys
import ppmreader as reader
import math

def rotate(filename,angle):
	# open file for use
	[size,img_mxclr,img_in] = reader.ppmreader(filename)
	# get cos and sin of angle
	rad = math.radians(float(angle))
	cosine =  math.cos(rad)
	sine = math.sin(rad)

	cen = [int(size[0]/2),int(size[1]/2)]

	# calculate new bounding rectangle
	nsize = [int(math.ceil(abs(size[0]*cosine)+abs(size[1]*sine))),int(math.ceil(abs(size[1]*cosine)+abs(size[0]*sine)))]
	ncen = [int(nsize[0]/2),int(nsize[1]/2)]
	offset = [int(math.ceil((size[0]-nsize[0])/2)),int(math.ceil((size[1]-nsize[1])/2))]
	cdif = [ncen[0]-cen[0],ncen[1]-cen[1]]

	out = [[0,0,0]]*nsize[0]*nsize[1]

	for i in range(nsize[1]):
		for j in range(nsize[0]):
			# calculate new pixel x,y index
			xn = int(math.cos(rad)*(j-ncen[0]) - math.sin(rad)*(i-ncen[1])) + ncen[0]-1
			yn = int(math.sin(rad)*(j-ncen[0]) + math.cos(rad)*(i-ncen[1])) + ncen[1]-1

			# only move pixels that are within the limits of the image.
			xdif = xn-cdif[0]
			ydif = yn-cdif[1]
			if (xdif<size[0]) and (xdif>=0) and (ydif<size[1]) and (ydif>=0):
				out[i*nsize[0]+j] = img_in[ydif*size[0]+xdif]

	rot = open('RotatedDory.ppm','w')

	header = "P3\n# This is image has been rotated by Kyle Marais\n{0} {1}\n{2}\n".format(nsize[0],nsize[1],img_mxclr)

	rot.write(header)

	for pixel in out:
		rot.write("{0} {1} {2}\n".format(pixel[0],pixel[1],pixel[2]))

	rot.close

rotate('Dory.ppm',sys.argv[1])
