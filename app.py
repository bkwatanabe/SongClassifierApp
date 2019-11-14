import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import librosa as lb

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS


# Flask app config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "audio"
app.config['JS'] = "static/js"
app.config['FAVICON'] = "static"


# Routing for homepage, static files, and the uploader
@app.route('/', methods=["GET"])
def homepage():
    return render_template('index.html')

# could include upload id to this to get the results for the specific song.
@app.route('/results', methods=["GET"])
def resultspage():
    return render_template('results.html')

@app.route('/js/<path:path>', methods=["GET"])
def get_send_js(path):
    return send_from_directory(app.config['JS'], path)


@app.route('/favicon.ico', methods=["GET"])
def get_favicon():
    return send_from_directory(app.config['FAVICON'], "favicon.ico")


# Endpoint for uploading files
# Accepts files if it has an allowed extension
# Else raises an error
@app.route('/uploader', methods=["POST"])
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    if allowed_file(filename):
        print("Uploaded ", f)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # x , sr = lb.load(f)
        x, sr = lb.load("audio/" + filename)
        print(sr, x)
        print(type(x))
        print(x.max())
        os.remove("audio/" + filename)
        return filename + " was uploaded successfully."
    else:
        raise ValueError(filename.rsplit('.', 1)[1].lower() + " is not an allowed file type.")


if __name__ == '__main__':
    app.run()
