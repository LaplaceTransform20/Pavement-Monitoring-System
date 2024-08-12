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

SHARED_DRIVE_ID = "0AJgwtlVQm-JQUk9PVA"
ROOT_FOLDER_ID = "17wGYvqdbXFs_U47XpB89Rcu9DYWrPl4L"


config = 'ArduCAM_108MP_MIPI_2Lane_RAW8_12000x9000_1.4fps-1.cfg'

#Main Program Loop
while True:
    #Create a datetime object containing current time and date
    now = dt.now()
    #If time is 2:00PM (14:00) and within first minute, then take images
    if now.hour==14 and now.minute==11:
        #Take image at 20MP resolution
        ret20, img20 = CaptureThread_20MP()
        time.sleep(5)
        img108 = Capture_Thread_108MP.main(config)

        time.sleep(2)
        saveFrame_Local('20MP', img20)
        time.sleep(2)
        saveFrame_Local('108MP', img108)
        
        source_folder = "./Captures"    # Local folder (to-be-uploaded)
        destination_folder = "Samples"  # Destination folder (Shared Drive)
     
        source_dir = Path(source_folder)
        files = list(source_dir.glob("**/*"))
        print(files)
        
        drive = GoogleDrive()
       
        #Uploads each image to google drive
        for file in files:
            drive.upload_file(file, destination_folder)
        time.sleep(5)

    time.sleep(5)
    print(now)


