# app.py
from flask import Flask, request, render_template, send_file, jsonify
from steganography.utils import encode_message, decode_message
from werkzeug.utils import secure_filename
import os
import shutil
import uuid
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
MAX_MESSAGE_LENGTH = 1000

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def init_app():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logger.info("Application initialized successfully")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """Save uploaded file in a unique per-request directory."""
    request_dir = os.path.join(UPLOAD_FOLDER, uuid.uuid4().hex)
    os.makedirs(request_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(request_dir, filename)
    file.save(filepath)
    logger.info(f"File saved: {filepath}")
    return filepath


def cleanup_path(path):
    """Remove a file and its parent directory if inside UPLOAD_FOLDER."""
    try:
        if not path or not os.path.exists(path):
            return
        parent = os.path.dirname(path)
        if os.path.abspath(parent).startswith(os.path.abspath(UPLOAD_FOLDER)):
            shutil.rmtree(parent, ignore_errors=True)
        else:
            os.unlink(path)
    except OSError:
        pass


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encode', methods=['POST'])
def encode():
    image_path = None
    encoded_image_path = None
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        if 'message' not in request.form:
            return jsonify({"error": "No message provided"}), 400

        image = request.files['image']
        message = request.form['message']

        if image.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400
        if len(message) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"}), 400

        image_path = save_uploaded_file(image)
        encoded_image_path = encode_message(image_path, message)

        logger.info("Message encoded successfully")
        return send_file(
            encoded_image_path,
            as_attachment=True,
            download_name='encoded_image.png',
            mimetype='image/png'
        )

    except Exception as e:
        logger.error(f"Encoding error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        cleanup_path(image_path)
        cleanup_path(encoded_image_path)


@app.route('/decode', methods=['POST'])
def decode():
    image_path = None
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image = request.files['image']

        if image.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        image_path = save_uploaded_file(image)
        decoded_message = decode_message(image_path)

        logger.info("Message decoded successfully")
        return jsonify({"message": decoded_message, "success": True})

    except Exception as e:
        logger.error(f"Decoding error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        cleanup_path(image_path)


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File is too large"}), 413


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == '__main__':
    init_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
