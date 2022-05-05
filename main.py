from flask import Flask, render_template, request
from services import face_service, computer_vision_service

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template('home.html')


@app.route("/results", methods=['POST'])
def results():
    url = request.form.get('url')

    tags, color = computer_vision_service.analyze_image(url, 'es')

    image = {
        'faces': face_service.detect_faces_in_image(url),
        'description': computer_vision_service.describe_image(url, 'es'),
        'tags': tags,
        'color': color,
        'ocr': computer_vision_service.get_image_text(url, 'es', 36),
    }

    print(image)

    return render_template('results.html', image_url=url, image=image)
