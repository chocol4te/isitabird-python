import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
from werkzeug import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file:
        hash = hashlib.sha512(secure_filename(file.filename).encode('utf-8')).hexdigest()

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], hash))

        os.system("./infer.sh " + hash)

        return redirect(url_for('loading', hash=hash))

@app.route('/loading')
def loading():
    hash = request.args.get('hash')
    return render_template('loading.html', hash=hash)

@app.route('/results')
def results():
    filename = request.args.get('hash')
    filepath = "uploads/" + filename + ".txt"
    output = open(filepath, "r").read()
    bird = output.rpartition('-')[0].rstrip()
    notbird = output.rpartition('-')[2].rstrip()

    os.system("rm uploads/" + filename + "*")

    return render_template('results.html', bird=bird, notbird=notbird)



if __name__ == '__main__':
    app.run(
            host="0.0.0.0",
            port=int("5000"),
            debug=True
            )

