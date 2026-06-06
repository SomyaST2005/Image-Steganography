# Image Steganography System

![Steganography Web App - Google Chrome 05-02-2025 11_28_32](https://github.com/user-attachments/assets/0b6a2638-6ad9-4fc7-9250-80adbdbacdbf)

## Introduction
The Image Steganography System is a secure and efficient application designed to embed secret messages into digital images. This project employs three key techniques:
1. **Huffman Encoding** for compressing the message.
2. **Spread Spectrum Encoding** for enhanced security.
3. **Least Significant Bit (LSB) Encoding** for embedding data into the image.

The system ensures minimal distortion of the cover image and is resistant to detection. It provides a scalable framework for covert communication with applications in secure messaging, digital watermarking, and intellectual property protection.

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

The system evaluates the quality of the encoded image by comparing the original cover image with the steganographic output image. The goal is to confirm that the hidden message is embedded while keeping visual distortion as low as possible.

### Mean Squared Error (MSE)

Mean Squared Error measures the average squared difference between pixel values of the original image and the encoded image.

A lower MSE value means the encoded image is more similar to the original image.

### Peak Signal-to-Noise Ratio (PSNR)

Peak Signal-to-Noise Ratio measures the quality of the encoded image compared to the original image.

A higher PSNR value means better image quality and lower visible distortion.

### Benchmark Methodology

The benchmark can be performed by encoding messages of different lengths into cover images of different sizes and then comparing the original and encoded images using MSE and PSNR.

Example test setup:

| Image Size | Message Length |
| ---------- | -------------- |
| 100 × 100  | Short message  |
| 250 × 250  | Medium message |
| 500 × 500  | Long message   |


## Encoding Pipeline

```text
Plain Text Message
        |
        v
Huffman Encoding
        |
        v
Spread Spectrum Encoding
        |
        v
LSB Embedding
        |
        v
Encoded Steganographic Image

### Benchmark Results

| Image Size | Message Length | MSE | PSNR (dB) |
| ---------- | -------------: | --: | --------: |
| 100 × 100  |        2 chars | 0.0006 | 80.35 |
| 100 × 100  |       17 chars | 0.001633 | 76.00 |
| 100 × 100  |       43 chars | 0.003367 | 72.86 |
| 100 × 100  |      500 chars | 0.0392 | 62.20 |
| 250 × 250  |        2 chars | 0.000112 | 87.64 |
| 250 × 250  |       17 chars | 0.000256 | 84.05 |
| 250 × 250  |       43 chars | 0.000587 | 80.45 |
| 250 × 250  |      500 chars | 0.005931 | 70.40 |
| 500 × 500  |        2 chars | 0.000017 | 95.74 |
| 500 × 500  |       17 chars | 0.000059 | 90.45 |
| 500 × 500  |       43 chars | 0.000125 | 87.15 |
| 500 × 500  |      500 chars | 0.001451 | 76.52 |

**Average PSNR:** 80.32 dB  
**Worst-case PSNR:** 62.20 dB

### Key Observation

The benchmark results show that the system preserves image quality effectively across different image sizes and message lengths. As expected, larger messages introduce more distortion, which increases MSE and lowers PSNR. However, even in the worst-case scenario, the PSNR remains above 62 dB, indicating that the visual quality of the encoded image is still very high. The average PSNR of 80.32 dB demonstrates that the steganographic process introduces minimal visible distortion overall.



```@2024 DEVELOPED BY SOMYA SHEKHAR TIWARI```

