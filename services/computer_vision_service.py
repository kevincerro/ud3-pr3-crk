import os
import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials


def get_client():
    return ComputerVisionClient(
        os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT'),
        CognitiveServicesCredentials(os.environ.get('AZURE_COMPUTER_VISION_KEY'))
    )


def describe_image(url: str, lang: str):
    client = get_client()

    analysis = client.describe_image(url, 1, lang)

    if not analysis:
        raise Exception('No analysis returned.')

    return analysis.captions[0].text


def analyze_image(url: str, lang: str):
    client = get_client()

    features = [
        VisualFeatureTypes.tags,
        VisualFeatureTypes.color,
    ]

    analysis = client.analyze_image(url, visual_features=features, language=lang)

    tags = [tag.name for tag in analysis.tags]
    color = analysis.color.accent_color

    return tags, color


def get_image_text(url: str, lang: str, max_chars: int):
    client = get_client()

    # Request OCR
    analysis = client.read(url, language=lang, raw=True)
    location = analysis.headers["Operation-Location"]
    id_location = len(location) - max_chars
    operation = location[id_location:]

    # Wait until OCR completes
    i = 0
    while True:
        result = client.get_read_result(operation)

        if i >= 10 or result.status == OperationStatusCodes.succeeded:
            break

        i = i + 1
        time.sleep(1)

    return [line.text for line in result.analyze_result.read_results[0].lines]
