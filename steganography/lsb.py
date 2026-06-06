# lsb.py
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import numpy as np
import logging
import os
import json
import tempfile

logger = logging.getLogger(__name__)

MAX_MESSAGE_BITS = 8_000_000  # ~1MB of text as safety upper bound


def set_lsb(value, bit):
    """Set the least significant bit of a pixel value."""
    value = np.uint8(value)
    return np.uint8(value | 1) if bit == 1 else np.uint8(value & 0xFE)


def lsb_encode(image_path, binary_message, message_length, huffman_dict=None):
    """Encode binary message into image using LSB steganography.

    Args:
        image_path: Path to the cover image.
        binary_message: Binary string to embed.
        message_length: Length of the binary message (stored in first 32 pixels).
        huffman_dict: Optional dict to embed as PNG metadata for self-contained decoding.

    Returns:
        Path to the encoded PNG image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError("Input image not found")
    if not binary_message:
        raise ValueError("Empty binary message provided")

    image = Image.open(image_path)
    img_array = np.array(image)

    if len(binary_message) > img_array.size:
        raise ValueError("Message too large for this image")

    flat_image = img_array.flatten()
    length_bits = format(message_length, '032b')

    for i, bit in enumerate(length_bits):
        flat_image[i] = set_lsb(flat_image[i], int(bit))

    for i, bit in enumerate(binary_message):
        flat_image[i + 32] = set_lsb(flat_image[i + 32], int(bit))

    img_array = flat_image.reshape(img_array.shape)
    encoded_image = Image.fromarray(img_array)

    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir=tempfile.gettempdir())
    output_path = tmp.name
    tmp.close()

    if huffman_dict:
        metadata = PngInfo()
        metadata.add_text("huffman_dict", json.dumps(huffman_dict))
        encoded_image.save(output_path, 'PNG', pnginfo=metadata)
    else:
        encoded_image.save(output_path, 'PNG')

    logger.info(f"Message encoded successfully in image: {output_path}")
    return output_path


def lsb_decode(image_path):
    """Decode message from LSB-encoded image.

    Returns:
        Tuple of (binary_message, huffman_dict_json).
        huffman_dict_json is None if not embedded in the image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError("Encoded image not found")

    image = Image.open(image_path)
    img_array = np.array(image)
    flat_image = img_array.flatten()
    total_pixels = len(flat_image)

    length_bits = ''.join(str(flat_image[i] & 1) for i in range(32))
    message_length = int(length_bits, 2)

    if message_length <= 0:
        raise ValueError("Invalid encoded image: message length is zero")
    if message_length > total_pixels - 32:
        raise ValueError("Invalid encoded image: message length exceeds image capacity")
    if message_length > MAX_MESSAGE_BITS:
        raise ValueError("Invalid encoded image: message length unreasonably large")

    binary_message = ''.join(str(flat_image[i] & 1) for i in range(32, 32 + message_length))
    huffman_dict_json = image.info.get("huffman_dict")

    logger.info("Message extracted successfully from image")
    return binary_message, huffman_dict_json
