import argparse
from typing import Optional, cast
import time
import cv2
import ArducamEvkSDK
from ArducamEvkSDK import Camera, Param, LoggerLevel, Frame

from img_cvt_utils import show_image, convert_image

config = 'ArduCAM_108MP_MIPI_2Lane_RAW8_12000x9000_1.4fps-1.cfg'


def log_callback(level, msg):
    print(msg)


def main(config):
    print("ArducamEvkSDK Version: {}".format(ArducamEvkSDK.__version__))

    camera = Camera()
    param = Param()
    param.config_file_name = config
    param.bin_config = config.endswith(".bin")
    
    r = camera.open(param)
    if not r:
        raise Exception("open camera error! ret={}".format(camera.last_error))
    camera.set_message_callback(log_callback)
    camera.log_level = LoggerLevel.Info

    print("SerialNumber: {}".format(''.join(chr(i) for i in camera.device.serial_number)))
    print("DeviceType: {}".format(camera.usb_type))
    print("DeviceSpeed: {}".format(camera.device.speed))
    print("VID:PID: {:04x}:{:04x}".format(camera.device.id_vendor, camera.device.id_product))

    camera.init()
    camera.start()
    config = camera.config
    

    print("config.width={}, config.height={}".format(config.width, config.height))
    
    time_start = time.time()
    
    while True:
        image = cast(Optional[Frame], camera.capture(1000))
        if image is None:
            continue
        show_image(image) 
        
        print(f"get frame({image.format.width}x{image.format.height}) from camera.")
        
        #key = cv2.waitKey(1)
        #if key == ord('q'):
            #cv2.destroyAllWindows
        time_end = time.time()
        diff = time_end - time_start
        
        if diff >= 5 and image is not None:
            break
        
    cv2.destroyAllWindows()
    camera.stop()
    camera.close()
    
    #Convert the image data into a image array
    img108MP = convert_image(image.data, image.format)
    
    return img108MP
    

#Running 108MP imaging function with config file     
main(config)

