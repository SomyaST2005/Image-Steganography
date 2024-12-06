# app.py

from flask import Flask, request, render_template, send_file, jsonify
from steganography.huffman import *
from steganography.utils import encode_message
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return jsonify({"error": "No image or message provided"}), 400

    image = request.files['image']
    message = request.form['message']
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    encoded_image_path, huffman = encode_message(image_path, message)

    return send_file(encoded_image_path, as_attachment=True, download_name='encoded_image.png')

if __name__ == '__main__':
    app.run(debug=True)
