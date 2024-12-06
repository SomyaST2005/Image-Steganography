import random

def spread_spectrum_encode(binary_message, length):
    random.seed(42)
    spread_sequence = [random.choice([0, 1]) for _ in range(length)]
    spread_message = ''.join(str(int(b) ^ s) for b, s in zip(binary_message, spread_sequence))
    return spread_message