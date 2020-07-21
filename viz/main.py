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

import random
import sys
from datetime import datetime
from pathlib import Path

import imageio
import numpy as np
from PIL import Image, ImageDraw

from colcon.colour import Colour
from gradient.gradient_class import Gradient
from gradient.utilities import create_pixel_gradient
from viz.utilities import hex_to_rgb, progress_bar, progress_complete, scale_frames_nn
from viz.visualiser import SortingVisualiser

if __name__ == "__main__":
    # -------------- Initialise Variables -------------- #
    USE_IMAGE = True  # Use an image or gradient as input?
    IMAGE_NAME = "starry_night_small.jpg"  # Path to image if we use one

    COLOUR_1 = "#270561"  # starting colour
    COLOUR_2 = "#c78d28"  # ending colour
    NUM_COLOURS = 128  # total colours in gradient
    GRAPHIC_TYPE = "pixels"  # alternative is "bars"
    COLOUR_SPACE = "LCHab"  # interpolation colour space
    DIRECTION = False  # Direction of interpolation. True to reverse
    RANDOM = True  # Randomise the image?
    REVERSE = False  # Reverse the image?
    ALGORITHM = sys.argv[1]  # Algorithm to use
    GIF_DURATION = 6  # Duration of GIF
    SCALE = False  # Does image need to be upscaled?
    RESCALE_X = 600  # x res of GIF
    RESCALE_Y = 600  # y res of GIF
    FPS = 24  # FPS of GIF
    FRAME_DELAY = 40  # Delay between each GIF frame
    TOTAL_FRAMES = FPS * GIF_DURATION

    # Load image and turn into numpy array if we are using one as input
    if USE_IMAGE:
        # --- Testing
        # Create random pixel grid to simulate image input
        # pixels = np.zeros((20, 20, 3), dtype="uint8")

        # colours = [
        # (255, 0, 0),
        # (0, 255, 0),
        # (0, 0, 255),
        # (255, 255, 0),
        # (255, 0, 255),
        # (0, 255, 255),
        # (0, 0, 0),
        # (255, 255, 255)
        # ]
        # create two colour grid to determine which function causes the error.
        # __replace_with_integers or __replace_with_pixels
        # for i in range(pixels.shape[0]):
        # for j in range(pixels.shape[1]):
        # pixels[i, j, :] = random.choice(colours)

        # --- Load Image
        img_path = Path(
            __file__).resolve().parent.parent / "img" / "input" / IMAGE_NAME
        img = Image.open(img_path)
        pixels = np.array(img)
        img = Image.fromarray(pixels).resize((RESCALE_X, RESCALE_Y), Image.NEAREST)
        img.show()

    # Generate colour gradient used as input to the visualiser
    else:
        # Determine number of vertical colours. 1 vertical colour for bars. > 1 for "pixel" look.  if GRAPHIC_TYPE == "bars":
        if GRAPHIC_TYPE == "bars":
            V_COLOURS = 1
        else:
            V_COLOURS = round(
                RESCALE_Y / (RESCALE_X / NUM_COLOURS)
            )  # Maintain square pixel dimension during image upscaling.

        # Turn input hex string into rgb tuple and create Colour objects.
        start_colour = Colour(*hex_to_rgb(COLOUR_1), scale_rgb=True)
        end_colour = Colour(*hex_to_rgb(COLOUR_2), scale_rgb=True)

        # Create gradient and turn gradient into a pixel array.
        gradient = Gradient(start_colour, end_colour)
        gradient.blend(NUM_COLOURS, COLOUR_SPACE, reverse_direction=True)
        pixels = create_pixel_gradient(NUM_COLOURS, V_COLOURS, gradient)

        # Preview gradient and exit program if flag is set
        PREVIEW_GRADIENT = False
        if PREVIEW_GRADIENT:
            img = Image.fromarray(pixels)
            img.resize((RESCALE_X, RESCALE_Y), Image.NEAREST).show()
            sys.exit()

    # Create our file diferectory (if it doesn't exist) and create file name.
    path = Path(__file__).resolve().parent.parent / "img" / ALGORITHM
    path.mkdir(parents=True, exist_ok=True)
    path /= datetime.now().strftime("%y-%m-%d_%H-%M-%S.gif")

    # Sort the image and visualise the swaps made.
    visualiser = SortingVisualiser(pixels, randomise=RANDOM, reverse=REVERSE)
    visualiser.sort(ALGORITHM)

    # If there are less swaps than frames in the gif, lower frame rate until 1 swap per frame
    if visualiser.max_swaps / TOTAL_FRAMES < 1:
        print(visualiser.max_swaps)
        TOTAL_FRAMES = visualiser.max_swaps
        FRAME_DELAY = GIF_DURATION / TOTAL_FRAMES
        FPS = TOTAL_FRAMES / GIF_DURATION
    frames = visualiser.visualise(TOTAL_FRAMES, ALGORITHM)

    # Scale to desired resolution and save
    if SCALE:
        frames = scale_frames_nn(frames, RESCALE_X, RESCALE_Y)
    imageio.mimsave(path, frames)
