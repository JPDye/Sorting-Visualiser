"""
Given two input colours, create a gradient with the given number of colour
spaces using the colour space provided.

TODO:
Reimpliment giving more than two colours as input for a gradient.

Rewrite 'generate_interval_list' function. The idea is awful and I only did it
this way to see if it would work. Could be done so much cleaner. wtf.

Remove 'reverse_direction' boolean. It's not hard to determine which direction
the shortest path to the correct colour is. I was just lazy.
"""

from src.colour.colour import Colour
from src.colour.converter import ColourConverter

from PIL import Image, ImageDraw
import numpy as np


class Gradient:
    def __init__(self, *colours):
        self.converter = ColourConverter()
        self.colours = [self.converter.convert_colour(colour, "RGB") for colour in colours]

    def convert_gradient_colour_space(self, colour_space):
        """Convert gradient array into desired colour space."""
        for colour in self.colours:
            self.converter.convert_colour(colour, colour_space)
        return self

    def group_colours(self):
        """Yield two colours from the gradient array at a time."""
        for i in range(len(self.colours) - 1):
            yield self.colours[i:i + 2]

    def generate_interval_list(self, final_amount):
        """Generates the number of interpolations that need to be done per colour grouping
        to achieve the desired output number of colours. Only necessary for the LCHab which
        gets interpolated twice, once in LCHab and again in RGB. Saves time as LCHab to RGB
        is expensive and  errors can occur when interpolating in the LCHab colour space due to
        the shape of it's colour solid.
        """
        num_of_existing_colours = len(self.colours)
        num_of_colours_to_create = final_amount - num_of_existing_colours

        loops_per_interpolation = num_of_colours_to_create // (num_of_existing_colours - 1)
        if loops_per_interpolation > 0:
            remainder = num_of_colours_to_create // loops_per_interpolation
            interval_list = []
            for i in range(len(self.colours) - 1):
                if remainder > 0:
                    interval = 1 / (loops_per_interpolation + 2)
                    remainder -= 1
                else:
                    interval = 1 / (loops_per_interpolation + 1)
                interval_list.append(interval)
        else:
            interval_list = [1]
        return interval_list

    def interpolate_between(self, start, end, interval):
        """Helper function for the interpolate function. Generates colours between two input colours."""
        new_colours = [start]
        step = interval
        while interval < 1:
            new_x = start[0] + (end[0] - start[0]) * interval
            new_y = start[1] + (end[1] - start[1]) * interval
            new_z = start[2] + (end[2] - start[2]) * interval
            new_colour = Colour(new_x, new_y, new_z, start.colour_space)
            new_colours.append(new_colour)
            interval += step
        return new_colours

    def interpolate(self, interval_list):
        """Create gradient from the input colours. Group them into twos and pass to the helper function."""
        new_colours = []
        for start, end in self.group_colours():
            interval = interval_list.pop()
            temp = self.interpolate_between(start, end, interval)
            new_colours.extend(temp)
        new_colours.append(self.colours[-1])
        return new_colours

    def blend(self, final_amount, colour_space="RGB", reverse_direction=False):
        self.convert_gradient_colour_space(colour_space)

        if colour_space == "RGB" or colour_space == "XYZ" or colour_space == "LAB":
            interval_list = self.generate_interval_list(final_amount)
            self.colours = self.interpolate(interval_list)

        elif colour_space == "HSV":
            if reverse_direction:
                # Traverse the colour space in the opposite direction
                if self.colours[0][0] < self.colours[-1][0]:
                    self.colours[0].channels = (self.colours[0][0] + 360, self.colours[0][1], self.colours[0][2])
                else:
                    self.colours[1].channels = (self.colours[1][0] + 360, self.colours[1][1], self.colours[1][2])
            interval_list = self.generate_interval_list(final_amount)
            self.colours = self.interpolate(interval_list)

        elif colour_space == "LCHab":
            if reverse_direction:
                # Traverse the colour space in the opposite direction
                if self.colours[0][2] < self.colours[-1][2]:
                    self.colours[0].channels = (self.colours[0][0], self.colours[0][1], self.colours[0][2] + 360)
                else:
                    self.colours[1].channels = (self.colours[1][0], self.colours[1][1], self.colours[1][2] + 360)

            # Interpolate to generate a few LCHab colours
            interval_list = self.generate_interval_list(3)
            self.colours = self.interpolate(interval_list)

            # Interpolate again in RGB colour space to populate to desired amount
            self.blend(final_amount, "RGB")
        self.convert_gradient_colour_space("sRGB")
        return self


if __name__ == "__main__":
    from src.gradient.utilities import create_multi_gradient_array, create_image

    def hex_to_rgb(hex_code):
        rgb_tuple = []
        hex_code = hex_code.lstrip("#")
        for i in range(0, len(hex_code), 2):
            rgb_tuple.append(int(hex_code[i:i+2], 16))
        return rgb_tuple

    rdir = False
    c1 = "#d9cd29"
    c2 = "#ab155b"
    a = Colour(*hex_to_rgb(c1), scale_rgb=True)
    b = Colour(*hex_to_rgb(c2), scale_rgb=True)

    gradient = Gradient(a, b)
    gradient.blend(100, "LCHab", reverse_direction=rdir)

    pixels = create_multi_gradient_array([gradient.colours], 600, 150, 15)
    create_image(pixels, ["LCHab"], a, b, 600, 150, 15).show()
