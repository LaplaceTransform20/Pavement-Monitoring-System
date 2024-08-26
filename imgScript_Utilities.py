import cv2 as cv
import numpy as np
import time

from datetime import datetime as dt

#Saves inputted image as a tiff file, with name based on resolution, Date, Month and Year
def saveFrame_Local(res, img):
    now = dt.now()
    
    if res=='20MP':
        filename = 'Capture_20MP_' + now.strftime("%Y-%m-%-d_%-H-%-M-%-S") + '.tiff'
        cv.imwrite('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures_20MP_Local/' + filename, img)
        print("20MP Local Save Successful")
        return filename
    elif res=='108MP':
        filename = 'Capture_108MP_' + now.strftime("%Y-%m-%-d_%-H-%-M-%-S") + '.tiff'
        cv.imwrite('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures_108MP_Local/' + filename, img)
        print("108MP Local Save Successful")
        return filename
        
        
#Displays Frame given, scaled to some percentage      
def displayFrame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)
    cv.imshow('Most Recent Frame', frame)
    
