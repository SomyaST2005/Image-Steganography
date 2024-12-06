from .huffman import HuffmanCoding
from .lsb import lsb_encode
from .spread_spectrum import spread_spectrum_encode

def encode_message(image_path, message):
    huffman = HuffmanCoding()
    binary_message = huffman.encode(message)

    spread_message = spread_spectrum_encode(binary_message, len(binary_message))

    encoded_image_path = lsb_encode(image_path, spread_message)
    return encoded_image_path, huffman