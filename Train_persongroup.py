from FaceKey import cog_endpoint, cog_key
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import glob
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import sys
import time
import os

PERSON_GROUP_ID = str('family')
TARGET_PERSON_GROUP_ID = str('family')
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))
'''
Detect faces and register to correct person
'''

# Define dad
daniel = face_client.person_group_person.create(PERSON_GROUP_ID, "Dad")
# Define mom
shan = face_client.person_group_person.create(PERSON_GROUP_ID, "Mom")

# Find all jpeg images of friends in working directory
daniel_images = [file for file in glob.glob('*.jpg') if file.startswith("d")]
shan_images = [file for file in glob.glob('*.jpg') if file.startswith("s")]

# Add to a dad person
for image in daniel_images:
    d = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, daniel.person_id, d)

# Add to a mom person
for image in shan_images:
    s = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, shan.person_id, s)

'''
Train PersonGroup
'''
print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)
