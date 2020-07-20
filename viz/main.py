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
import imageio

from pathlib import Path
from PIL import Image, ImageDraw

from datetime import datetime

from colcon.colour import Colour
from gradient.gradient_class import Gradient
from gradient.utilities import create_pixel_gradient
from viz.visualiser_class import SortingVisualiser
from viz.upscaling_functions import scale_frames_nn, nearest_neighbour

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
        rgb_tuple.append(int(hex_code[i:i+2], 16))
    return rgb_tuple


if __name__ == "__main__":
    # -------------- Initialise Variables -------------- #
    COLOUR_1 = "#270561"        # starting colour
    COLOUR_2 = "#c78d28"        # ending colour
    NUM_COLOURS = 100          # total colours in gradient
    GRAPHIC_TYPE = "pixels"     # alternative is "bars"
    COLOUR_SPACE = "LCHab"        # interpolation colour space
    DIRECTION = False           # Direction of interpolation. True to reverse.
    RANDOM = True               # Randomise the image?
    REVERSE = False             # Reverse the image?
    ALGORITHM = sys.argv[1]  # Algorithm to use
    GIF_DURATION = 2           # Duration of GIF
    RESCALE_X = 600             # x res of GIF
    RESCALE_Y = 600            # y res of GIF
    FPS = 24                    # FPS of GIF
    FRAME_DELAY = 40            # Delay between each GIF frame

    # ---------------- Vairable Logic ---------------- #
    TOTAL_FRAMES = FPS * GIF_DURATION

    # Determine number of vertical colours. 1 vertical colour for bars. > 1 for "pixel" look.
    if GRAPHIC_TYPE == "bars":
        V_COLOURS = 1
    else:
        V_COLOURS = round(RESCALE_Y / (RESCALE_X / NUM_COLOURS))    # Maintain square pixel dimension during image upscaling.

    # ---------------- Visualise Algorithm ---------------- #
    # Turn input hex string into rgb tuple and create Colour objects.
    start_colour = Colour(*hex_to_rgb(COLOUR_1), scale_rgb=True)
    end_colour = Colour(*hex_to_rgb(COLOUR_2), scale_rgb=True)

    # Create out file diferectory (if it doesn't exist) and create file name.
    path = Path(__file__).resolve().parent.parent / "img" / ALGORITHM
    path.mkdir(parents=True, exist_ok=True)
    path /= datetime.now().strftime("%y-%m-%d_%H-%M-%S.gif")

    # Create gradient and turn gradient into a pixel array.
    gradient = Gradient(start_colour, end_colour)
    gradient.blend(NUM_COLOURS, COLOUR_SPACE, reverse_direction=True)
    pixels = create_pixel_gradient(NUM_COLOURS, V_COLOURS, gradient)

    # ---------------- Preview Gradient ----------------- #
    PREVIEW_GRADIENT = False     # Display gradient and exit if true
    if PREVIEW_GRADIENT:
        Image.fromarray(nearest_neighbour(pixels, RESCALE_X, RESCALE_Y)).show()
        sys.exit()
    # --------------------------------------------------- #

    # Sort the image and visualise the swaps made.
    visualiser = SortingVisualiser(Image.fromarray(pixels), randomise=RANDOM, reverse=REVERSE)
    visualiser.sort(ALGORITHM)

    if visualiser.max_swaps / TOTAL_FRAMES < 1:     # If there are less swaps than frames in the gif, lower frame rate until 1 swap per frame.
        TOTAL_FRAMES = visualiser.max_swaps
        FRAME_DELAY = GIF_DURATION / TOTAL_FRAMES
        FPS = TOTAL_FRAMES / GIF_DURATION
    frames = visualiser.visualise(TOTAL_FRAMES, ALGORITHM)    # Generate frames of the visualisation

    # Scale to desired resolution and save
    scaled_frames = scale_frames_nn(frames, RESCALE_X, RESCALE_Y)
    imageio.mimsave(path, scaled_frames)
