# utils.py
from .huffman import HuffmanCoding
from .lsb import lsb_encode, lsb_decode
from .spread_spectrum import spread_spectrum_encode, spread_spectrum_decode
import logging

logger = logging.getLogger(__name__)

def encode_message(image_path, message):
    """
    Complete encoding process: Huffman -> Spread Spectrum -> LSB
    Args:
        image_path: Path to input image
        message: Message to encode
    Returns:
        Tuple of (encoded image path, huffman instance, message_length)
    """
    try:
        # Step 1: Huffman encoding
        huffman = HuffmanCoding()
        binary_message = huffman.encode(message)
        logger.info("Huffman encoding completed")

        # Step 2: Spread spectrum encoding
        spread_message = spread_spectrum_encode(binary_message, len(binary_message))
        logger.info("Spread spectrum encoding completed")

        # Step 3: LSB encoding
        # Encode the length of the message first, then the actual message
        message_length = len(spread_message)
        encoded_image_path = lsb_encode(image_path, spread_message, message_length)
        logger.info("LSB encoding completed")

        return encoded_image_path, huffman

    except Exception as e:
        logger.error(f"Error in message encoding: {str(e)}")
        raise

def decode_message(image_path, huffman):
    """
    Complete decoding process: LSB -> Spread Spectrum -> Huffman
    Args:
        image_path: Path to encoded image
        huffman: HuffmanCoding instance used for encoding
    Returns:
        Decoded message
    """
    try:
        # Step 1: LSB decoding
        spread_message = lsb_decode(image_path)
        logger.info("LSB decoding completed")

        # Step 2: Spread spectrum decoding
        binary_message = spread_spectrum_decode(spread_message, len(spread_message))
        logger.info("Spread spectrum decoding completed")

        # Step 3: Huffman decoding
        message = huffman.decode(binary_message)
        logger.info("Huffman decoding completed")

        return message

    except Exception as e:
        logger.error(f"Error in message decoding: {str(e)}")
        raise