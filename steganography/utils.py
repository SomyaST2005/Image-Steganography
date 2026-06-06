# utils.py
import json
import logging
from .huffman import HuffmanCoding
from .lsb import lsb_encode, lsb_decode
from .spread_spectrum import spread_spectrum_encode, spread_spectrum_decode

logger = logging.getLogger(__name__)


def encode_message(image_path, message):
    """Complete encoding process: Huffman -> Spread Spectrum -> LSB.

    Args:
        image_path: Path to input image.
        message: Message to encode.

    Returns:
        Path to the encoded image (Huffman dict is embedded in PNG metadata).
    """
    try:
        huffman = HuffmanCoding()
        binary_message = huffman.encode(message)
        logger.info("Huffman encoding completed")

        spread_message = spread_spectrum_encode(binary_message, len(binary_message))
        logger.info("Spread spectrum encoding completed")

        message_length = len(spread_message)
        encoded_image_path = lsb_encode(
            image_path, spread_message, message_length, huffman.huffman_dict
        )
        logger.info("LSB encoding completed")

        return encoded_image_path

    except Exception as e:
        logger.error(f"Error in message encoding: {str(e)}")
        raise


def decode_message(image_path):
    """Complete decoding process: LSB -> Spread Spectrum -> Huffman.

    The Huffman dictionary is extracted from the image's PNG metadata,
    so no prior session or encoding context is needed.

    Args:
        image_path: Path to encoded image.

    Returns:
        Decoded message string.
    """
    try:
        spread_message, huffman_dict_json = lsb_decode(image_path)
        logger.info("LSB decoding completed")

        if not huffman_dict_json:
            raise ValueError(
                "No encoding data found in this image. "
                "Was it encoded with this tool?"
            )

        binary_message = spread_spectrum_decode(spread_message, len(spread_message))
        logger.info("Spread spectrum decoding completed")

        huffman = HuffmanCoding()
        huffman.huffman_dict = json.loads(huffman_dict_json)
        message = huffman.decode(binary_message)
        logger.info("Huffman decoding completed")

        return message

    except Exception as e:
        logger.error(f"Error in message decoding: {str(e)}")
        raise
