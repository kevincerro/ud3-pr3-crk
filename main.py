from flask import Flask, render_template, request
from services import face_service

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template('home.html')


@app.route("/results", methods=['POST'])
def results():
    url = request.form.get('url')

    detected_faces = face_service.detect_faces_in_image(url)

    return render_template('results.html', image_url=url, faces=detected_faces)
