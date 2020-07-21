"""
Provides an interface for generating sorting visualisations.

TODO:
GIF_DURATION variable is useless. Changes to the library for writing gifsmeans my gifs now last
as long as they want to. I'll get round to fixing it at some point I suppose.

Creating GIFs can be a hassle. Need to have proper argument parsing, or maybe just a full CLI.

Add a gradient preview option. Having to wait for a GIF to be created just to realise the gradient
looks awful is annoying.

Provide support for multi-colour input when creating gradients. Previously supported this but
removed it due to the code being messy. I'll reimplement it in a cleaner way when I find the time.

Provide error checking when using LCHab colour space. Shape of colour volume results in
unsupported RGB values when interpolating. As is, you just end up with ugly streaks in the gradient.
"""

import sys
from datetime import datetime
from pathlib import Path

import imageio
import numpy as np
from PIL import Image, ImageDraw

from colcon.colour import Colour
from gradient.gradient_class import Gradient
from gradient.utilities import create_pixel_gradient


def add_header(image, sorting_method, start_colour, end_colour):
    draw = ImageDraw.draw(image)

    start_text = str(start_colour)
    start_text_size = draw.textsize(start_text)
    start_text_x_pos = 5

    end_text = str(end_colour)
    end_text_size = draw.textsize(end_text)
    end_test_x_pos = image.size[0] - end_text_size[0] - 5

    sm_text = sorting_method
    sm_text_size = draw.textsize(sm_text)
    sm_text_x_pos = (image.size[0] - sm_text_size[0]) / 2

    draw.text((start_text_x_pos, 2), start_text, (255, 255, 255))
    draw.text((end_test_x_pos, 2), end_text, (255, 255, 255))
    draw.text((sm_text_x_pos, 2), sm_text, (255, 255, 255))


def hex_to_rgb(hex_code):
    rgb_tuple = []
    hex_code = hex_code.lstrip("#")
    for i in range(0, len(hex_code), 2):
        rgb_tuple.append(int(hex_code[i:i + 2], 16))
    return rgb_tuple

# Scaling takes time so provide some visual feedback
def progress_bar(text, iteration, max_iteration, length=40):
    percentage = (100 * iteration / max_iteration)
    completed = int(length * iteration / max_iteration)
    bar = '█' * completed + "-" * (length - completed)

    print("\r{}|{}|".format(text, bar), end='\r')

def progress_complete(text, length=40):
    bar = '█' * length
    print("\r{}|{}|".format(text, bar))


# Upscaling Algorithm -- Good for scaling pixel art and similar items
def nearest_neighbour(image, x_res, y_res):
    scaled_image = np.zeros((y_res, x_res, 3), dtype=np.uint8)
    for y in range(y_res):
        source_y = int(y / y_res * image.shape[0])
        for x in range(x_res):
            source_x = int(x / x_res * image.shape[1])
            scaled_image[y, x, :] = image[source_y, source_x, :]
    return scaled_image

def scale_frames_nn(frames, x_res, y_res):
    scaled_frames = []
    for i in range(len(frames)):
        scaled_frames.append(nearest_neighbour(frames[i], x_res, y_res))
        progress_bar("Scaling GIF:\t ", i, len(frames))
    progress_complete("Scaling GIF\t ")
    return scaled_frames


if __name__ == "__main__":
    # -------------- Initialise Variables -------------- #
    USE_IMAGE = False
    IMAGE_PATH = "img.jpg"

    COLOUR_1 = "#270561"  # starting colour
    COLOUR_2 = "#c78d28"  # ending colour
    NUM_COLOURS = 128  # total colours in gradient
    GRAPHIC_TYPE = "pixels"  # alternative is "bars"
    COLOUR_SPACE = "LCHab"  # interpolation colour space
    DIRECTION = False  # Direction of interpolation. True to reverse.
    RANDOM = True  # Randomise the image?
    REVERSE = False  # Reverse the image?
    ALGORITHM = sys.argv[1]  # Algorithm to use
    GIF_DURATION = 6  # Duration of GIF
    SCALE = True
    RESCALE_X = 600  # x res of GIF
    RESCALE_Y = 200  # y res of GIF
    FPS = 24  # FPS of GIF
    FRAME_DELAY = 40  # Delay between each GIF frame

    # ---------------- Variable Logic ---------------- #
    TOTAL_FRAMES = FPS * GIF_DURATION

    if USE_IMAGE:
        # ---------------- Load Image ---------------- #
        img = Image.open(IMAGE_PATH)
        pixels = np.array(img)

    else:
        # Determine number of vertical colours. 1 vertical colour for bars. > 1 for "pixel" look.  if GRAPHIC_TYPE == "bars":
        if GRAPHIC_TYPE == "bars":
            V_COLOURS = 1
        else:
            V_COLOURS = round(
                RESCALE_Y / (RESCALE_X / NUM_COLOURS)
            )  # Maintain square pixel dimension during image upscaling.

        # ---------------- Create Gradient ---------------- #
        # Turn input hex string into rgb tuple and create Colour objects.
        start_colour = Colour(*hex_to_rgb(COLOUR_1), scale_rgb=True)
        end_colour = Colour(*hex_to_rgb(COLOUR_2), scale_rgb=True)

        # Create gradient and turn gradient into a pixel array.
        gradient = Gradient(start_colour, end_colour)
        gradient.blend(NUM_COLOURS, COLOUR_SPACE, reverse_direction=True)
        pixels = create_pixel_gradient(NUM_COLOURS, V_COLOURS, gradient)

        # ---------------- Preview Gradient ----------------- #
        PREVIEW_GRADIENT = False  # Display gradient and exit if true
        if PREVIEW_GRADIENT:
            Image.fromarray(nearest_neighbour(pixels, RESCALE_X,
                                              RESCALE_Y)).show()
            sys.exit()
        # --------------------------------------------------- #

    # Create out file diferectory (if it doesn't exist) and create file name.
    path = Path(__file__).resolve().parent.parent / "img" / ALGORITHM
    path.mkdir(parents=True, exist_ok=True)
    path /= datetime.now().strftime("%y-%m-%d_%H-%M-%S.gif")

    # Sort the image and visualise the swaps made.
    visualiser = SortingVisualiser(pixels, randomise=RANDOM, reverse=REVERSE)
    visualiser.sort(ALGORITHM)

    if visualiser.max_swaps / TOTAL_FRAMES < 1:  # If there are less swaps than frames in the gif, lower frame rate until 1 swap per frame.
        TOTAL_FRAMES = visualiser.max_swaps
        FRAME_DELAY = GIF_DURATION / TOTAL_FRAMES
        FPS = TOTAL_FRAMES / GIF_DURATION
    frames = visualiser.visualise(
        TOTAL_FRAMES, ALGORITHM)  # Generate frames of the visualisation

    # Scale to desired resolution and save
    if SCALE:
        frames = scale_frames_nn(frames, RESCALE_X, RESCALE_Y)
    imageio.mimsave(path, frames)
