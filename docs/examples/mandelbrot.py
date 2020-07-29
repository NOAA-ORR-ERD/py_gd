import numpy as np
import py_gd as gd


def Mandelbrot_iter (c):
    z = 0
    for iters in range(200):
        if abs(z) >= 2:
            return iters
        z = z ** 2 + c
    return iters


def Mandelbrot(size):
    image = gd.Image(400, 400, preset_colors='turbo')

    xPts = np.arange(-1.5, 0.5, 2.0 / size)
    yPts = np.arange(-1, 1, 2.0 / size)
    scale = 400.0 / 2
    x_shift = 1.5
    y_shift = 1.0

    for xx, x in enumerate(xPts):
        for yy, y in enumerate(yPts):
            # v = Mandelbrot_iter(np.complex(x, y))
            v = Mandelbrot_iter( x + y * 1j)
            _x = scale * (x + x_shift)
            _y = scale * (y + y_shift)
            print("_x: %6.2f, _y: %6.2f, v: %3d" % (_x, _y, v))
            image.set_pixel_value((_x, _y), v)
    return image

im = Mandelbrot(100)

im.save ("Mandelbrot.png", file_type="png")
