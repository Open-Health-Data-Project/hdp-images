import math
import numpy as np


def find_optimal_crop(image, width, height):
    left_upper = [0, 0]
    right_upper = [0, 0]
    right_bottom = [0, 0]
    left_bottom = [0, 0]

    for i in range(width):
        if (image[0, i] == [0, 0, 0]).all():
            left_upper[1] = i
        else:
            break

    for i in range(width):
        if (image[height-1, i] == [0, 0, 0]).all():
            left_bottom[1] = i
        else:
            break

    for i in range(width-1, 0, -1):
        if (image[0, i] == [0, 0, 0]).all():
            right_upper[1] = width - i
        else:
            break

    for i in range(width-1, 0, -1):
        if (image[height-1, i] == [0, 0, 0]).all():
            right_bottom[1] = width - i
        else:
            break

    for i in range(height):
        if (image[i, 0] == [0, 0, 0]).all():
            left_upper[0] = i
        else:
            break

    for i in range(height):
        if (image[i, width-1] == [0, 0, 0]).all():
            right_upper[0] = i
        else:
            break

    for i in range(height-1, 0, -1):
        if (image[i, 0] == [0, 0, 0]).all():
            left_bottom[0] = height - i
        else:
            break

    for i in range(height-1, 0, -1):
        if (image[i, width-1] == [0, 0, 0]).all():
            right_bottom[0] = height - i
        else:
            break

    crop_borders = (left_upper, left_bottom, right_upper, right_bottom)

    for pair in crop_borders:
        if (pair[0] / height) > (pair[1] / width):
            pair[0] = 0
        else:
            pair[1] = 0

    crop_values = [max(left_upper[0], right_upper[0]), height - max(left_bottom[0], right_bottom[0]),
                   max(left_upper[1], left_bottom[1]), width - max(right_upper[1], right_bottom[1])]

    return crop_values


def crop(image):
    y_nonzero, x_nonzero, _ = np.nonzero(image)
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]


def largest_rotated_rect(w, h, angle):
    """
    Given a rectangle of size wxh that has been rotated by 'angle' (in
    radians), computes the width and height of the largest possible
    axis-aligned rectangle within the rotated rectangle.

    Original JS code by 'Andri' and Magnus Hoff from Stack Overflow

    Converted to Python by Aaron Snoswell
    """

    quadrant = int(math.floor(angle / (math.pi / 2))) & 3
    sign_alpha = angle if ((quadrant & 1) == 0) else math.pi - angle
    alpha = (sign_alpha % math.pi + math.pi) % math.pi

    bb_w = w * math.cos(alpha) + h * math.sin(alpha)
    bb_h = w * math.sin(alpha) + h * math.cos(alpha)

    gamma = math.atan2(bb_w, bb_w) if (w < h) else math.atan2(bb_w, bb_w)

    delta = math.pi - alpha - gamma

    length = h if (w < h) else w

    d = length * math.cos(alpha)
    a = d * math.sin(alpha) / math.sin(delta)

    y = a * math.cos(gamma)
    x = y * math.tan(gamma)

    return (
        bb_w - 2 * x,
        bb_h - 2 * y
    )


def crop_around_center(image, width, height):
    """
    Given a NumPy / OpenCV 2 image, crops it to the given width and height,
    around it's centre point
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if width > image_size[0]:
        width = image_size[0]

    if height > image_size[1]:
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]
