"""
py_gd demo with moderate complexity -- showing a number of the features

"""

from py_gd import Image

img = Image(width=600, height=600, preset_colors='xkcd')

img.clear('lilac')

img.draw_line((0, 0), (600, 600), color='red', line_width=10)

img.save("moderate_complex.png", 'png')

