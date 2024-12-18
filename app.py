# app.py
from flask import Flask, request, render_template, send_file, jsonify, session
from steganography.huffman import HuffmanCoding
from steganography.utils import encode_message, decode_message
from werkzeug.utils import secure_filename
import os
import shutil
import logging
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
MAX_MESSAGE_LENGTH = 1000  # Maximum message length

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def init_app():
    """Initialize application requirements"""
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        raise

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_old_files():
    """Clean up old files from upload folder"""
    try:
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)
        logger.info("Old files cleaned successfully")
    except Exception as e:
        logger.error(f"Error cleaning old files: {str(e)}")
        raise

def save_uploaded_file(file):
    """Save uploaded file with timestamp"""
    try:
        if not file:
            raise ValueError("No file provided")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"File saved successfully: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise

@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    """Handle encoding requests"""
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        if 'message' not in request.form:
            return jsonify({"error": "No message provided"}), 400

        image = request.files['image']
        message = request.form['message']

        # Validate inputs
        if image.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400
        if len(message) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"}), 400

        # Process image and encode message
        image_path = save_uploaded_file(image)
        encoded_image_path, huffman = encode_message(image_path, message)

        # Store encoding data in session
        session['huffman_dict'] = huffman.huffman_dict
        session['message_length'] = len(message)

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
        clean_old_files()

@app.route('/decode', methods=['POST'])
def decode():
    """Handle decoding requests"""
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        if 'huffman_dict' not in session:
            return jsonify({"error": "No encoding data found. Please encode a message first"}), 400

        image = request.files['image']

        # Validate inputs
        if image.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400

        # Process image and decode message
        image_path = save_uploaded_file(image)
        
        # Recreate Huffman coding instance
        huffman = HuffmanCoding()
        huffman.huffman_dict = session['huffman_dict']

        # Decode message
        decoded_message = decode_message(image_path, huffman)
        
        logger.info("Message decoded successfully")
        return jsonify({
            "message": decoded_message,
            "success": True
        })

    except Exception as e:
        logger.error(f"Decoding error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        clean_old_files()

# Error handlers
@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({"error": "File is too large"}), 413

@app.errorhandler(400)
def bad_request(e):
    """Handle bad request error"""
    return jsonify({"error": str(e)}), 400

@app.errorhandler(500)
def server_error(e):
    """Handle internal server error"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle not found error"""
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    init_app()
    app.run(debug=True)