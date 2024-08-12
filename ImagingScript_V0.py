import numpy as np
import cv2 as cv
import time
from datetime import datetime as dt
from gdrive import *

import Capture_Thread_108MP


import io
import os
#import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
PARENT_FOLDER_ID = "1rX00Mr-VHCY3J1Hw0SHAXIs3XAc6Rzmy"
RAW_IMAGES_ID = "1gaLhsWlUP_Iwv5BQ7oosbHLB0yZIlkEC"

#Creates crendentials using the JSON key containing service account credentials
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)

#Build the Google Drive Service
service = build('drive', 'v3', credentials = creds)


#setup Arducam 20MP Camera Module (UVC camera) - /dev/video0
cam20MP = cv.VideoCapture(0)

height_20 = 3672
width_20 = 5496
cam20MP_PREV_FRAME_RATE = 9

#Set resolution of 20MP camera to 5496(H)x3672(V)
cam20MP.set(cv.CAP_PROP_FRAME_HEIGHT,height_20)
cam20MP.set(cv.CAP_PROP_FRAME_WIDTH, width_20)
cam20MP.set(cv.CAP_PROP_FPS, cam20MP_PREV_FRAME_RATE)


def CaptureThread_20MP():
    end = False
    time_start=time.time()
    while end == False:
        ret, img = cam20MP.read()
        #cv.imshow("IMG", img)
        time_end = time.time()
        diff = time_end - time_start
        #once at least 5 sec has passed, display the current frame.
        if diff >= 5:
            #returns the final frame captured
            print("20MP Capture Successful")
            return ret, img
            end = True
        else:
            end = False

def displayFrame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)
    cv.imshow('Most Recent Frame', frame)

#Saves inputted image as a tiff file, with name based on resolution, Date, Month and Year
def saveFrame_Local(res, img):
    now = dt.now()
    if res=='20MP':
        cv.imwrite('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures/Capture_20MP_'+now.strftime("%Y-%b-%d") + '.tiff', img)
        print("20MP Local Save Successful")
    elif res=='108MP':
        cv.imwrite('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures/Capture_108MP_'+now.strftime("%Y-%b-%d")+'.tiff', img)
        print("108MP Local Save Successful")



def uploadFile_V1(file_path, name):

    file_metadata = {
        'name' : name,
        'parents': [PARENT_FOLDER_ID]
        }
    file = service.files().create(
        body = file_metadata,
        media_body = file_path,
        fields = 'id'
        ).execute()

def create_folder(folder_name, parent_folder_id = None):
    """Create a folder in Google Drive and return its ID."""
    folder_metadata = {
        'name': folder_name,
        'mimeType': "application/vnd.google-apps.folder",
        'parents': [parent_folder_id] if parent_folder_id else []
        }

    created_folder = service.files().create(
        body = folder_metadata,
        fields = 'id'
        ).execute()
    print(f'Created Folder ID: {created_folder["id"]}')
    return created_folder["id"]



config = 'ArduCAM_108MP_MIPI_2Lane_RAW8_12000x9000_1.4fps-1.cfg'
#Capture_Thread_108MP.main(config)

#Main Program Loop
while True:
    #Create a datetime object containing current time and date
    now = dt.now()
    #If time is 2:00PM (14:00) and within first minute, then take images
    if now.hour==0 and now.minute==56:
        #Take image at 20MP resolution
        ret20, img20 = CaptureThread_20MP()
        time.sleep(5)
        img108 = Capture_Thread_108MP.main(config)

        time.sleep(5)
        saveFrame_Local('20MP', img20)
        time.sleep(5)
        saveFrame_Local('108MP', img108)

    time.sleep(5)
    print(now)

