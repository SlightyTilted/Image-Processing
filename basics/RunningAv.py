# Author: Kyle
#
# Script that takes in video and applies basic frame differencing to frames.

import sys
import numpy as np
import cv2 as cv

def main(filename):

	# Open video capture
	vidcap = cv.VideoCapture(0)
	threshold = 20
	lr=0.05

	# capture frame at T(i-1)
	success, prevBack = vidcap.read()
	size = np.shape(prevBack)
	sclsize = [int(round(size[0]/2)),int(round(size[1]/2))]

	prevBack = cv.cvtColor(prevBack,cv.COLOR_BGR2GRAY)
	prevBack=cv.resize(prevBack,(sclsize[1],sclsize[0]),cv.INTER_AREA)


	while (True):
		#capture frame at T(i)
		success,pCur = vidcap.read()
		pCur = cv.cvtColor(pCur,cv.COLOR_BGR2GRAY)
		pCur=cv.resize(pCur,(sclsize[1],sclsize[0]),cv.INTER_AREA)

		if success:
			out = prevBack

			# calculate B(t)=alpha*F(t) + (1-alpha)*B(t-1)
			prevBack=lr*pCur+(1-lr)*prevBack

			for i in range(sclsize[0]):
				for j in range(sclsize[1]):
					condition=abs(int(pCur[i][j])-int(prevBack[i][j]))
					if condition > threshold:
						out[i][j]=255
					else:
						out[i][j]=0

			out = cv.resize(out,(size[1],size[0]),cv.INTER_LINEAR)
			cv.imshow('Running Average',out)
			cv.imshow('background',prevBack)
			# Save video frames
			if cv.waitKey(2) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv.destroyAllWindows()

main(sys.argv[0])
