

import time

from image_processing import pixelate_region

FRAME_INTERVAL = 1 / 30  # it is my frame interval for refreshing the window, which is 30 frames per second just estimated number



# this processes the whole image in the main thread, refreshing the window as it goes, it takes image and square size as needed in task
def run_single(image, square_size, window):
    
    last_refresh = 0.0

    def refresh_window():
        nonlocal last_refresh
        now = time.perf_counter()
        if now - last_refresh < FRAME_INTERVAL:
            return True
        last_refresh = now
        return window.show(image)

    return pixelate_region(image, 0, image.shape[0], square_size,
                           on_progress=refresh_window)
