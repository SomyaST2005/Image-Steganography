![image](https://github.com/user-attachments/assets/4cf3fe04-b912-490a-81d0-37101d1c5780)# Image Steganography System

## Introduction
The Image Steganography System is a secure and efficient application designed to embed secret messages into digital images. This project employs three key techniques:
1. **Huffman Encoding** for compressing the message.
2. **Spread Spectrum Encoding** for enhanced security.
3. **Least Significant Bit (LSB) Encoding** for embedding data into the image.

The system ensures minimal distortion of the cover image and is resistant to detection. It provides a scalable framework for covert communication with applications in secure messaging, digital watermarking, and intellectual property protection.

![Steganography Web App - Google Chrome 05-02-2025 11_28_32](https://github.com/user-attachments/assets/0b6a2638-6ad9-4fc7-9250-80adbdbacdbf)

---

## Project Structure
```
project-root/
|
|-- app.py                   # Main application script.
|-- requirements.txt         # Python dependencies.
|-- README.md                # Project documentation.
|
|-- steganography/           # Core logic for steganographic techniques.
|   |-- __init__.py
|   |-- huffman.py           # Huffman Encoding and Decoding.
|   |-- spread_spectrum.py   # Spread Spectrum Encoding and Decoding.
|   |-- lsb.py               # LSB Encoding and Decoding.
|   |-- utils.py             # Utility functions.
|
|-- templates/               # HTML templates for the web application.
|   |-- index.html
|
|-- static/                  # Frontend assets.
|   |-- scripts.js
|   |-- styles.css
|
|-- encoded/                 # Directory for encoded images.
|   |-- encoded_image.png
|
|-- app.log                  # Log file for debugging.
```

---

## Features
1. **Message Compression**: Efficiently compresses plaintext messages using Huffman Encoding.
2. **Enhanced Security**: Introduces randomness via Spread Spectrum Encoding to protect against detection.
3. **Image Quality Preservation**: Uses LSB Encoding to minimize visible distortion in the cover image.
4. **Web Interface**: Simple web application for uploading images and embedding/retrieving messages.
5. **Evaluation Metrics**: Includes metrics like Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR) to assess performance.

---

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Backend framework for the web application.
- **OpenCV**: Image processing library.
- **NumPy**: Numerical computation library.
- **HTML/CSS/JavaScript**: Frontend for the web application.

---

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project-root
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open a web browser and navigate to `http://127.0.0.1:5000`.

---

## How to Use
1. **Encoding a Message**:
   - Upload a cover image.
   - Enter the message to be embedded.
   - Click the "Encode" button.
   - Download the encoded image.

2. **Decoding a Message**:
   - Upload the encoded image.
   - Click the "Decode" button.
   - View the extracted message.

---

## Evaluation Metrics
1. **Mean Squared Error (MSE)**:
   - Measures the average squared difference between the original and encoded images.

2. **Peak Signal-to-Noise Ratio (PSNR)**:
   - Evaluates the quality of the encoded image compared to the original image.
These metrics ensure that the system maintains high image quality while embedding data.





```@2024 DEVELOPED BY SOMYA SHEKHAR TIWARI```

