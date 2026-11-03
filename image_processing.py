

import math
import time

import cv2
import numpy as np

_MIN_SLEEP_SECONDS = 0.002

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


def count_squares(image_shape, square_size):
    height, width = image_shape[:2]
    return math.ceil(height / square_size) * math.ceil(width / square_size)

# It is function for averaging the color of a square block of pixels and setting all pixels in that block to the average color that needed in assignment
def average_square(block):
    
    mean_color = block.mean(axis=(0, 1))
    block[:] = (mean_color + 0.5).astype(np.uint8)


def split_into_regions(height, square_size, region_count):
    square_rows = math.ceil(height / square_size)
    region_count = max(1, min(region_count, square_rows))
    base, extra = divmod(square_rows, region_count)

    regions = []
    row = 0
    for index in range(region_count):
        rows_in_region = base + (1 if index < extra else 0)
        y_start = row * square_size
        y_end = min((row + rows_in_region) * square_size, height)
        regions.append((y_start, y_end))
        row += rows_in_region
    return regions

# It is function for pixelating a region of the image by dividing it into square blocks and averaging the color of each block, I have used double loop (more faster approach can be used)
def pixelate_region(image, y_start, y_end, square_size,
                    delay_per_square=0.0, on_progress=None):
    
    width = image.shape[1]
    pending_delay = 0.0

    for y in range(y_start, y_end, square_size):
        y_stop = min(y + square_size, y_end)
        for x in range(0, width, square_size):
            average_square(image[y:y_stop, x:x + square_size])

            if delay_per_square:
                pending_delay += delay_per_square
                if pending_delay >= _MIN_SLEEP_SECONDS:
                    time.sleep(pending_delay)
                    pending_delay = 0.0

            if on_progress is not None and not on_progress():
                return False
    return True
