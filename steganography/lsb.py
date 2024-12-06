from PIL import Image
import numpy as np

import numpy as np

def set_lsb(value, bit):
    value = np.uint8(value)
    if bit == 1:
        value = np.uint8(value | 1)
    else:
        value = np.uint8(value & 0xFE)
    return value


def lsb_encode(image_path, binary_message):
    image = Image.open(image_path)
    img_array = np.array(image)
    
    flat_image = img_array.flatten()
    for i, bit in enumerate(binary_message):
        flat_image[i] = set_lsb(flat_image[i], int(bit))
    
    img_array = flat_image.reshape(img_array.shape)
    encoded_image = Image.fromarray(img_array)
    encoded_image.save('encoded_image.png')
    return 'encoded_image.png'
