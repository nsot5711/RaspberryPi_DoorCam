from shutil import copyfile
import os
import glob
from datetime import datetime

def replacePicture():
    fileList = glob.glob('/home/pi/PiDoorCameraApp/data/family*.jpg')
    for filePath in fileList:
        try:
            copyfile(filePath, '/home/pi/PiDoorCamera/family{}.jpg'.format(datetime.now()))
        except:
            continue
    
def deletePictures():
    fileList = glob.glob('/home/pi/PiDoorCamera/*.jpg')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception as e:
            exceptionError = str(e)
            print(exceptionError)
    
