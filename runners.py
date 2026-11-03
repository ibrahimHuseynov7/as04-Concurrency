

import os
import time
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory

import numpy as np

from image_processing import pixelate_region, split_into_regions

FRAME_INTERVAL = 1 / 30  # it is my frame interval for refreshing the window, which is 30 frames per second just estimated number
# it is function for getting the number of CPU cores available on the system, which is used to determine how many worker processes to create for multi-core processing
def worker_count():
   
    return os.cpu_count() or 1

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


def _worker(shm_name, shape, y_start, y_end, square_size):
    
    shm = SharedMemory(name=shm_name)
    try:
        image = np.ndarray(shape, dtype=np.uint8, buffer=shm.buf)
        pixelate_region(image, y_start, y_end, square_size)
        del image  # release the buffer before closing the shared memory
    finally:
        shm.close()
# this function is for processing the image in parallel using multiple worker processes, it divides the image into horizontal bands and assigns each band to a separate worker process, it uses shared memory to allow all processes to access and modify the same image data, it also refreshes the window as the workers process their assigned regions, and handles user input to close the window if needed
def run_multi(image, square_size, window, workers):
    
    shm = SharedMemory(create=True, size=image.nbytes)
    try:
        shared = np.ndarray(image.shape, dtype=np.uint8, buffer=shm.buf)
        shared[:] = image

        regions = split_into_regions(image.shape[0], square_size, workers)
        processes = [
            Process(target=_worker,
                    args=(shm.name, image.shape, y_start, y_end, square_size),
                    daemon=True)
            for y_start, y_end in regions
        ]
        print(f"Starting {len(processes)} worker process(es) "
              f"on {worker_count()} CPU core(s)")
        for process in processes:
            process.start()

        completed = True
        while any(process.is_alive() for process in processes):
            if not window.show(shared):
                completed = False
                for process in processes:
                    process.terminate()
                break
            time.sleep(FRAME_INTERVAL)

        for process in processes:
            process.join()

        if completed:
            failed = [p for p in processes if p.exitcode != 0]
            if failed:
                raise RuntimeError(f"{len(failed)} worker process(es) failed")
            image[:] = shared
        del shared
    finally:
        shm.close()
        shm.unlink()
    return completed