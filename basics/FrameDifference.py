#Author: Kyle Marais
#Script that takes in video from webcam, and then applies basic frame differencing to the frames acquired from the video.
import sys
import numpy as np
import cv2 as cv

def main(filename):

	# Open webcam capture
	vidcap = cv.VideoCapture(0)
	thr = 20;

	# capture frame at T(i-1)
	success, prevBack = vidcap.read()
	size = np.shape(prevBack)
	# sclsize = [30,30]
	prevBack = cv.cvtColor(prevBack,cv.COLOR_BGR2GRAY)
	out=prevBack
	while (True):
		#capture frame at T(i)
		success,pCur = vidcap.read()
		pCur = cv.cvtColor(pCur,cv.COLOR_BGR2GRAY)
		if success:
			for i in range(size[0]):
				for j in range(size[1]):
					cond=abs(int(pCur[i][j])-int(prevBack[i][j]))
					if cond >thr:
						out[i][j]=255
					else:
						out[i][j]=0


			cv.imshow('Frame Differencing',out)
			# update background frame
			prevBack=pCur
			# Save video frames
			#cv.imwrite("stvidcap_out/frame%d.ppm" % count, img) #save frame as PPM file.
			if cv.waitKey(2) & 0xFF == 27:
				break
		else:
			break

	vidcap.release()
	cv.destroyAllWindows()

main(sys.argv[0])
