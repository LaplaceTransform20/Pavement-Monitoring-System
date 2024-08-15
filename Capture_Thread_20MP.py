import cv2 as cv
import numpy as np
import time


def CaptureThread_20MP():
    
    #setup Arducam 20MP Camera Module (UVC camera) Object - /dev/video0
    cam20MP = cv.VideoCapture(0)
    
    height_20 = 3672
    width_20 = 5496
    cam20MP_PREV_FRAME_RATE = 9

    #Set resolution of 20MP camera to 5496(H)x3672(V)
    cam20MP.set(cv.CAP_PROP_FRAME_HEIGHT,height_20)
    cam20MP.set(cv.CAP_PROP_FRAME_WIDTH, width_20)
    #Set fps of the video capture
    cam20MP.set(cv.CAP_PROP_FPS, cam20MP_PREV_FRAME_RATE)
    print('20MP Camera set')
    
    end = False
    time_start=time.time()
    while end == False:
        ret, img = cam20MP.read()
        #cv.imshow("IMG", img)
        time_end = time.time()
        diff = time_end - time_start
        #once at least 5 sec has passed, display the current frame.
        if diff >= 5 and ret == True:
            #returns the final frame captured
            print("20MP Capture Successful")
            return ret, img
            end = True
        else:
            end = False
            
