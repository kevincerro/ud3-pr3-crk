import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


def get_face_client():
    return FaceClient(os.environ.get('AZURE_FACE_ENDPOINT'), CognitiveServicesCredentials(os.environ.get('AZURE_FACE_KEY')))

def detect_faces_in_image(url: str):
    face_client = get_face_client()
    detected_faces = face_client.face.detect_with_url(url=url, detection_model='detection_03')

    if not detected_faces:
        raise Exception('No face detected.')

    return detected_faces
