

import cv2
import numpy as np

# It is function for taking image from the path and returning it as a numpy array for easier processing
def load_image(path):
    
    data = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"'{path}' is not a readable image file")
    return image

# It is function for saving image to the path after processing it
def save_image(path, image):
    
    ok, encoded = cv2.imencode(".jpg", image)
    if not ok:
        raise OSError(f"Could not encode image for '{path}'")
    encoded.tofile(path)

# It is function for averaging the color of a square block of pixels and setting all pixels in that block to the average color that needed in assignment
def average_square(block):
    
    mean_color = block.mean(axis=(0, 1))
    block[:] = (mean_color + 0.5).astype(np.uint8)

# It is function for pixelating a region of the image by dividing it into square blocks and averaging the color of each block, I have used double loop (more faster approach can be used)
def pixelate_region(image, y_start, y_end, square_size):
    
    width = image.shape[1]

    for y in range(y_start, y_end, square_size):
        y_stop = min(y + square_size, y_end)
        for x in range(0, width, square_size):
            average_square(image[y:y_stop, x:x + square_size])
