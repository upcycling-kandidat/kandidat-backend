from base64 import b64encode
from utils import remove_background
import io
import os
from PIL import Image
from flask import (
    Flask,
    jsonify,
    request,
)
from werkzeug.utils import secure_filename
from flask_cors import CORS
from predict import (
    get_components,
    get_materials,
    get_dimensions,
    get_colors,
    get_defects
)
from storage import upload_file
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'ERROR',
        'handlers': ['file']
    }
})


app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET"])
def index():
    return "upcycling-kandidat"

@app.route("/components", methods=["POST"])
def components():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"Error": "No files was sent, try againg"})

        uploaded_files = request.files.getlist("file")
        results = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            allowed = allowed_file(filename)

            if not allowed:
                return jsonify({"Error": "File type not allowed"})

            image_bytes = file.read()
            defects = get_components(image_bytes, filename)
            results.append(defects)

        return results
    return jsonify({"Error": "Method not allowed"})


@app.route("/materials", methods=["POST"])
def materials():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"Error": "No files was sent, try againg"})

        uploaded_files = request.files.getlist("file")
        results = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            allowed = allowed_file(filename)

            if not allowed:
                return jsonify({"Error": "File type not allowed"})

            image_bytes = file.read()
            material = get_materials(image_bytes)
            results.append(material)

        return results
    return jsonify({"Error": "Method not allowed"})

@app.route("/dimensions", methods=["POST"])
def dimensions():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"Error": "No files was sent, try againg"})

        uploaded_files = request.files.getlist("file")
        results = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            allowed = allowed_file(filename)

            if not allowed:
                return jsonify({"Error": "File type not allowed"})

            image_bytes = file.read()
            dimensions = get_dimensions(image_bytes, filename)
            results.append(dimensions)

        return results
    return jsonify({"Error": "Method not allowed"})

@app.route("/transparent", methods=["POST"])
def transparent():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"Error": "No files was sent, try againg"})

        uploaded_files = request.files.getlist("file")
        results = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            allowed = allowed_file(filename)

            if not allowed:
                return jsonify({"Error": "File type not allowed"})

            image_bytes = file.read()
            transparent = remove_background(image_bytes, filename)
            results.append(transparent)

        return results
    return jsonify({"Error": "Method not allowed"})

@app.route("/colors", methods=["POST"])
def colors():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"Error": "No files was sent, try againg"})

        uploaded_files = request.files.getlist("file")
        results = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            allowed = allowed_file(filename)

            if not allowed:
                return jsonify({"Error": "File type not allowed"})

            image_bytes = file.read()
            colors = get_colors(image_bytes)
            results.append(colors)

        return results
    return jsonify({"Error": "Method not allowed"})

@app.route("/defects", methods=["POST"])
def defects():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"Error": "No files was sent, try againg"})

        uploaded_files = request.files.getlist("file")
        results = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            allowed = allowed_file(filename)

            if not allowed:
                return jsonify({"Error": "File type not allowed"})

            image_bytes = file.read()
            defects = get_defects(image_bytes, filename)
            results.append(defects)

        return results
    return jsonify({"Error": "Method not allowed"})