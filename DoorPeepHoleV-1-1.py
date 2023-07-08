#import libraries for PiCamera, Motion Sensor and LED
from picamera import PiCamera
from gpiozero import MotionSensor, LED
from time import sleep
from datetime import datetime
from Replace_with_family import replacePicture, deletePictures

# import libraries for face API
from FaceKey import cog_endpoint, cog_key
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os
import glob
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

camera = PiCamera()
msensor = MotionSensor(23)
greenLED = LED(17)
redLED = LED(27)

##--- Main Program
# Startup for MotionSensor
sleep(60)
print('Sensor is in READY State')
greenLED.off()
redLED.off()
# infinite loop

while True:
    replacePicture()
    knownPerson = 0
    msensor.wait_for_motion()
    deletePictures()

    for i in range(4):
        try:
            camera.capture('/home/pi/PiDoorCamera/door{}.jpg'.format(datetime.now()))
            sleep(0.1)
            
            #Identify a face against a defined PersonGroup
            
            # Group image for testing against
            test_image_array = sorted(glob.glob('/home/pi/PiDoorCamera/door*.jpg'))
            image = open(test_image_array[i], 'r+b')
            print(test_image_array[i])

            # Detect faces
            face_ids = []
            # We use detection model 2 because we are not retrieving attributes.
            faces = face_client.face.detect_with_stream(image, detectionModel='detection_02')
            for face in faces:
                face_ids.append(face.face_id)
            image.close()

            # If no faces in list then move to next iteration of loop
            if len(face_ids) == 0:
                continue
            else:
                # Identify faces
                results = face_client.face.identify(face_ids, 'family')
                for person in results:
                    if len(person.candidates) > 0:
                        # set knownPerson value for LED    
                        knownPerson += 1
                            
        except Exception as e:
            print(str(e))
            continue
         
    if knownPerson > 0:
            # Light green LED
            greenLED.on()
            sleep(30)
            greenLED.off()
            deletePictures()
    else:
            # Light red LED
            redLED.on()
            sleep(30)
            redLED.off()
            deletePictures()
    
