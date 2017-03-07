import cv2 as cv
import numpy as np
import csv
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from wand.image import Image
# from matplotlib import pyplot as plt
from array import array

#RUN THE FIRST TIME TO BREAK PDF INTO JPG IMAGES (1 per page)

# with Image(filename = "MCQ_600dpi_2016.pdf",resolution=(300,300))as img:
#     img_width = img.width
#     ratio     = 2483 / img_width
#     img.resize(2483, int(ratio * img.height))
#     img.format = 'jpeg'
#     img.save(filename = "img.jpg")

#VARIABLES FOR PROJECT
threshold = 0.8
blockx = 330
blocky = 320

xdiff = 620
ydiff = 70

def writeToCSV():
    with open('results.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter= ",",
                                quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        spamwriter.writerow([stuNum, task, qNum, ans])

def getStudentNumber(image):
    global value, taskar, stuChar
    stutemp = cv.imread('templates/studentTemplate.jpg',0)
    cheight, cwidth = stutemp.shape[::-1]
    matchedn = cv.matchTemplate(image, stutemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(matchedn)
    top_left = max_loc
    pointx = top_left[0] #pointx = top_left coordinate of 1stcorner
    pointy = top_left[1] #pointy = y coord of top left corner of 1st corner
    bottom_right = (top_left[0] + cheight, top_left[1] + cwidth)
    bottom_left = (top_left[0],top_left[1]+cwidth)
    print(bottom_right)
    print(bottom_left)

    roi = image[bottom_left[1]:bottom_left[1]+1494, bottom_left[0]:bottom_left[0]+410]
    small = cv.resize(roi, (0,0), fx=0.3, fy=0.3)
    #cv.imshow("student block", small)
    #cv.imwrite('studentblock.ppm', roi )
    #stublock = cv.cvtColor(roi, cv.COLOR_BGR2GRAY) #will be used for template matching (or the setup thereof)

    ret,stublockac = cv.threshold(roi, 127,255,cv.THRESH_BINARY)                                                            #will be used to write circles to blob
    xoff = 57                                                                  #move 57 pixels to get to next column
    yoff = 57
                                                                                #move 65 pixels to go down a letter
    #ret, atemp = cv.threshold(atemp, 127, 255, cv.THRESH_BINARY)
    #colPix = cv.countNonZero(threshquestion)
    value = []
    yhold =0
    xhold =10
    letter = 0
    for i in range(0,7):                                                        #i = columns

        #MAKE IF STATEMENT FOR COLUMN 2
        # if i == 2:
        if i ==2:
            for j in range(0,27):
                start = stublockac[yhold:yhold+65, xhold:xhold+57]
                counter = cv.countNonZero(start)
                #print(counter)
                if counter < 2500:
                    letter = j
                    yhold = yhold + yoff
                    break
                yhold = yhold + yoff
            xhold = xhold + xoff
            yhold =0
            continue
        for j in range(0,10):    #ROWS
            start = stublockac[yhold:yhold +65, xhold:xhold +57]
            counter = cv.countNonZero(start)
            #print(counter)
            if counter < 2800:
                value.append(j)
                yhold = yhold + yoff
                break
            yhold = yhold + yoff
            #print(yhold)
            #print(xhold)

        xhold = xhold+xoff
        yhold = 0

    stuChar = ""
    if letter == 0:
        stuChar="A"
    if letter == 1:
        stuChar="B"
    if letter == 2:
        stuChar="C"
    if letter == 3:
        stuChar="D"
    if letter == 4:
        stuChar="E"
    if letter == 5:
        stuChar="F"
    if letter == 6:
        stuChar="G"
    if letter == 7:
        stuChar="H"
    if letter == 8:
        stuChar="I"
    if letter == 9:
        stuChar="J"
    if letter == 10:
        stuChar="K"
    if letter ==11:
        stuChar="L"
    if letter == 12:
        stuChar="M"
    if letter == 13:
        stuChar="N"
    if letter == 14:
        stuChar="O"
    if letter == 15:
        stuChar="P"
    if letter == 16:
        stuChar="Q"
    if letter == 17:
        stuChar="R"
    if letter == 18:
        stuChar="S"
    if letter == 19:
        stuChar="T"
    if letter == 20:
        stuChar="U"
    if letter == 21:
        stuChar="V"
    if letter == 22:
        stuChar="W"
    if letter == 23:
        stuChar="X"
    if letter == 24:
        stuChar="Y"
    if letter == 25:
        stuChar = "Z"

    print(letter)

    taskstx = 276
    tasksty = 710
    taskar = []
    for i in range(0,2):                                                        #i = columns
        #MAKE IF STATEMENT FOR COLUMN 2
        # if i == 2:
        for j in range(0,9):    #ROWS
            start = stublockac[tasksty:tasksty +65, taskstx:taskstx +57]
            counter = cv.countNonZero(start)
            #print(counter)
            if counter < 2800:
                if j != 0:
                    taskar.append(j)
                tasksty = tasksty + yoff
                break
            tasksty = tasksty + yoff
            #print(tasksty)
            #print(taskstx)

        taskstx = taskstx+ xoff
        tasksty = 710

    # print(value)
    # print(taskar)
    return value

def cornerfind(imagevar):
    global pointx, pointy, cheight, cwidth, img, img2, pos, threshold, simage
    #SETUP CORNER templates
    cornertemp = cv.imread('templates/cornertemplate.jpg',0)
    cheight, cwidth = cornertemp.shape[::-1]
    simage = imagevar.copy()
    pos =[]
    for n in range(0,4):
        matched = cv.matchTemplate(imagevar, cornertemp, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(matched)

        top_left = max_loc
        pointx = top_left[0] #pointx = top_left coordinate of 1stcorner
        pointy = top_left[1] #pointy = y coord of top left corner of 1st corner
        bottom_right = (top_left[0] + cwidth, top_left[1] + cheight)

        if max_val >= threshold:
            topLeftx=max_loc[0]
            topLefty = max_loc[1]
            centre = topLeftx + cwidth/2, topLefty + cheight/2
            pos.append(centre)
            cv.rectangle(imagevar, max_loc, (max_loc[0]+cwidth, max_loc[1]+cheight), (0,0,255), -2)

    #print(pos)
    minP = min(pos)
    pointy= minP[1]
    pointx=minP[0]
    #print(minP)
    if pointy<200:              #rotate image if needed
        imagevar =cv.flip(imgtemp,-1)
        simage = cv.flip(imgtemp,-1)
        img2=cv.cvtColor(imagevar, cv.COLOR_GRAY2RGB)
        cornerfind(imagevar)
        # matched = cv.matchTemplate(imagevar, cornertemp, cv.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(matched)
        # top_left = max_loc

    return matched
#ALIGNMENT METHOD
def align(img, corners):
    result = img.copy()
    h, w = np.shape(result)
    if corners[0][1] != corners[1][1]:
        xd = corners[0][0] - corners[1][0]
        yd = corners[0][1] - corners[1][1]
        grad = yd/xd
        theta = np.arctan(grad)
        A = cv.getRotationMatrix2D((w/2,h/2),theta,1)
        result = cv.warpAffine(result,A,(w,h))
        cv.imwrite('align.ppm',result)
        matchi = cornerfine(result)
        corners = pos
        print corners
    return result
#Align ends


#START OF MAIN
def Main():
    global img, imgtemp, img2, res, heigh, width, matched, ydiff, xdiff, atemp, btemp, ctemp, dtemp, etemp, pos, emptytemp, simage, stuNum, task, qNum
    emptytemp = cv.imread('templates/emptytemplate.jpg',0)
    kernel = np.ones((5,5),np.uint8)
    emptytemp = cv.dilate(emptytemp,kernel,iterations = 2)
    page = int(sys.argv[1])
    img = cv.imread('images/img-%i.jpg'%(page,),0)
    #imgtemp = cv.imread('images/img-9.jpg',0)
    imgtemp = img.copy()
    img2 = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    res = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    height, width = img.shape
    matched =cornerfind(img);                                                   #find corners of MCQ
    studentNumber =getStudentNumber(simage)
    #.imshow("block %i" % (i,), blocka)
    stuNum = "g"
    counter =0;
    for i in studentNumber[0:]:
        counter = counter +1
        if counter == 2:
            stuNum = stuNum + stuChar
        stuNum = stuNum + str(i)
    #STUDENT NUMBER = stunum

    if len(stuNum)< 8:
        stuNum = "invalid student number"

    task = ""
    for i in taskar[0:]:
        task = task + str(i)
    #TASK NUMBER = task

    if len(task)< 2:
        task = "invalid task number"
    #img =align(img,pos)     #FIX ALIGNMENT METHOD
    tempydiff = ydiff
    checker = False
    qNum=1
    for i in range(0,13):
        if i < 6:

            getBlock()
            ydiff = ydiff + 325
            q1 = blocka[starty-25: starty+25, startx-25: startx+210]
            q2 = blocka[50+starty-25: 50+starty+25, startx-25: startx+210]
            q3 = blocka[100+starty-25: 100+starty+25, startx-25: startx+210]
            q4 = blocka[150+starty-25: 150+starty+25, startx-25: startx+210]
            q5 = blocka[200+starty-25: 200+starty+25, startx-25: startx+210]

            questionTemp(q1)
            qNum =qNum +1
            questionTemp(q2)
            qNum =qNum +1
            questionTemp(q3)
            qNum =qNum +1
            questionTemp(q4)
            qNum =qNum +1
            questionTemp(q5)
            qNum =qNum +1
            print("\n")

            cv.imshow("block %i" % (i,), blocka)
    #cv.imwrite("blocka.png", blocka)
            cv.waitKey(0)
            cv.destroyAllWindows

        if i == 6:
            ydiff = tempydiff
            xdiff = xdiff + 470

        if i > 6:

            getBlock()
            ydiff = ydiff + 325
            q1 = blocka[starty-25: starty+25, startx-25: startx+210]
            q2 = blocka[50+starty-25: 50+starty+25, startx-25: startx+210]
            q3 = blocka[100+starty-25: 100+starty+25, startx-25: startx+210]
            q4 = blocka[150+starty-25: 150+starty+25, startx-25: startx+210]
            q5 = blocka[200+starty-25: 200+starty+25, startx-25: startx+210]

            questionTemp(q1)
            qNum =qNum +1
            questionTemp(q2)
            qNum =qNum +1
            questionTemp(q3)
            qNum =qNum +1
            questionTemp(q4)
            qNum =qNum +1
            questionTemp(q5)
            qNum =qNum +1
            print("\n")
            cv.imshow("block %i" % (i,), blocka)
    #cv.imwrite("blocka.png", blocka)
            cv.waitKey(0)
            cv.destroyAllWindows

    #END OF MAIN

def getBlock():
    global startx, starty, blocka, blockac, circles

    roix = xdiff+pointx
    roiy = ydiff+pointy

    roi = img2[roiy: roiy+blocky, roix:roix+blockx]
#roi = img2[320:636, 692:1020]

    blocka = cv.cvtColor(roi, cv.COLOR_BGR2GRAY) #will be used for template matching (or the setup thereof)
# cv.imshow("before circles", blocka)
# cv.waitKey(0)
#cv.destroyAllWindow
    blockac = cv.cvtColor(roi, cv.COLOR_BGR2GRAY) #will be used to write circles to blob

    circles = cv.HoughCircles(blockac,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=25)

    circles = np.uint16(np.around(circles))

    SalientCircleX = []
    SalientCircleY = []
    for i in circles[0,:]:
    # draw the outer circle
        SalientCircleX.append(i[0])
        SalientCircleY.append(i[1])
        cv.circle(blockac,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
        cv.circle(blockac,(i[0],i[1]),2,(0,0,255),3)

    SalientCircleX.sort()
    SalientCircleY.sort()

    startx = SalientCircleX[0]
    starty = SalientCircleY[0]
    #END OF GETBLOCK METHOD

def questionTemp(question):
    global ans
    #question = cv.cvtColor(questiont, cv.COL)
    tempthresh = 0.1
    owidth, oheight = question.shape[::-1]
    hasmatched = False
    #print(oheight)

    kernel = np.ones((5,5),np.uint8)
    atemp = cv.imread('templates/atemplate.jpg',0)
    atemp = cv.erode(atemp,kernel,iterations = 1)
    atemp = cv.dilate(atemp,kernel, iterations = 1)
    ret, atemp = cv.threshold(atemp, 127, 255, cv.THRESH_BINARY)


    kernel = np.ones((5,5),np.uint8)
    btemp = cv.imread('templates/btemplate.jpg',0)
    btemp = cv.erode(btemp,kernel,iterations = 1)
    btemp = cv.dilate(btemp,kernel, iterations = 1)
    ret, btemp = cv.threshold(btemp, 127, 255, cv.THRESH_BINARY)

    kernel = np.ones((5,5),np.uint8)
    ctemp = cv.imread('templates/ctemplate.jpg',0)
    ctemp = cv.erode(ctemp,kernel,iterations = 1)
    ctemp = cv.dilate(ctemp,kernel, iterations = 1)
    ret, ctemp = cv.threshold(ctemp, 127, 255, cv.THRESH_BINARY)

    kernel = np.ones((5,5),np.uint8)
    dtemp = cv.imread('templates/dtemplate.jpg',0)
    dtemp = cv.erode(dtemp,kernel,iterations = 1)
    dtemp = cv.dilate(dtemp,kernel, iterations = 1)
    ret, dtemp = cv.threshold(dtemp, 127, 255, cv.THRESH_BINARY)

    kernel = np.ones((5,5),np.uint8)
    etemp = cv.imread('templates/etemplate.jpg',0)
    etemp = cv.erode(etemp,kernel,iterations = 1)
    etemp = cv.dilate(etemp,kernel, iterations = 1)
    ret, etemp = cv.threshold(etemp, 127, 255, cv.THRESH_BINARY)

    kernal = np.ones((5,5),np.uint8)
    question = cv.erode(question, kernal, iterations=1)
    question = cv.dilate(question,kernel, iterations = 1)
    ret, threshquestion = cv.threshold(question, 127, 255, cv.THRESH_BINARY)




    #Need to get intensity value for question, and then compare with intensity values of templates. Have thresholded question

    totPixelsinQ = owidth * oheight
    colPix = cv.countNonZero(threshquestion)
    zeroPixels = totPixelsinQ - cv.countNonZero(threshquestion)
    #print(zeroPixels)

    if zeroPixels>2500:
        print("invalid answer")
        ans = "invalid answer"
        writeToCSV()
        hasmatched = True


    amatched = cv.matchTemplate(question, atemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(amatched)


    if max_val >= tempthresh and hasmatched == False:
        print("answer = a")
        ans = "A"
        writeToCSV()
        hasmatched = True

    bmatched = cv.matchTemplate(question, btemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(bmatched)

    if max_val >= tempthresh and hasmatched == False:
        print("answer = b")
        ans = "B"
        writeToCSV()
        hasmatched = True


    cmatched = cv.matchTemplate(question, ctemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(cmatched)

    if max_val >= tempthresh and hasmatched == False:
        print("answer = c")
        ans = "C"
        writeToCSV()
        hasmatched = True

    dmatched = cv.matchTemplate(question, dtemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(dmatched)

    if max_val >= tempthresh and hasmatched == False:
        print("answer = d")
        ans = "D"
        writeToCSV()
        hasmatched = True

    ematched = cv.matchTemplate(question, etemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(ematched)

    if max_val >= tempthresh and hasmatched == False:
        print("answer = e")
        ans = "E"
        writeToCSV()
        hasmatched = True

    question = cv.dilate(question,kernel, iterations = 1)
    empmatched = cv.matchTemplate(question, emptytemp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(emptytemp)

    if max_val >= tempthresh and hasmatched== False:
        print("no answer supplied or invalid input")
        ans = "no answer supplied/invalid input"
        writeToCSV()
        hasmatched = True

    if hasmatched == False:
        print("invalid answer")


#END OF QUESTIONTEMP METHOD

Main()
