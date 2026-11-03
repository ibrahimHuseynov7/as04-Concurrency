## Image Pixelation

Divides an image into `square_size × square_size` blocks and fills every block
with its average color. Progress is drawn on screen while the work happens,
and the final image is saved as `result.jpg`.

Two processing modes:

- **S (single-threaded)** — one thread processes the squares left-to-right, top-to-bottom.
- **M (multi-core)** — the image is split into horizontal bands, one per CPU core,
  and every band is processed in parallel (each band still left-to-right, top-to-bottom).

## Requirements

- Python 3.9 or newer
- Windows, macOS or Linux

## Installation

**macOS / Linux**
Create virtual environment if you have version conflicts


```bash
python3 -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py <photo.jpg> <square_size> <S|M> [--fast]
Please wait around 5-6 seconds for the first run, as the libraries are compiled and cached.
```

| Argument      | Meaning                                                   |
|---------------|-----------------------------------------------------------|
| `photo.jpg`   | Path to the input JPG image (any size)                    |
| `square_size` | Side of the averaging square in pixels (positive integer) |
| `S` / `M`     | `S` = single-threaded, `M` = multi-core                   |
| `--fast`      | Optional: disable the slowdown used to visualize progress |

Examples:

```bash
python main.py photo.jpg 20 S
python main.py photo.jpg 5 M
```

(On macOS use `python3` if `python` is not found and the virtual environment is not active.)

While running: press **Esc** or **q**, or close the window, to abort.
After finishing: the result stays on screen and is saved to `result.jpg`
in the current directory; press any key or close the window to exit.

## How it works

- **Averaging:** for each square, the mean of each color channel (B, G, R) is
  computed independently and the whole square is set to that color. Squares at
  the right/bottom edges may be smaller than `square_size`; they are averaged the same way.
- **Large images:** if the image is larger than the screen, only the *displayed*
  copy is scaled down to fit. Processing and `result.jpg` always use the original
  full-resolution image.
- **Visible progress:** small images are processed in milliseconds, so by
  default a tiny delay per square is added (about 4 seconds in total for mode S).
  Mode M uses the same per-square delay, so its speed-up is visible.
  Use `--fast` to measure real processing time.



## Project structure

```
main.py              Command-line interface and program flow
image_processing.py  Image I/O and the averaging algorithm
runners.py           Single-threaded and multi-core processing modes
display.py           Window display and fit-to-screen scaling
requirements.txt     Python dependencies
```