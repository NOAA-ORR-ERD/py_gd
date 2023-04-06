"""
draw_dots.py


This draws a bunch of dots in different colors
and makes an animated gif of them.
"""

import numpy as np
from py_gd import Image, Animation

N = 50  # number of dots
w, h = 400, 400  # Size of image

img = Image(width=w, height=h)
img.clear('white')

# random colors: excluding first three: transparent, white, black
num_colors = len(img.get_colors())
colors = np.random.randint(3, num_colors - 1, N)

# initial position of the points
points = (np.random.random((N, 2)) * w).astype(np.int32)

# draw the initial image
img.draw_dots(points, diameter=10, color=colors)

#  Save the first frame as a PNG
img.save('dots.png', 'png')


# create the animation
anim = Animation('dots.gif',
                 delay=10,  # in 1/100s
                 )

anim.begin(img)

# Run a loop to move the dots, and make a new frame each time
for i in range(100):
    move = (np.random.random((N, 2)) * 20 - 10).astype(np.int32)
    points = points + move
    img.clear('white')
    img.draw_dots(points, diameter=10, color=colors)
    anim.add_frame(img)
anim.close()
