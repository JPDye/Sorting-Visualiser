"""
Didn't really have a plan so what was once a large class with lots of functionality
got rewritten multiple times until it became tiny, containing functions that
probably shouldn't be inside of it.
"""

class Colour:
    def __init__(self, a, b, c, colour_space="sRGB", scale_rgb=False):
        if (colour_space == "RGB" or colour_space == "sRGB") and scale_rgb:
            a /= 255
            b /= 255
            c /= 255
        self.colour_space = colour_space
        self.channels = (a, b, c)

    def __str__(self):
        return str(self.channels)

    def __getitem__(self, key):
        return self.channels[key]

    def scale_rgb(self, up=True):
        if up:
            a = self.channels[0] * 255
            b = self.channels[1] * 255
            c = self.channels[2] * 255
        else:
            a = self.channels[0] / 255
            b = self.channels[1] / 255
            c = self.channels[2] / 255
        return Colour(a, b, c, self.colour_space)

    def get_round_values(self, precision=0):
        a, b, c = self.channels
        return (round(a, precision), round(b, precision), round(c, precision))

if __name__ == "__main__":
    pass
