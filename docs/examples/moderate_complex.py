"""
py_gd demo with moderate complexity -- showing a number of the features

"""

from py_gd import Image

img = Image(width=600, height=600, preset_colors='xkcd')

img.clear('lilac')

img.save("moderate_complex.png", 'png')

