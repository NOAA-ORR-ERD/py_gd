"""
ultra_simple_example.py

About the simplest example for py_gd

This draws a red line at a diagonal across an image.
"""

from py_gd import Image

img = Image(width=400, height=400)

img.draw_line((1, 1), (400, 300), color='red', line_width=10)

img.save('my_image.png', 'png')

