from PIL import Image
import numpy as np
import os
import tempfile
from steganography.utils import encode_message

def calculate_mse(original_path, encoded_path):
    original = np.array(Image.open(original_path).convert("RGB"), dtype=np.float64)
    encoded = np.array(Image.open(encoded_path).convert("RGB"), dtype=np.float64)
    return np.mean((original - encoded) ** 2)

def calculate_psnr(mse):
    if mse == 0:
        return float("inf")
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))

def create_test_image(size, path):
    # Deterministic random image so results are repeatable
    np.random.seed(size[0] * size[1])
    image_array = np.random.randint(0, 256, (size[1], size[0], 3), dtype=np.uint8)
    image = Image.fromarray(image_array)
    image.save(path)

def main():
    image_sizes = [(100, 100), (250, 250), (500, 500)]

    long_message = (
    "Open source contribution helps beginners learn real-world development, "
    "Git, GitHub, documentation, testing, and collaboration through practical "
    "project work. This benchmark message is used to evaluate image quality "
    "after hiding text inside a PNG image using steganography techniques. "
)

    long_message = (long_message * 3)[:500]

    messages = {
        "2 chars": "Hi",
        "17 chars": "Open Source Rocks",
        "43 chars": "This is a benchmark message for testing.",
        "500 chars": long_message
    }

    results = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for size in image_sizes:
            original_path = os.path.join(temp_dir, f"original_{size[0]}x{size[1]}.png")
            create_test_image(size, original_path)

            for label, message in messages.items():
                encoded_path = encode_message(original_path, message)
                mse = calculate_mse(original_path, encoded_path)
                psnr = calculate_psnr(mse)

                results.append([
                    f"{size[0]} × {size[1]}",
                    label,
                    round(mse, 6),
                    round(psnr, 2)
                ])

    print("| Image Size | Message Length | MSE | PSNR (dB) |")
    print("|---|---:|---:|---:|")

    for row in results:
        print(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")

    avg_psnr = sum(row[3] for row in results) / len(results)
    worst_psnr = min(row[3] for row in results)

    print("\nAverage PSNR:", round(avg_psnr, 2), "dB")
    print("Worst PSNR:", round(worst_psnr, 2), "dB")

if __name__ == "__main__":
    main()