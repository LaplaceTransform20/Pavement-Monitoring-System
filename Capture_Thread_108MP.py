import argparse
from typing import Optional, cast
import time
import cv2
import ArducamEvkSDK
from ArducamEvkSDK import Camera, Param, LoggerLevel, Frame

from img_cvt_utils import show_image, convert_image

#config = 'ArduCAM_108MP_MIPI_2Lane_RAW8_12000x9000_1.4fps-1.cfg'
config = 'ArduCAM_108MP_MIPI_2Lane_RAW8_4000x3000_12fps.cfg'

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


def log_callback(level, msg):
    print(msg)


def main(config, cameraParameters):
    print("ArducamEvkSDK Version: {}".format(ArducamEvkSDK.__version__))

    camera = Camera()
    param = Param()
    param.config_file_name = config
    param.bin_config = config.endswith(".bin")
    
    r = camera.open(param)
    
    #If no supported device found, then the program ends
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
    
    #show all controls
    for ct in camera.controls:
        print("{}({}): range({}:{}:{}), default={}".format(ct.name, ct.func, ct.min, ct.max, ct.step, ct.default))
    
    #Sets all control parameters of the camera module, based on the users input
    camera.set_control("setFocus", cameraParameters["Sensor_Focus"])
    camera.set_control("setFramerate", cameraParameters["Sensor_Framerate"])
    camera.set_control("setExposureTime", cameraParameters["Sensor_Exposure_Time"])
    camera.set_control("setGain", cameraParameters["Sensor_Analog_Gain"])
    camera.set_control("setDigitalGainR", cameraParameters["Sensor_Digital_Gain(R)"])
    camera.set_control("setDigitalGainB", cameraParameters["Sensor_Digital_Gain(B)"])
    camera.set_control("setEnableGamma" , cameraParameters["ISP_Gamma_Gain_Enable"])
    camera.set_control("setGainR", cameraParameters["ISP_Gain(R)"])
    camera.set_control("setGainB", cameraParameters["ISP_Gain(B)"])
    
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
            #break
            
        time_end = time.time()
        diff = time_end - time_start
        cv2.waitKey(1)
        
        if diff >= 5 and image is not None:
            break
        
    cv2.destroyAllWindows()
    camera.stop()
    camera.close()
    
    #Convert the image data into a image array
    img108MP = convert_image(image.data, image.format)
    
    #cv2.imwrite("/home/SamuelRPI/Desktop/PavMonSystem/Cam_Interface_Testing/Captures/108MP_TestImage.tiff", img108MP)
    #print("Save Successful")
    return img108MP
    

#Runs Arducam 108MP imaging function with config file, and 3 parameters
#Sensor Focus (0-1023), Analog Gain (0-1600), Exposure Time (26-83734)
main(config, camera_Parameters_108MP)

