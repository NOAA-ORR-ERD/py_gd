# Tests of using a "color ramp" or "heatmap"
#
# This is for when you want to use a continuous color map
# with the colors changing value

from pathlib import Path

import numpy as np

from py_gd.colors import colorschemes, colorscheme_names
from py_gd.color_ramp import ColorRamp

from py_gd import Image
from .test_gd import outfile, check_file

import pytest

def test_color_index():
    colors = [(i, i+5, 1+10) for i in range(25)]

    cr = ColorRamp(colors, 0, 1000, num_colors=100)

    assert cr.color_index.shape == (100, 3)
    assert np.all(cr.color_index[0] == colors[0])
    assert np.all(cr.color_index[-1] == colors[-1])


def test_init_with_named_scheme():
    scheme = 'inferno'
    cr = ColorRamp(scheme, 100, 1000, num_colors=250)
    colors = colorschemes[scheme]
    assert cr.color_index.shape == (250, 3)
    assert np.all(cr.color_index[0] == colors[0][1])
    assert np.all(cr.color_index[-1] == colors[-1][1])


def test_init_with_named_base_colors():
    scheme = 'inferno'
    cr = ColorRamp(scheme, 100, 1000, base_colorscheme='web')

    assert cr.start_index == len(colorschemes['web'])
    assert cr._num_colors == 256 - len(colorschemes['web'])


def test_init_with_int_base_colors():
    scheme = 'inferno'
    cr = ColorRamp(scheme, 100, 1000, base_colorscheme=6)

    assert cr.start_index == 6


def test_get_color_indices():
    """
    should get the color index directly for the color
    """
    scheme = 'inferno'
    cr = ColorRamp(scheme, 100, 1000, num_colors=200, base_colorscheme=5)

    inds = cr.get_color_indices([50, 100, 500, 1000, 1100])

    assert inds.dtype == np.uint8
    assert inds.shape == (5,)
    assert np.all(inds - 5 == [0, 0, 89, 199, 199])


def test_get_colors():
    """
    get the rgb colors corresponding to the values
    """
    scheme = 'inferno'
    cr = ColorRamp(scheme, 100, 1000, num_colors=200)

    colors = cr.get_colors([50, 100, 500, 1000, 1100])

    assert colors.dtype == np.uint8
    assert colors.shape == (5, 3)
    assert np.all(colors == [[0, 0, 4],
                             [0, 0, 4],
                             [166, 45, 95],
                             [252, 255, 164],
                             [252, 255, 164],
                             ])


def test_colorlist():
    """
    colorlist is supposed to return a list of colors compatible with
    Image.add_colors
    """
    scheme = 'inferno'
    cr = ColorRamp(scheme, 100, 1000, num_colors=10)

    colorlist = cr.colorlist

    print(colorlist)

    for c in colorlist:
        assert isinstance(c[0], str)
        assert len(c[1]) == 3

    # make sure there aren't any duplicates
    # Image doesn't let you add duplicate color names
    assert len(set(colorlist)) == len(colorlist)

def test_image_with_colorramp():
    """
    generate an image using a colorramp
    """
    w, h, = 500, 500
    img = Image(w, h, preset_colors='BW')

    points = np.array([(x, y) for x in range(0, w, 10) for y in range(0, h, 10)])

    values = np.hypot(points[:, 0], points[:, 1])

    existing_colors = img.get_color_names()

    print(existing_colors)

    cr = ColorRamp('inferno', 0, np.hypot(500, 500), base_colorscheme=len(existing_colors))

    img.add_colors(cr.colorlist)

    color_idx = cr.get_color_indices(values)

    img.draw_dots(points, diameter=10, color=color_idx)

    img.save(outfile("test_image_with_colorramp.png"), 'png')

    assert check_file("test_image_with_colorramp.png")

schemes = [name[0] for name in colorscheme_names if name[1] == 'continuous']
@pytest.mark.parametrize("scheme", schemes)
def test_image_with_all_colorramps(scheme):
    """
    Make sure an image can be generated with all the included color ramps

    NOTE: This does not test that they are rendered properly,
          Just that they can be created.
    """
    w, h, = 500, 500
    img = Image(w, h, preset_colors='BW')

    points = np.array([(x, y) for x in range(0, w, 10) for y in range(0, h, 10)])

    values = np.hypot(points[:, 0], points[:, 1])

    existing_colors = img.get_color_names()

    cr = ColorRamp(scheme, 0, np.hypot(500, 500), base_colorscheme=existing_colors)

    img.add_colors(cr.colorlist)

    color_idx = cr.get_color_indices(values)

    img.draw_dots(points, diameter=10, color=color_idx)

    img.save(outfile("test_image_with_colorramp.png"), 'png')

    assert Path(outfile("test_image_with_colorramp.png")).is_file()

