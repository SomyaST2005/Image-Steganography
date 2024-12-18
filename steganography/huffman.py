# huffman.py
import heapq
from collections import defaultdict, Counter
import logging

class HuffmanCoding:
    def __init__(self):
        self.huffman_dict = {}
        self.logger = logging.getLogger(__name__)

    def build_tree(self, message):
        """
        Build Huffman tree and generate encoding dictionary
        Args:
            message: Input message to encode
        """
        try:
            # Calculate frequency of each character
            frequency = Counter(message)
            
            if len(frequency) == 0:
                raise ValueError("Empty message provided")

            # Create heap with initial nodes
            heap = [[weight, [char, ""]] for char, weight in frequency.items()]
            heapq.heapify(heap)

            # Build Huffman tree
            while len(heap) > 1:
                lo = heapq.heappop(heap)
                hi = heapq.heappop(heap)

                # Add '0' to all codes in lo tree
                for pair in lo[1:]:
                    pair[1] = '0' + pair[1]
                
                # Add '1' to all codes in hi tree
                for pair in hi[1:]:
                    pair[1] = '1' + pair[1]

                # Combine trees and push back to heap
                heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

            # Generate final encoding dictionary
            self.huffman_dict = {a[0]: a[1] for a in heapq.heappop(heap)[1:]}
            self.logger.info("Huffman tree built successfully")
            
        except Exception as e:
            self.logger.error(f"Error building Huffman tree: {str(e)}")
            raise

    def encode(self, message):
        """
        Encode message using Huffman coding
        Args:
            message: Message to encode
        Returns:
            Encoded binary string
        """
        try:
            if not message:
                raise ValueError("Empty message provided")

            if not self.huffman_dict:
                self.build_tree(message)

            encoded = ''.join(self.huffman_dict[char] for char in message)
            self.logger.info(f"Message encoded successfully, length: {len(encoded)} bits")
            return encoded

        except Exception as e:
            self.logger.error(f"Error encoding message: {str(e)}")
            raise

    def decode(self, encoded_message):
        """
        Decode Huffman-encoded message
        Args:
            encoded_message: Binary string to decode
        Returns:
            Decoded message
        """
        try:
            if not encoded_message:
                raise ValueError("Empty encoded message provided")

            if not self.huffman_dict:
                raise ValueError("Huffman dictionary not initialized")

            reverse_dict = {v: k for k, v in self.huffman_dict.items()}
            decoded_message = ''
            temp_code = ''

            for bit in encoded_message:
                temp_code += bit
                if temp_code in reverse_dict:
                    decoded_message += reverse_dict[temp_code]
                    temp_code = ''

            if temp_code:  # Check for invalid encoding
                raise ValueError("Invalid encoded message")

            self.logger.info("Message decoded successfully")
            return decoded_message

        except Exception as e:
            self.logger.error(f"Error decoding message: {str(e)}")
            raise