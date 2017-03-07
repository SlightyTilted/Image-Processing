#Written by Kyle, help provided by Sean Devenport
import numpy as np
import cv2

def main():
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

	vidcap = cv2.VideoCapture(0)

	while True:
		flg, img=vidcap.read()
		gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		if flg:
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			for (x,y,w,h) in faces:
			    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
			    roi_gray = gray[y:y+h, x:x+w]
			    roi_color = img[y:y+h, x:x+w]
			    eyes = eye_cascade.detectMultiScale(roi_gray)
			    for (ex,ey,ew,eh) in eyes:
			        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

			cv2.imshow('img',img)
			if cv2.waitKey(2) & 0xFF == 27:
				break
		else:
			break
	vidcap.release()
	cv2.destroyAllWindows()

main()
