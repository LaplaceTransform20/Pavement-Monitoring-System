import numpy as np
import cv2 as cv
import time
import json

#from datetime import datetime as dt
from datetime import datetime, timedelta
from gdrive import GoogleDrive

import Capture_Thread_108MP
from Capture_Thread_20MP import *
from imgScript_Utilities import *

import argparse
import io
import os
import os.path
from pathlib import Path

SHARED_DRIVE_ID = "0AJgwtlVQm-JQUk9PVA"
ROOT_FOLDER_ID = "17wGYvqdbXFs_U47XpB89Rcu9DYWrPl4L"

config108MP = 'ArduCAM_108MP_MIPI_2Lane_RAW8_12000x9000_1.4fps-1.cfg'


parser = argparse.ArgumentParser()
parser.add_argument("--hour", default=12, type=int)
parser.add_argument("--minute", default=00, type=int)
parser.add_argument("--images-per-day", default=1, type=int)
config = parser.parse_args()


hour = config.hour
minute = config.minute
images_per_day = config.images_per_day

num_images = 24*60
interval = 24 * 60 // images_per_day
today = datetime.now().date()
start_time = datetime(year=today.year,
                      month=today.month,
                      day=today.day,
                      hour=hour,
                      minute=minute)

def get_next_time(start_time, interval):
    next_time = start_time
    while next_time < datetime.now():
        next_time += timedelta(minutes=interval)
    
    print(f"Next camera capture time:\t{next_time}")
    return next_time

next_time = get_next_time(start_time, interval)


#Main Program Loop
while True:

    now = datetime.now().replace(second=0, microsecond=0) 
    if now == next_time:
        
        #Take 20MP image
        ret20, img20 = CaptureThread_20MP()
        time.sleep(5)
        
        #Open JSON file 
        f = open('Camera_108MP_Parameters.json')
        
        #returns json object as dictionary containing camera parameters
        camParam = json.load(f)
        
        #Take 108MP image
        img108 = Capture_Thread_108MP.main(config108MP, camParam)
        
        #Close the json file
        f.close()
        
        time.sleep(2)
        filename_20MP = saveFrame_Local('20MP', img20)
        time.sleep(2)
        filename_108MP = saveFrame_Local('108MP', img108)
        
        
        source_folder_20MP = "./Captures_20MP_Local/"    # Local folder containing 20MP Images (to-be-uploaded)
        source_folder_108MP = "./Captures_108MP_Local/"  # Local Folder containing 108MP Images (to-be-uploaded)
        
        destination_folder_20MP = "Captures_20MP_Drive"  # Destination folder for 20MP Images (Shared Drive)
        destination_folder_108MP = "Captures_108MP_Drive" # Destination folder for 108MP Images (Shared Drive)
        

        path_20MP_file = source_folder_20MP+filename_20MP     # Path to the most recent 20MP image to be uploaded
        path_108MP_file = source_folder_108MP+filename_108MP  # Path to the most recent 108MP to be uploaded
        

        drive = GoogleDrive()
       
        #Uploads each image to google drive
        try:
            drive.upload_file(path_20MP_file, destination_folder_20MP)
        except:
            print("Upload Failed")
            pass
            
        try:
            drive.upload_file(path_108MP_file, destination_folder_108MP)
        except:
            print("Upload Failed")
            pass
            
            
        #Gets the next time for image capture
        next_time = get_next_time(start_time, interval)
        start_time = next_time
    
