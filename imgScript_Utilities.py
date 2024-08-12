import cv2 as cv
import numpy as np
import time

from datetime import datetime as dt

#Saves inputted image as a tiff file, with name based on resolution, Date, Month and Year
def saveFrame_Local(res, img):
    now = dt.now()
    if res=='20MP':
        cv.imwrite('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures/Capture_20MP_'+now.strftime("%Y-%b-%d") + '.tiff', img)
        print("20MP Local Save Successful")
    elif res=='108MP':
        cv.imwrite('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures/Capture_108MP_'+now.strftime("%Y-%b-%d")+'.tiff', img)
        print("108MP Local Save Successful")
        
        
#Displays Frame given, scaled to some percentage      
def displayFrame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)
    cv.imshow('Most Recent Frame', frame)