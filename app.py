from base64 import b64encode
import io
import os
from PIL import Image
from flask import (
    Flask,
    Response,
    abort,
    jsonify,
    request,
    send_file,
    send_from_directory,
)
from flask_cors import CORS
from predict import get_prediction
from werkzeug.utils import secure_filename
from storage import upload_file


app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():
    return "Hello World"


@app.route("/predict", methods=["POST"])
def predict():
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
            image_result = get_prediction(image_bytes)
            image_result_path = f"tmp-{filename}"
            image_result.save(image_result_path)
            uploaded = upload_file(image_result_path)
            os.remove(image_result_path)
            results.append(uploaded)

        return results
    return jsonify({"Error": "Method not allowed"})


# @app.route("/<path:filename>")
# def image(filename):
#     try:
#         width = int(request.args["width"])
#         height = int(request.args["height"])
#     except (KeyError, ValueError):
#         return send_from_directory("static", filename)

#     try:
#         im = Image.open(filename)
#         im.thumbnail((width, height), Image.ANTIALIAS)
#         bytes_io = io.BytesIO()
#         im.save(bytes_io, format="JPEG")
#         return Response(bytes_io.getvalue(), mimetype="image/jpeg")

#     except IOError:
#         abort(404)

#     return send_from_directory("static", filename)
