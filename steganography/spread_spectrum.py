# spread_spectrum.py
import random
import numpy as np
import logging

logger = logging.getLogger(__name__)

def spread_spectrum_encode(binary_message, length):
    """
    Encode binary message using spread spectrum technique
    Args:
        binary_message: Binary string to encode
        length: Length of spreading sequence
    Returns:
        Spread spectrum encoded message
    """
    try:
        if not binary_message:
            raise ValueError("Empty binary message provided")

        # Use numpy for better performance
        random.seed(42)  # Fixed seed for reproducibility
        spread_sequence = np.array([random.choice([0, 1]) for _ in range(length)])
        message_bits = np.array([int(b) for b in binary_message])
        
        # XOR operation using numpy
        spread_message = np.logical_xor(message_bits, spread_sequence)
        result = ''.join(str(int(bit)) for bit in spread_message)
        
        logger.info(f"Message spread successfully, length: {len(result)} bits")
        return result

    except Exception as e:
        logger.error(f"Error in spread spectrum encoding: {str(e)}")
        raise

def spread_spectrum_decode(spread_message, length):
    """
    Decode spread spectrum message
    Args:
        spread_message: Spread spectrum encoded message
        length: Length of spreading sequence
    Returns:
        Decoded binary message
    """
    try:
        if not spread_message:
            raise ValueError("Empty spread message provided")

        # Use numpy for better performance
        random.seed(42)  # Same seed as encoding
        spread_sequence = np.array([random.choice([0, 1]) for _ in range(length)])
        spread_bits = np.array([int(b) for b in spread_message])
        
        # XOR operation using numpy
        decoded_bits = np.logical_xor(spread_bits, spread_sequence)
        result = ''.join(str(int(bit)) for bit in decoded_bits)
        
        logger.info("Message de-spread successfully")
        return result

    except Exception as e:
        logger.error(f"Error in spread spectrum decoding: {str(e)}")
        raise