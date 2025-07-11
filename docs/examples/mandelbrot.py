"""
Drawing a Madelbrot set

Draws a Madelbrot by setting colors pixel by pixel
"""

import numpy as np
import py_gd as gd


def Mandelbrot_iter(c):
    z = 0
    for iters in range(200):
        if abs(z) >= 2:
            return iters
        z = z ** 2 + c
    return iters


def Mandelbrot(size):
    image = gd.Image(size, size, preset_colors='turbo')

    scale = size / 2
    x_shift = 1.5
    y_shift = 1.0

    v_max = 0
    for i in range(image.width):
        for j in range(image.height):
            x = (i / scale) - x_shift
            y = (j / scale) - y_shift
            v = Mandelbrot_iter( x + (y * 1j))
            print("i: %d, j: %d, v: %3d" % (i, j, v))
            image.set_pixel_value((i, j), v)
            v_max = max(v_max, v)
    return image

im = Mandelbrot(400)

im.save ("mandelbrot.png", file_type="png")
