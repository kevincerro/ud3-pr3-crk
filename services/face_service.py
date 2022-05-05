import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


def get_client():
    return FaceClient(
        os.environ.get('AZURE_FACE_ENDPOINT'),
        CognitiveServicesCredentials(os.environ.get('AZURE_FACE_KEY'))
    )


def detect_faces_in_image(url: str):
    client = get_client()

    attributes = ['age', 'emotion']
    detected_faces = client.face.detect_with_url(url=url, return_face_attributes=attributes)

    if not detected_faces:
        return []

    # Find emotion with better score
    for face in detected_faces:
        emotions = face.face_attributes.emotion
        face.emotion = get_most_scored_emotion(emotions)

    return detected_faces


def get_most_scored_emotion(emotions):
    scores = {
        'anger': emotions.anger,
        'contempt': emotions.contempt,
        'disgust': emotions.disgust,
        'fear': emotions.fear,
        'happiness': emotions.happiness,
        'neutral': emotions.neutral,
        'sadness': emotions.sadness,
        'surprise': emotions.surprise,
    }

    name = max(scores, key=scores.get)
    score = scores[name]

    return {
        'name': name,
        'score': score,
    }
