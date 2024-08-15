import numpy as np
import cv2 as cv
import time
from datetime import datetime as dt
from gdrive import GoogleDrive

import Capture_Thread_108MP
from Capture_Thread_20MP import *

from imgScript_Utilities import *

import io
import os
import os.path
from pathlib import Path
import RPI.GPIO as GPIO

LED_PIN_RED = 23
GPIO.setMode(LED_PIN_RED, GPIO.OUT)

SHARED_DRIVE_ID = "0AJgwtlVQm-JQUk9PVA"
ROOT_FOLDER_ID = "17wGYvqdbXFs_U47XpB89Rcu9DYWrPl4L"


config = 'ArduCAM_108MP_MIPI_2Lane_RAW8_12000x9000_1.4fps-1.cfg'

#Control Parameters for the 108MP Camera Module
camera_Parameters_108MP = {
    "Sensor_Focus" : 380,
    "Sensor_Framerate" : 1,
    "Sensor_Exposure_Time" : 65000,
    "Sensor_Analog_Gain" : 177,
    "Sensor_Digital_Gain(R)" : 126,
    "Sensor_Digital_Gain(B)" : 126,
    "ISP_Gamma_Gain_Enable" : 1,
    "ISP_Gain(R)" : 100,
    "ISP_Gain(B)" : 100,
    }

#Start with all LED's off
GPIO.output(LED_PIN_RED, GPIO.LOW)

#Main Program Loop
while True:
    #Red LED remains turned on constantly for entire program loop duration
    GPIO.output(LED_PIN_RED,GPIO.HIGH)    
    
    #Create a datetime object containing current time and date
    now = dt.now()
    #If time is 2:00PM (14:00) and within first minute, then take images
    if now.hour==15 and now.minute==44:
        #Take image at 20MP resolution
        
        ret20, img20 = CaptureThread_20MP()
        time.sleep(5)
        img108 = Capture_Thread_108MP.main(config, camera_Parameters_108MP)

        time.sleep(2)
        saveFrame_Local('20MP', img20)
        time.sleep(2)
        saveFrame_Local('108MP', img108)
        
        source_folder_20MP = "./Captures_20MP_Local"    # Local folder containing 20MP Images (to-be-uploaded)
        source_folder_108MP = "./Captures_108MP_Local"  # Local Folder containing 108MP Images (to-be-uploaded)
        
        destination_folder_20MP = "Captures_20MP_Drive"  # Destination folder for 20MP Images (Shared Drive)
        destination_folder_108MP = "Captures_108MP_Drive" # Destination folder for 108MP Images (Shared Drive)
        
        source_dir_20MP = Path(source_folder_20MP)
        source_dir_108MP = Path(source_folder_108MP)
        
        files_20MP = list(source_dir_20MP.glob("**/*"))
        files_108MP  = list(source_dir_20MP.glob("**/*"))
        
        print(files_20MP)
        print(files_108MP)
        
        drive = GoogleDrive()
       
        #Uploads each image to google drive
        for file in files_20MP:
            drive.upload_file(file, destination_folder_20MP)
            
        for file2 in files_108MP:
            drive.upload_file(file2, destination_folder_108MP)
        
        time.sleep(5)
        
        os.remove('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures_20MP_Local/Capture_20MP_'+now.strftime("%Y-%b-%d") + '.tiff')
        os.remove('/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures_108MP_Local/Capture_108MP_'+now.strftime("%Y-%b-%d")+'.tiff')

    time.sleep(5)
    print(now)

#If main loop ends, then Red LED is turned off
GPIO.output(LED_PIN_RED,GPIO.HIGH)
