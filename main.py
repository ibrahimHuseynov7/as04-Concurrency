import argparse
import sys
import time

from image_processing import count_squares, load_image, save_image
from display import ImageWindow
from runners import run_single, run_multi, worker_count
# It is output for saving the result image after processing it
RESULT_PATH = "result.jpg"
ANIMATION_SECONDS = 4.0


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number

# we defgined a function for parsing the command line arguments, which includes the image path, square size, and mode single-threaded or multi-core that we have in assignment.
def parse_args():
    parser = argparse.ArgumentParser(
        description="Pixelate an image by averaging the color of square blocks.")
    parser.add_argument("image", help="path to the input JPG image")
    parser.add_argument("square_size", type=positive_int,
                        help="side length of the averaging square, in pixels")
    parser.add_argument("mode", type=str.upper, choices=("S", "M"),
                        help="S = single-threaded, M = multi-core (parallel)")
    parser.add_argument("--fast", action="store_true",
                        help="disable the artificial slowdown used to visualize progress")
    return parser.parse_args()

# I have used exception to make sure that program will not crash if the image path is not correct or the image is not readable, and also I have used sys.stderr to print the error messages to the standard error stream, which is a good practice for error reporting

def main():
    args = parse_args()

    try:
        image = load_image(args.image)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    height, width = image.shape[:2]
    print(f"Loaded '{args.image}' ({width}x{height}), "
          f"square size {args.square_size}, mode {args.mode}")

    window = ImageWindow(f"Pixelator - mode {args.mode}", image.shape)
    window.show(image)

    delay = 0.0 if args.fast else ANIMATION_SECONDS / count_squares(image.shape, args.square_size)

    start = time.perf_counter()
    if args.mode == "S":
        completed = run_single(image, args.square_size, window, delay)
    else:
        completed = run_multi(image, args.square_size, window, delay, worker_count())
    elapsed = time.perf_counter() - start

    if not completed:
        print("Window closed before processing finished - result not saved.")
        window.close()
        return 1

    save_image(RESULT_PATH, image)
    print(f"Done in {elapsed:.2f} s. Result saved to '{RESULT_PATH}'.")
    print("Press CTRL-C to close the window")

    try:
        window.wait_for_close(image)
    except KeyboardInterrupt:
        pass
    window.close()
    return 0




if __name__ == "__main__":
    sys.exit(main())