"""
Provides an interface for generating sorting visualisations.

TODO:
Creating GIFs can be a hassle. Need to have proper argument parsing, or maybe just a full CLI.

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
from viz.colourmaps import generate_gradient, colourmaps

if __name__ == "__main__":
    # -- Set USE_IMAGE to True if you want to sort an image. False if you want to use a gradient.
    USE_IMAGE = False  # Use an image or gradient as input?
    IMAGE_NAME = "starry_night.jpg"  # Image name. Place image in ../img/input

    # -- If using a gradient, set gradient settings.
    COLOUR_MAP = "plasma"   # choose from "custom", "viridis", "inferno", "plasma" and "magma"
    COLOUR_1 = "#270561"  # starting colour for custom gradients
    COLOUR_2 = "#c78d28"  # ending colour for custom gradients
    NUM_COLOURS = 128  # total colours in gradient
    GRAPHIC_TYPE = "pixels"  # alternative is "bars"
    COLOUR_SPACE = "LCHab"  # interpolation colour space for custom gradients
    DIRECTION = False  # Direction of interpolation. True to reverse. Only for custom gradients.

    # -- Visualisation attributes

    PREVIEW_GRADIENT = False
    RANDOM = True  # Randomise the image?
    REVERSE = False  # Reverse the image?
    ALGORITHM = sys.argv[1]  # Algorithm to use
    GIF_DURATION = 5  # Duration of GIF
    SCALE = True  # Does image need to be upscaled?
    RESCALE_X = 600  # x res of GIF
    RESCALE_Y = 200  # y res of GIF
    FPS = 16  # FPS of GIF
    FRAME_DELAY = 1 / FPS  # Delay between each GIF frame
    TOTAL_FRAMES = FPS * GIF_DURATION

    # -- Load image for use with visualiser
    if USE_IMAGE:
        img_path = Path(__file__).resolve().parent.parent / "img" / "input" / IMAGE_NAME
        img = Image.open(img_path)
        pixels = np.array(img)

    # -- Generate gradient for use with visualiser
    else:
        if GRAPHIC_TYPE == "bars":
            V_COLOURS = 1
        else:
            V_COLOURS = round(RESCALE_Y / (RESCALE_X / NUM_COLOURS))  # Maintain square pixel dimension during image upscaling.

        # -- Generate custom colour map using ColCon and GradientCreator
        if COLOUR_MAP == "custom":
            start_colour = Colour(*hex_to_rgb(COLOUR_1), scale_rgb=True)    # Create colours and scale_rgb down to 0-1 range
            end_colour = Colour(*hex_to_rgb(COLOUR_2), scale_rgb=True)

            # Create gradient and turn gradient into a pixel array.
            gradient = Gradient(start_colour, end_colour)   # Initialise gradient object
            gradient.blend(NUM_COLOURS, COLOUR_SPACE, reverse_direction=True)   # interpolate a gradient with NUM_COLOURS using COLOUR_SPACE
            pixels = create_pixel_gradient(NUM_COLOURS, V_COLOURS, gradient.colours)    # turn colours of gradient into a pixel array

        # -- Use existing matplotlib colour map
        else:
            gradient = generate_gradient(colourmaps[COLOUR_MAP], NUM_COLOURS)    # create gradient of NUM_COLOURS
            pixels = create_pixel_gradient(NUM_COLOURS, V_COLOURS, gradient)    # turn gradient into a pixel array
        #  -- Preview gradient and exit program if flag is set
        if PREVIEW_GRADIENT:
            img = Image.fromarray(pixels)
            img.resize((RESCALE_X, RESCALE_Y), Image.NEAREST).show()
            sys.exit()

    # -- Create our file directory (if it doesn't exist) and create file name.
    path = Path(__file__).resolve().parent.parent / "img" / ALGORITHM
    path.mkdir(parents=True, exist_ok=True)
    path /= datetime.now().strftime("%y-%m-%d_%H-%M-%S.gif")

    # -- Sort the image and visualise the swaps made.
    visualiser = SortingVisualiser(pixels, randomise=RANDOM, reverse=REVERSE)
    visualiser.sort(ALGORITHM)

    # -- If there are less swaps than frames in the gif, lower frame rate until 1 swap per frame
    if visualiser.max_swaps / TOTAL_FRAMES < 1:
        TOTAL_FRAMES = visualiser.max_swaps
        FRAME_DELAY = GIF_DURATION / TOTAL_FRAMES
        FPS = TOTAL_FRAMES / GIF_DURATION
    frames = visualiser.visualise(TOTAL_FRAMES, ALGORITHM)

    # -- Scale to desired resolution
    if SCALE:
        frames = scale_frames_nn(frames, RESCALE_X, RESCALE_Y)

    # -- Save
    imageio.mimsave(path, frames, duration=FRAME_DELAY)
