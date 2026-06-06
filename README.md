# StegShield — Image Steganography System

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/flask-3.x-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Deployed](https://img.shields.io/badge/deployed-Render-46e3b7)

> **Live Demo:** [image-steganography-9ryi.onrender.com](https://image-steganography-9ryi.onrender.com)

---

## Introduction

StegShield is a web-based image steganography tool that hides secret messages inside PNG images. It uses a **three-layer encoding pipeline** that makes the embedded data both compressed and visually undetectable:

| Layer | Technique | Purpose |
|-------|-----------|---------|
| 1 | **Huffman Encoding** | Compresses the message using variable-length codes — frequent characters get shorter codes, reducing the binary footprint |
| 2 | **Spread Spectrum** | XORs the bitstream with a pseudo-random sequence, spreading the signal to avoid detectable patterns |
| 3 | **LSB Embedding** | Hides the final bitstream in the least significant bits of image pixels — invisible to the human eye |

The encoded image is **self-contained** — the Huffman dictionary is embedded in the PNG metadata, so decoding works on any device, in any browser, without needing the original encoding session.

---

## Project Structure

```
project-root/
|
|-- app.py                   # Flask application entry point
|-- Procfile                 # Render/Heroku deployment config
|-- requirements.txt         # Python dependencies
|-- .env.example             # Environment variable template
|-- README.md
|
|-- steganography/           # Core encoding/decoding logic
|   |-- __init__.py
|   |-- huffman.py           # Huffman Encoding & Decoding
|   |-- spread_spectrum.py   # Spread Spectrum XOR obfuscation
|   |-- lsb.py               # LSB pixel embedding & extraction
|   |-- utils.py             # Orchestrator: chains all 3 layers
|
|-- templates/
|   |-- index.html           # Single-page UI (dark theme, glassmorphism)
|
|-- static/
|   |-- styles.css           # Design system (CSS variables, responsive)
|   |-- scripts.js           # Client-side validation & async fetch
```

---

## Features

- **Three-layer encoding** — Huffman compression → Spread spectrum obfuscation → LSB embedding
- **Self-contained encoded images** — Huffman dictionary stored in PNG metadata; decode anywhere, anytime
- **Professional dark-themed UI** — Glassmorphism card design, drag-and-drop, toast notifications, light/dark mode toggle
- **Real-time capacity indicator** — Shows how many characters your image can hold
- **Client-side validation** — File type, file size, and message length checked before uploading
- **Accessible** — Full ARIA support, keyboard navigation, reduced-motion support
- **Responsive** — Works on mobile, tablet, and desktop

---

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Core language |
| **Flask** | Web framework & REST API |
| **Pillow (PIL)** | Image loading, pixel manipulation, PNG metadata |
| **NumPy** | Fast array operations for pixel bit manipulation |
| **Gunicorn** | Production WSGI server |
| **Vanilla HTML/CSS/JS** | Frontend — no frameworks, zero dependencies |

---

## Setup Instructions

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/SomyaST2005/Image-Steganography.git
cd Image-Steganography

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env

# 5. Run the application
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### Deploy to Render

1. Push the repo to GitHub
2. Connect the repo on [Render](https://render.com)
3. Set the environment variable `SECRET_KEY` to a random string
4. Render auto-detects the `Procfile` and deploys

---

## How to Use

### Encoding a Message

1. Open the **Encode** tab
2. Drop an image (PNG or JPEG) into the upload zone, or click to browse
3. Type your secret message (max 1000 characters)
4. Watch the capacity bar to see how much space you're using
5. Click **Encode Message**
6. Download the encoded PNG — it looks identical to the original

### Decoding a Message

1. Switch to the **Decode** tab
2. Upload the previously encoded PNG image
3. Click **Decode Message**
4. Your original message appears — copy it with one click

---

## Pipeline Architecture

```
  ┌──────────┐     ┌────────────────┐     ┌───────────────────┐     ┌──────────────┐
  │ Message  │────▶│ Huffman        │────▶│ Spread Spectrum   │────▶│ LSB          │
  │ (text)   │     │ Compression    │     │ XOR Obfuscation   │     │ Embedding    │
  └──────────┘     └────────────────┘     └───────────────────┘     └──────┬───────┘
                                                                          │
                                                                    ┌─────▼───────┐
                                                                    │ Encoded PNG │
                                                                    │ (self-cont- │
                                                                    │ ained)      │
                                                                    └─────────────┘

  ┌──────────────┐     ┌───────────────┐     ┌────────────────━═══┐     ┌──────────┐
  │ Encoded PNG  │────▶│ LSB           │────▶│ Spread Spectrum    │────▶│ Huffman  │
  │              │     │ Extraction    │     │ De-XOR             │     │ Decode   │
  └──────────────┘     └───────────────┘     └────────────────━━━━┘     └────┬─────┘
                                                                            │
                                                                     ┌──────▼──────┐
                                                                     │ Original    │
                                                                     │ Message     │
                                                                     └─────────────┘
```

---

## Evaluation Metrics

To measure image quality after embedding, we compare the original cover image with the encoded image pixel by pixel using two standard metrics:

### Mean Squared Error (MSE)
Measures the average squared difference between original and encoded pixel values. Lower = better.
```
MSE = (1/N) × Σ (original - encoded)²
```

### Peak Signal-to-Noise Ratio (PSNR)
Expresses the ratio between the maximum possible signal power and the noise introduced. Higher = better. A PSNR above **40 dB** is considered visually lossless.
```
PSNR = 10 × log₁₀(255² / MSE)
```

### Real Benchmark Results

Tests performed on randomly generated RGB images at various sizes and message lengths:

| Image Size | Message | Chars | MSE | PSNR |
|-----------|---------|-------|-----|------|
| 100×100 | "Hi" | 2 | 0.000567 | 80.60 dB |
| 100×100 | "This is a secret" | 17 | 0.001433 | 76.57 dB |
| 100×100 | Full sentence | 43 | 0.003900 | 72.22 dB |
| 100×100 | Long message | 500 | 0.033900 | 62.83 dB |
| 250×250 | "Hi" | 2 | 0.000107 | 87.85 dB |
| 250×250 | "This is a secret" | 17 | 0.000272 | 83.79 dB |
| 250×250 | Full sentence | 43 | 0.000656 | 79.96 dB |
| 250×250 | Long message | 500 | 0.005531 | 70.70 dB |
| 500×500 | "Hi" | 2 | 0.000015 | 96.47 dB |
| 500×500 | "This is a secret" | 17 | 0.000053 | 90.86 dB |
| 500×500 | Full sentence | 43 | 0.000152 | 86.31 dB |
| 500×500 | Long message | 500 | 0.001369 | 76.77 dB |

### Summary

| Metric | Range | Average |
|--------|-------|---------|
| MSE | 0.000015 — 0.033900 | 0.003996 |
| PSNR | 62.83 — 96.47 dB | **80.41 dB** |

**Key observations:**

- **All PSNR values far exceed the 40 dB threshold** for visual losslessness — the human eye cannot detect any difference between original and encoded images
- Larger images produce dramatically better quality (500×500 PSNR is ~16 dB higher than 100×100 for the same message)
- Even at maximum capacity (500 chars on a 100×100 image), PSNR stays above 60 dB — well into the "excellent" quality range

---

## Security Considerations

- The **spread spectrum layer** uses a fixed seed for XOR obfuscation — this provides obfuscation, not cryptographic encryption. For truly secure communication, encrypt your message before encoding.
- Encoded images are standard PNG files — they upload to social media, email, and messaging platforms without triggering any filters.
- The Huffman dictionary is stored as PNG metadata (`tEXt` chunk) — invisible to image viewers but required for decoding.

---

## License

MIT — free to use, modify, and distribute.

---

**Developed by Somya Shekhar Tiwari • 2024**
