"""
Automatic Colour Converter
--------------------------

This document contains the code for the ColourConverter class
which provides functionality for converting between colour spaces
simply by entering the input colour space and the desired output
colour space. No need to understand what conversions need to take place
to reach the final colour space.

The ColourConverter class can be considered as having two parts.

The first 'part' is the code that allow for converting between
individual colour spaces such as the 'convert_LAB_to_LCHab' and
'convert_RGB_to_HSV' functions. All mathematics used for converting
between colour space has been taken from Bruce Lindblooms website
and tested against his own colour space conversion calculator.

The second 'part' is the code that creates the conversion graph
and conversion logic. This code initalises and populates the
conversion graph as well as executing the 'conversion_path' output
by the graph.

TODO:
Add more colour spaces. Munsell and CIE CAM02 are particularly
interesting for their perceptual uniformity. Munsell can't be created
by transforming a CIE colour space. It has to be read from a lookup table
which means additional functionality would need to be added to the
Colour Converter class. CIE CAM02 would be easier. The maths for converting
from XYZ to CAM02 can be found on wikipedia. Just got to find time.

Support changing the Standard Illuminant / Reference White. Default
for this project is D65 which isn't ideal.

Support changing the viewing angle. Default for this project is 2Degrees.
Not as useful as be able to change the RefWhite but would be nice functionality.

Provide some colour difference functions.
"""

from src.colour.colour import Colour
from src.colour.digraph import DiGraph

