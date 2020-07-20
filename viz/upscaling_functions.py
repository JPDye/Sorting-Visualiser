"""
Using PIL to upscale and save GIFs results in artefacts so I use
array2gif instead. array2gif doesn't have an upscaling function so
my only option is to convert my frames to PIL images, upscale, convert
back to numpy arrays and save with array2gif. Or... I could learn a
bit about upscaling algorithms and implement it myself.
"""

import numpy as np


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
    import numpy as np
    from PIL import Image

    from colcon.colour import Colour
    from axial.gradient_class import Gradient
    from axial.utilities import create_pixel_gradient

    colour_1 = (Colour(255, 0, 0, scale_rgb=True))
    colour_2 = (Colour(0, 0, 255, scale_rgb=True))

    gradient = Gradient(colour_1, colour_2)
    gradient.blend(10, "HSV", reverse_direction=False)

    pixels = create_pixel_gradient(10, 10, gradient)
    for i in range(pixels.shape[0]):
        np.random.shuffle(pixels[i, :, :])

    # PIL scaling
    Image.fromarray(pixels).resize((600, 600), Image.NEAREST).show()

    # My Scaling
    Image.fromarray(nearest_neighbour(pixels, 600, 300)).show()
