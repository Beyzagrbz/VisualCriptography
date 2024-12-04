import numpy as np
from PIL import Image

def floyd_steinberg_dithering(image):
    """Floyd-Steinberg dithering algoritması ile görüntüyü siyah-beyaz hale getirir"""
    img = np.array(image, dtype=float)
    h, w = img.shape

    for y in range(h-1):
        for x in range(1, w-1):
            old_pixel = img[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            img[y, x] = new_pixel
            
            error = old_pixel - new_pixel
            
            img[y, x+1] += error * 7/16
            img[y+1, x-1] += error * 3/16
            img[y+1, x] += error * 5/16
            img[y+1, x+1] += error * 1/16

    return Image.fromarray(np.uint8(img))