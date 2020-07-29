from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import pytest

import py_gd
from py_gd.colors import colorschemes

from .test_gd import outfile

all_color_schemes = ('magma',
                     'inferno',
                     'plasma',
                     'viridis',
                     'cividis',
                     'twilight',
                     # 'twilight_shifted',
                     'turbo',
                     'css4',
                     'tableau',
                     'xkcd',
                     'web',
                     )


# make sure the ones we expect are there
@pytest.mark.parametrize("color_name", all_color_schemes)
def test_known_colors(color_name):
    colors = colorschemes[color_name]
    assert len(colors) <= 256
    for n, rgb in colors:
        assert isinstance(n, str)
        assert len(rgb) in (3, 4)
        for i in rgb:
            assert 0 <= i <= 255
            assert isinstance(i, int)


@pytest.mark.parametrize("color_name", all_color_schemes)
def test_drawing_with_colors(color_name):
    """
    not really a test, but it does produce examples of all the colors
    """
    w, h = 60, 30
    dx = w + 10
    dy = h + 10

    W = (w + dx * 13)
    H = (h + dy * 23)
    im = py_gd.Image(W, H, preset_colors=color_name)

    print(im)
    print(im.get_color_names())
    colors = iter(colorschemes[color_name])
    for i in range(12):
        for j in range(22):
            try:
                color, rgb = next(colors)
            except StopIteration:
                break
            # im.draw_text(self, text, point, font="medium", color='black', align='lt',
            #              background='none')
            print('drawing a rectagle in:', color)
            x = i * dx
            y = j * dy
            im.draw_rectangle((x, y), (x + w, y + h),
                              fill_color=color,
                              )
    im.save(outfile("sample_{}.png").format(color_name), 'png')







