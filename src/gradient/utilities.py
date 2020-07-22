"""
The purpose of this file was to contain all the utility functions that
would allow me to turn the output of the gradient class into labelled images.
This was mostly an afterthought and as such the code is messy, uncommented
poorly written.
"""

from PIL import Image, ImageDraw
import numpy as np


def create_pixel_gradient(x_res, y_res, colours):
    pixels = np.zeros((y_res, x_res, 3), dtype="uint8")

    column = 0
    step = x_res // len(colours)
    remainder = x_res % len(colours)

    for colour in colours:
        if remainder > 0:
            pixels[:, column:column+step+1 , :] = colour.scale_rgb().channels
            remainder -=1
            column += step + 1
        else:
            pixels[:, column:column+step , :] = colour.scale_rgb().channels
            column += step
    return pixels

def create_multi_gradient_array(gradients, x_res, y_res, spacer_thickness):
    num_of_gradients = len(gradients)
    final_y_res = (y_res * num_of_gradients) + (spacer_thickness * num_of_gradients)

    pixels = np.zeros((final_y_res, x_res, 3), dtype="uint8")

    row = spacer_thickness
    step = y_res

    for gradient in gradients:
        pixels[row+step:row+step+spacer_thickness, :, :] = (32, 33, 33)
        pixels[row:row+step, :, :] = create_pixel_gradient(x_res, y_res, gradient.colours)
        row += step + spacer_thickness
    return pixels

def create_image(pixel_array, colour_spaces, start_colour, end_colour, x_res, y_res, header_height):
    image = Image.fromarray(pixel_array)
    draw = ImageDraw.Draw(image)

    row = 0
    step = y_res + header_height

    start_colour = rgb_to_hex(start_colour.scale_rgb().get_round_values())
    end_colour = rgb_to_hex(end_colour.scale_rgb().get_round_values())

    for i in range(len(colour_spaces)):
        start_text = str(start_colour)
        start_text_size = draw.textsize(start_text)
        start_text_x_pos = 5

        end_text = str(end_colour)
        end_text_size = draw.textsize(end_text)
        end_text_x_pos = x_res - end_text_size[0] - 5

        cs_text = colour_spaces[i]
        cs_text_size = draw.textsize(cs_text)
        cs_text_x_pos = (x_res - cs_text_size[0]) / 2


        draw.text((start_text_x_pos, row + 2), start_text, (255, 255, 255))
        draw.text((end_text_x_pos, row + 2), end_text, (255, 255, 255))
        draw.text((cs_text_x_pos, row + 2), cs_text, (255, 255, 255))

        row += step
    return image

def rgb_to_hex(colour):
    return f"{int(colour[0]):02x}{int(colour[1]):02x}{int(colour[2]):02x}"


if __name__ == "__main__":
    from pathlib import Path
    from datetime import datetime

    from src.visualise.utilities import hex_to_rgb
    from src.gradient.gradient import Gradient
    from src.colour.colour import Colour


    parent = Path(__file__).resolve().parent.parent.parent
    path = parent / "img" / "gradients"
    path.mkdir(parents=True, exist_ok=True)
    path /= datetime.now().strftime("%y-%m-%d_%H-%M-%S.png")

    x = Colour(*hex_to_rgb("#270561"), scale_rgb=True)
    y = Colour(*hex_to_rgb("#c78d28"), scale_rgb=True)

    x_res = 600
    y_res = 100
    header_height = 15

    num_of_colours = 128

    grad1 = Gradient(x, y)
    grad1.blend(num_of_colours, "RGB")

    grad2 = Gradient(x, y)
    grad2.blend(num_of_colours, "HSV", reverse_direction=False)

    grad3 = Gradient(x, y)
    grad3.blend(num_of_colours, "HSV", reverse_direction=True)

    grad4 = Gradient(x, y)
    grad4.blend(num_of_colours, "XYZ")

    grad5 = Gradient(x, y)
    grad5.blend(num_of_colours, "LAB")

    grad6 = Gradient(x, y)
    grad6.blend(num_of_colours, "LCHab", reverse_direction=False)

    grad7 = Gradient(x, y)
    grad7.blend(num_of_colours, "LCHab", reverse_direction=True)

    colour_spaces = ["RGB", "HSV", "HSV+", "XYZ", "LAB", "LCHab", "LCHab+"]
    gradient_array = [grad1, grad2, grad3, grad4, grad5, grad6, grad7]
    pixel_array = create_multi_gradient_array(gradient_array, x_res, y_res, header_height)

    image = create_image(pixel_array, colour_spaces, x, y, x_res, y_res, header_height)
    image.save(path)
