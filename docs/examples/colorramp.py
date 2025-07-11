"""
Using a Color Ramp

Example of how to use a colorramp

In this case, we plot a "Heatmap" of a surface from the equation:

z = sin(x) + sin(y)
"""

import numpy as np
from py_gd import Image
from py_gd.color_ramp import ColorRamp

N = 100  # number or grid points
D = 9 # diameter of dots
w, h = 600, 600  # Size of image


# Compute the function:

span = np.linspace(0, 2 * np.pi, N)

X, Y = np.meshgrid(span, span)

Z = np.sin(X) + np.cos(Y)

# create an image:

img = Image(width=w, height=h, preset_colors='BW')

# create a ColorRamp:
ramp = ColorRamp(colors='magma',  # use the magma colorscheme from MPL
                 min_value=-2.0,
                 max_value=2.0,
                 base_colorscheme=len(img.get_colors()),  # make sure we accommodate what's there
                 )

# and the ramp colors to the image:
img.add_colors(ramp.colorlist)
# draw the initial image, using dots:

x = (X / np.pi / 2 * h).flat
y = (Y / np.pi / 2 * w).flat

points = np.c_[x, y]
colors = ramp.get_color_indices(Z.flat)


img.draw_dots(points, diameter=D, color=colors)

#  Save the image as a PNG
img.save('colorramp.png', 'png')
