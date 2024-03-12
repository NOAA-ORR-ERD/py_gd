"""
Drawing a star with a spline
"""

import numpy as np

import py_gd

NUM_POINTS = 5

r1 = 100
r2 = 30

r = (r1, r2) * NUM_POINTS

angles = np.arange(NUM_POINTS  * 2) *  (np.pi / NUM_POINTS)


x = r * np.sin(angles)
y = r * np.cos(angles)

vertices = np.c_[x, y]

centers = [(r1 * 1.2 * i, r1 * 1.2 * j) for i in (1, 3) for j in (1, 3)]

#vertices += r1 * 1.2

# vertices = vertices.astype(np.int32)

w, h = r1 * 4.8, r1 * 4.8

img = py_gd.Image(w, h)
img.clear('white')

print("Vertices of Star")
print(vertices)

for c, smooth in zip(centers, (0.25, 0.5, 0.75, 1.0)):
    verts = vertices + c
    img.draw_spline_polygon(verts,
                            fill_color='yellow',
                            line_color='black',
                            smoothness=smooth)
    img.draw_text(f"smoothness={smooth}", (c[0], c[1] - r1), align="cb")

img.save("spline_star.png", 'png')




