# app.py
import sys
import os

# Ensure Python can see utils folder
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils.detection import detect_animals
from utils.map_alert import plot_on_map

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Detect animals
            detections = detect_animals(filepath)

            # Optional: Map alert
            map_file = plot_on_map(detections)

            return render_template("result.html", detections=detections, map_file=map_file)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)