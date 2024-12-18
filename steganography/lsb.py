# lsb.py
from PIL import Image
import numpy as np
import logging
import os

logger = logging.getLogger(__name__)

def set_lsb(value, bit):
    """Set the least significant bit of a pixel value"""
    try:
        value = np.uint8(value)
        return np.uint8(value | 1) if bit == 1 else np.uint8(value & 0xFE)
    except Exception as e:
        logger.error(f"Error setting LSB: {str(e)}")
        raise

def lsb_encode(image_path, binary_message, message_length):
    """Encode binary message into image using LSB steganography"""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError("Input image not found")

        if not binary_message:
            raise ValueError("Empty binary message provided")

        # Open and convert image
        image = Image.open(image_path)
        img_array = np.array(image)
        
        # Check if image has enough capacity
        if len(binary_message) > img_array.size:
            raise ValueError("Message too large for this image")

        # Flatten image and encode message length first
        flat_image = img_array.flatten()
        length_bits = format(message_length, '032b')  # 32 bits for length
        
        # Encode length
        for i, bit in enumerate(length_bits):
            flat_image[i] = set_lsb(flat_image[i], int(bit))
        
        # Encode message
        for i, bit in enumerate(binary_message):
            flat_image[i + 32] = set_lsb(flat_image[i + 32], int(bit))

        # Reshape and save
        img_array = flat_image.reshape(img_array.shape)
        encoded_image = Image.fromarray(img_array)
        output_path = 'encoded_image.png'
        encoded_image.save(output_path, 'PNG')

        logger.info(f"Message encoded successfully in image: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Error in LSB encoding: {str(e)}")
        raise

def lsb_decode(image_path):
    """Decode message from LSB-encoded image"""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError("Encoded image not found")

        # Open and process image
        image = Image.open(image_path)
        img_array = np.array(image)
        flat_image = img_array.flatten()

        # Extract length first (first 32 bits)
        length_bits = ''.join(str(flat_image[i] & 1) for i in range(32))
        message_length = int(length_bits, 2)

        # Extract message using the length we found
        binary_message = ''.join(str(flat_image[i] & 1) for i in range(32, 32 + message_length))

        logger.info("Message extracted successfully from image")
        return binary_message

    except Exception as e:
        logger.error(f"Error in LSB decoding: {str(e)}")
        raise