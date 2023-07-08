#-- Creating a person group and adding people for recognition
## importing resources
from FaceKey import cog_endpoint, cog_key
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os

PERSON_GROUP_ID = str('family')
TARGET_PERSON_GROUP_ID = str('family')
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))


#Create the PersonGroup

# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

# Define dad
daniel = face_client.person_group_person.create(PERSON_GROUP_ID, "Dad")
# Define mom
shan = face_client.person_group_person.create(PERSON_GROUP_ID, "Mom")