class ColourConverter:
    def __init__(self):
        self._supported_conversions = [
            ("RGB", "sRGB"),
            ("sRGB", "RGB"),

            ("RGB", "HSV"),
            ("HSV", "RGB"),

            ("RGB", "XYZ"),
            ("XYZ", "RGB"),

            ("XYZ", "LAB"),
            ("LAB", "XYZ"),

            ("LAB", "LCHab"),
            ("LCHab", "LAB")]
        self._conversion_graph = self.__create_conversion_graph()

    def __create_conversion_graph(self):
        graph = DiGraph()
        for start, end in self._supported_conversions:
            conversion_function = eval(f"self.convert_{start}_to_{end}")

            if start not in graph:
                vert_one = graph.insert_vertex(start)
            else:
                vert_one = graph.find_vert(start)

            if end not in graph:
                vert_two = graph.insert_vertex(end)
            else:
                vert_two = graph.find_vert(end)
            graph.insert_edge(vert_one, vert_two, conversion_function)
        return graph

    def __execute_conversion_path(self, colour, path):
        for edge in path:
            colour = edge.element()(colour)
        return colour

    def convert_colour(self, colour, final_colour_space):
        conversion_path = self._conversion_graph.find_path(colour.colour_space, final_colour_space, "dfs")
        return self.__execute_conversion_path(colour, conversion_path)

    def convert_RGB_to_sRGB(self, colour):
        """
        RGB  ---> R: 0-1, G: 0-1, B: 0-1
        sRGB <--- R: 0-1, G: 0-1, B: 0-1
        """
        if colour.colour_space =="RGB":
            colour.colour_space = "sRGB"
            rgb = colour.channels
            sRGB = []

            for i in rgb:
                if i < 0.0031308:
                    i = i * 12.92
                else:
                    i = 1.055 * pow(i, 1 / 2.4) - 0.055
                sRGB.append(i)
            colour.channels = tuple(sRGB)
            return colour
        else:
            raise ValueError("colour-space is not RGB")

    def convert_sRGB_to_RGB(self, colour):
        """
        sRGB ---> R: 0-1, G: 0-1, B: 0-1
        RGB  <--- R: 0-1, G: 0-1, B: 0-1
        """
        if colour.colour_space == "sRGB":
            colour.colour_space = "RGB"
            sRGB = colour.channels
            rgb = []

            for i in sRGB:
                if i <= 0.04045:
                    i /= 12.92
                else:
                    i = ((i + 0.055) / 1.055) ** 2.4
                rgb.append(i)
            colour.channels = tuple(rgb)
            return colour
        else:
            raise ValueError("colour-space is not RGB")

    def convert_RGB_to_HSV(self, colour):
        """
        RGB ---> R: 0-1, G: 0-1, B: 0-1
        HSV <--- H: 0-360, G: 0-1, B: 0-1
        """

        if colour.colour_space == "RGB":
            colour.colour_space = "HSV"

            r, g, b =  colour.channels

            c_max = max(r, g, b)
            c_min = min(r, g, b)
            delta = c_max - c_min

            # Hue Calculation
            if delta == 0:
                h = 0
            elif c_max == r:
                h = 60 * (((g - b) / delta) % 6)
            elif c_max == g:
                h = 60 * (((b - r) / delta) + 2)
            else:
                h = 60 * (((r - g) / delta) + 4)

            # Saturatoin Calculation
            if c_max == 0:
                s = 0
            else:
                s = delta / c_max

            # Value Calculation
            v = c_max

            colour.channels = (h, s, v)
            return colour
        else:
            raise ValueError("colour-space is not RGB")

    def convert_HSV_to_RGB(self, colour):
        """
        HSV ---> H: 0-360, S: 0-1, V: 0-1
        RGB <--- R: 0-1, 0-1, 0-1
        """
        if colour.colour_space == "HSV":
            colour.colour_space = "RGB"

            h, s, v = colour.channels

            if h >= 360:
                h -= 360

            if h < 0:
                h += 360

            c = v * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = v - c

            if 0 <= h < 60:
                r, g, b = c, x, 0
            elif 60 <= h < 120:
                r, g, b = x, c, 0
            elif 120 <= h < 180:
                r, g, b = 0, c, x
            elif 180 <= h < 240:
                r, g, b = 0, x, c
            elif 240 <= h < 300:
                r, g, b = x, 0, c
            elif 300 <= h < 360:
                r, g, b = c, 0, x

            r += m
            g += m
            b += m

            colour.channels = (r, g, b)
            return colour
        else:
            raise ValueError("colour-space is not HSV")

    def convert_RGB_to_XYZ(self, colour):
        """
        RGB ---> R: 0-255, G: 0-255, B: 0-255
        XYZ <--- X: 0-1, y: 0-1, Z: 0-1
        """
        if colour.colour_space == "RGB":
            colour.colour_space = "XYZ"

            matrix = [[ 0.4124564, 0.3575761, 0.1804375],
                      [ 0.2126729, 0.7151522, 0.0721750],
                      [ 0.0193339, 0.1191920, 0.9503041]]

            r, g, b = colour.channels

            x = r * matrix[0][0] + g * matrix[0][1] + b * matrix[0][2]
            y = r * matrix[1][0] + g * matrix[1][1] + b * matrix[1][2]
            z = r * matrix[2][0] + g * matrix[2][1] + b * matrix[2][2]

            colour.channels = (x, y, z)
            return colour
        else:
            raise ValueError("colour-space is not RGB")

    def convert_XYZ_to_RGB(self, colour):
        """
        XYZ <--- X: 0-1, y: 0-1, Z: 0-1
        RGB ---> R: 0-255, G: 0-255, B: 0-255

        """
        if colour.colour_space == "XYZ":
            colour.colour_space = "RGB"

            matrix = [[ 3.2404542,  -1.5371385,  -0.4985314],
                      [-0.9692660,   1.8760108,   0.0415560],
                      [ 0.0556434,  -0.2040259,   1.0572252]]

            x, y, z = colour.channels



            r = x * matrix[0][0] + y * matrix[0][1] + z * matrix[0][2]
            g = x * matrix[1][0] + y * matrix[1][1] + z * matrix[1][2]
            b = x * matrix[2][0] + y * matrix[2][1] + z * matrix[2][2]

            colour.channels = (abs(r), abs(g), abs(b))
            temp = colour.scale_rgb().get_round_values()
            return colour
        else:
            raise ValueError("colour-space is not XYZ")

    def convert_XYZ_to_LAB(self, colour):
        """
        XYZ ---> X: 0-1, Y: 0-1, Z: 0-1
        LAB <--- L: 0-100, A: -128-127, B: -128-127
        """
        if colour.colour_space == "XYZ":
            colour.colour_space = "LAB"

            x, y, z = colour.channels

            # D65 and 2 Degree Oberserver
            white_x = 95.0470 / 100
            white_y = 100.000 / 100
            white_z = 108.883 / 100

            x_r = x / white_x
            y_r = y / white_y
            z_r = z / white_z

            k = 24389 / 27
            e = 216 / 24389

            if x_r > e:
                f_x = x_r ** (1/3)
            else:
                f_x = (k * x_r + 16) / 116

            if y_r > e:
                f_y = y_r ** (1/3)
            else:
                f_y = (k * y_r + 16) / 116

            if z_r > e:
                f_z = z_r ** (1/3)
            else:
                f_z = (k * z_r + 16) / 116

            l = 116 * f_y - 16
            a = 500 * (f_x - f_y)
            b = 200 * (f_y - f_z)

            colour.channels = (l, a, b)
            return colour
        else:
            raise ValueError("colour-space is not XYZ")


    def convert_LAB_to_XYZ(self, colour):
        """
        LAB ---> L: 0-100, A: -128-127, B: -128-127
        XYZ <--- X: 0-1, Y: 0-1, Z: 0-1
        """
        if colour.colour_space == "LAB":
            colour.colour_space = "XYZ"

            l, a, b = colour.channels

            f_y = (l + 16) / 116
            f_z = f_y - (b / 200)
            f_x = (a / 500) + f_y

            white_x = 95.0470 / 100
            white_y = 100.000 / 100
            white_z = 108.883 / 100

            k = 24389 / 27
            e = 216 / 24389

            if (f_x ** 3) > e:
                x_r = f_x ** 3
            else:
                x_r = (116 * f_x - 16) /k


            if l > (k * e):
                y_r = ((l + 16) / 116) ** 3
            else:
                y_r = l / k


            if (f_z ** 3) > e:
                z_r = f_z ** 3
            else:
                z_r = (116 * f_z - 16) / k

            x = white_x * x_r
            y = white_y * y_r
            z = white_z * z_r

            colour.channels = (x, y, z)
            return colour
        else:
            raise ValueError("colour-space is not LAB")

    def convert_LAB_to_LCHab(self, colour):
        """
        LAB   ---> L: 0-100, A: -128-127, B: -128-127
        LCHab <--- L: 0-100, C: 0-100, H: 0-360

        """
        if colour.colour_space == "LAB":
            colour.colour_space = "LCHab"
            l, a, b = colour.channels

            c = (a ** 2 + b ** 2) ** 0.5

            from math import atan, atan2, pi

            # Calculate H in radians.
            if atan2(b, a) >= 0:
                h = atan2(b, a)
            else:
                h = atan2(b, a)  + (2 * pi)     # If hue is < 0 degrees add 360 degrees

            h *= (180 / pi)

            colour.channels = (l, c, h)
            return colour
        else:
            raise ValueError("colour-space is not LAB")

    def convert_LCHab_to_LAB(self, colour):
        """
        LCHab ---> L: 0-100, C: 0-100, H: 0-360
        LAB   <--- L: 0-100, A: -128-127, B: -128-127
        """
        if colour.colour_space == "LCHab":
            colour.colour_space = "LAB"
            l, c, h = colour.channels

            from math import cos, sin, pi

            h = h * (pi / 180) # Convert degrees to radians.
            a = (c * cos(h))
            b = (c * sin(h))

            colour.channels = l, a, b
            return colour
        else:
            raise ValueError("colour-space is not LCHab")

if __name__ == "__main__":
    colour = Colour(0, 0, 1, "HSV")
    converter = ColourConverter()
    print(converter.convert_colour(colour, "HSV"))
