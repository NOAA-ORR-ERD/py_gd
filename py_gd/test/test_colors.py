
import pytest

import py_gd
from py_gd.colors import colorschemes, colorscheme_names

from .test_gd import outfile

basic_schemes = ('transparent', 'BW')
discrete_schemes = ('web', 'tableau', 'css4', 'xkcd')

continuous_schemes = ('cividis', 'inferno', 'magma', 'plasma', 'turbo',
                      'twilight', 'viridis')

all_color_schemes = basic_schemes + discrete_schemes + continuous_schemes

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
            print('drawing a rectangle in:', color)
            x = i * dx
            y = j * dy
            im.draw_rectangle((x, y), (x + w, y + h),
                              fill_color=color,
                              )
    im.save(outfile(f"sample_{color_name}.png"), 'png')


def test_colornames():
    names = colorscheme_names
    all_names = set(all_color_schemes)
    for name in names:
        assert name[0] in all_names
        assert name[1] in {'discrete', 'continuous'}






