import numpy as np


# Add header to a frame
def add_header(image, sorting_method, start_colour, end_colour):
    """
    Add label to GIF with the sorting method and gradient colours displayed.
    """
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


# Easier way to add input colours to gradient creator
def hex_to_rgb(hex_code):
    """
    Convert hex values into RGB.
    """
    rgb_tuple = []
    hex_code = hex_code.lstrip("#")
    for i in range(0, len(hex_code), 2):
        rgb_tuple.append(int(hex_code[i:i + 2], 16))
    return rgb_tuple

# Execution can take a while. Progress bars provide visual proof that program isn't hanging.
def progress_bar(text, iteration, max_iteration, length=40):
    percentage = (100 * iteration / max_iteration)
    completed = int(length * iteration / max_iteration)
    bar = '█' * completed + "-" * (length - completed)

    print("\r{}|{}|".format(text, bar), end='\r')

def progress_complete(text, length=40):
    bar = '█' * length
    print("\r{}|{}|".format(text, bar))

# Imageio doesn't provide upscaling algorithms and I don't want to use PIL scaling
def nearest_neighbour(image, x_res, y_res):
    scaled_image = np.zeros((y_res, x_res, 3), dtype=np.uint8)
    for y in range(y_res):
        source_y = int(y / y_res * image.shape[0])
        for x in range(x_res):
            source_x = int(x / x_res * image.shape[1])
            scaled_image[y, x, :] = image[source_y, source_x, :]
    return scaled_image

def scale_frames_nn(frames, x_res, y_res):
    """
    Apply nearest neighbour scaling to every frame of a GIF and Display progress.
    """
    scaled_frames = []
    for i in range(len(frames)):
        scaled_frames.append(nearest_neighbour(frames[i], x_res, y_res))
        progress_bar("Scaling GIF:\t", i, len(frames))
    progress_complete("Scaling GIF\t")
    return scaled_frames
