#Author: Kyle Marais
#Script that takes in video from webcam, and then applies basic background subtraction to the acquired frames
import sys
import numpy as np
import cv2 as cv
import py_compile

def main(filename):

	# Open video capture for webcam
	vidcap = cv.VideoCapture(0)
	frames = [0]*3
	prevFrame = [0]*2
	threshold = 100;

	#capture first frame (background)
	success, prevBack = vidcap.read()
	size = np.shape(prevBack)
	cv.imshow('Frame',prevBack)
	prevBack = cv.cvtColor(prevBack,cv.COLOR_BGR2GRAY)

	while (True):
		success,pCur = vidcap.read()
		pCur = cv.cvtColor(pCur,cv.COLOR_BGR2GRAY)
		if success:
			# Do processing
			# calculate foreground mask
			for i in range(size[0]):
				for j in range(size[1]):
					condition=abs(int(pCur[i][j])-int(prevBack[i][j]))
					if condition >threshold:
						pCur[i][j]=255
					else:
						pCur[i][j]=0

			cv.imshow('Background Subtraction',pCur)

			# Save video frames
			if cv.waitKey(2) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv.destroyAllWindows()

main(sys.argv[0])
