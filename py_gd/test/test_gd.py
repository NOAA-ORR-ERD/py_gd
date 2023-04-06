#!/usr/bin/env python
"""
unit tests for the py_gd project

designed to be run with pytest:

py.test test_gd.py

"""

import sys
import hashlib
from pathlib import Path
import numpy as np

import pytest

from py_gd import Image, Animation, asn2array, from_array

print(py_gd.__version__)
print(py_gd.__file__)

HERE = Path(__file__).parent


def outfile(file_name):
    # just to make it a little easier to type..
    output_dir = HERE / "test_images_output"
    if not output_dir.exists():
        output_dir.mkdir()
    return output_dir / file_name


def check_file(name):
    """
    checks if the checksum of the passed in filename is the same as it was
    the last time the checksums were generated...
    """
    # checksums of all the images generated.
    # rebuild with the build_checksums.py script
    # you may need to do that with a new libjpeg version, for instance
    #  it would be nice if all images were checked, but only a few are now...
    checksums = {
        'image_clip.bmp': '6adb4af2332bedec46815f86ac462b9f',
        'image_copy.bmp': 'a0e7ffb4ecada86965fcfc60a032cad4',
        'image_copy_middle1.bmp': '0ac48cdf5e2652999a33efa6c558a9b7',
        'image_copy_middle2.bmp': '09be326e5940e58dfdfa492e03d7e818',
        'image_copy_trans.png': '8939012bbd494ec19c8afa639eedafb8',
        'image_copy_upper_left.bmp': '24f96fb535350df3cdcdc25bcb95a25a',
        'nothing.gif': 'fa2e02f338a8ab98c5c1f3cd280ca505',
        'one_frame_delete.gif': '35d46c172f95bf79fa66eb0c4f114ada',
        'sample_BW.png': 'a211aaa9093b345bc2c7944aaef76899',
        'sample_cividis.png': '5b6af4aa252d0a84969dfe93cdb489ae',
        'sample_css4.png': '43ffd2b528e067c37e46fed685bc6297',
        'sample_inferno.png': '850806ac80c706bf510d38443d3b145a',
        'sample_magma.png': '0ebdc1856554e2ed441cf94883a59bf9',
        'sample_plasma.png': 'd1e954be4f07b5b4b2bd712022525425',
        'sample_tableau.png': 'b64d48d10529655065a78149c2e16529',
        'sample_transparent.png': 'a60406f4c35294111ab6a1eda9eeb63a',
        'sample_turbo.png': 'c19b0b0c474ba425c3f5015a086aa8c8',
        'sample_twilight.png': 'ef008e3ca66132b49e7ff11d96ac0ba7',
        'sample_viridis.png': '8fe4956a7c00136e132ade927b433982',
        'sample_web.png': '5d5a8f1de03282ea675cf591eb32b815',
        'sample_xkcd.png': '83dd36fb952930d99ac4e68f23045906',
        'test_animation.gif': '3abc5d1963116b1a05701978b048ac8a',
        'test_animation_reset1.gif': 'a53e5aaebcf441f002927b913c12f213',
        'test_animation_reset2.gif': 'ec5961189acd876f73f8132707f13c82',
        'test_animation_reset_same.gif': 'ec5961189acd876f73f8132707f13c82',
        'test_animation_reuse.gif': 'a45117a3d17f1093d5e395fcc20e69e1',
        'test_animation_reuse_not_close.gif':
        '7587576ac36cd0e2e8bcd8ee4ff52b82',
        'test_animation_static.gif': '4639911d250a50f9a76a24bb23031921',
        'test_draw_dots_multi_color_indices.png':
        '415db687d254a58eb6d4cabc4be22ea8',
        'test_draw_dots_multi_named_colors.png':
        'ca7a67f726517e341b55366a7b08b48e',
        'test_image_arc.bmp': 'c0a3c29d49922cac32e4a6fae5c9ac4e',
        'test_image_array1.bmp': 'e268130b61eaecdc9d809b771909f7b6',
        'test_image_array2.bmp': 'e268130b61eaecdc9d809b771909f7b6',
        'test_image_circle.bmp': 'bc3e62938f64c5c084d176b99e7e156a',
        'test_image_clear_after.png': 'b6825be7e699ea19bd2571c3b4864dac',
        'test_image_clear_after2.png': '30bc477928a84571e60925fd61013a94',
        'test_image_clear_before.png': 'd34a1e3576b2732321f32c4ee1117730',
        'test_image_clear_before2.png': 'd34a1e3576b2732321f32c4ee1117730',
        'test_image_dot.png': 'ac9816fa29137487198c550be4e8db15',
        'test_image_dots_large.png': '0a49a24272e0e3bfba82fcdc21d3cb73',
        'test_image_dots_lots.png': '85b073f3d7d1d2d0797f8ac3b107a718',
        'test_image_ellipse.bmp': '543ec0befeb67d131f4df23eeb21e590',
        'test_image_grey.bmp': '46f3b8773ac4d552944a2eb378ba27e8',
        'test_image_line.bmp': 'd279707389a3bac62c4413839919b962',
        'test_image_line_clip.bmp': 'fe6e5505f60428d47a64124cbb86c68d',
        'test_image_pixel.bmp': '1bf9f74b1122d8b3cc4a955c7216feb7',
        'test_image_points.png': 'd16cb5b8b309f570940db8c17bccd9a1',
        'test_image_points3.png': 'fbbd89301eb5de8e7785da095c3c2b51',
        'test_image_poly1.bmp': 'd4654eb592716d5fe73c0661b39b39a7',
        'test_image_poly2.bmp': '066f46e0363d1c04b002ea1d6716a07f',
        'test_image_poly3.bmp': '4fa4411acb4aee16a1c6a2e15df44cc5',
        'test_image_polygon_clip.bmp': 'fb8037129941fd6c9e2686f0c109496b',
        'test_image_polyline.bmp': '01d7d25972d69796af9fefc67a1e17af',
        'test_image_rectangle.bmp': 'f0eff1deadc678b78e26bd1a4cd88810',
        'test_image_save.bmp': '1facb71e1f6d0e21abfb8b07ae900a49',
        'test_image_save.gif': '50f1d8d494edba646813b7e7ab830e64',
        'test_image_save.jpg': 'e6d5a45b093988240cbe3d0365c0675a',
        'test_image_save.png': '3067832d58ce76285b7e32d3f42e2659',
        'test_image_text.bmp': 'a7b1fe64f4da978706d857c39ce5c026',
        'test_image_with_colorramp.png': '1ac385ddcbe4b179ba00e718384f31d7',
        'test_image_x_large.png': 'e57caa7c4304f3806eb3f327ff717076',
        'test_image_x_lots.png': '4c3c223185c407c8ead2afbf28244ebe',
        'test_text_align.bmp': '3151fe59ab1177fe6fde144dedae1082',
        'test_text_background.bmp': 'da827b0d1bba63eba680d7328153c82d'
        }
    cs = hashlib.md5(open(outfile(name), 'rb').read()).hexdigest()
    if checksums[name] == cs:
        return True
    else:
        print("Checksum did not match for file:", name)
        return False


def test_init_simple():
    """
    simplest possible initialization -- no preset color palette
    """
    img = Image(width=400, height=400, preset_colors=None)
    assert img


def test_asn2array():
    """
    check if it works when the right input is used
    """
    arr = asn2array([(1, 2), (3, 4), (5, 6)], dtype=np.intc)

    assert type(arr) == np.ndarray
    assert arr.shape == (3, 2)
    assert arr.dtype == np.intc


def test_asn2array_fail():
    """
    check if it fails when wrong imput is used
    """
    with pytest.raises(ValueError):
        _arr = asn2array([(1, 2, 3), (3, 4, 5), (5, 6, 7)], dtype=np.intc)  # noqa: F841

    with pytest.raises(ValueError):
        _arr = asn2array((1, 2, 3, 3, 4, 5, 5, 6, 7), dtype=np.intc)  # noqa: F841

    assert True


def test_cant_save_file():
    img = Image(width=400, height=400)

    with pytest.raises(OSError):
        img.save("a/non_existant/file_path")


def test_non_ascii_file_name():
    """
    Can use full Unicode on utf-8 filesystems only
    e.g. OS-X and most Linux

    Windows only supports ASCII at this point
    """
    img = Image(width=400, height=400)

    filename = outfile("file\u2014name_with_unicode.png")  # u2014 is an EmDash
    if sys.getfilesystemencoding() == 'utf-8':
        # this should work
        img.save(filename)
        assert filename.exists()
    else:
        # other filesystem encodings raise an Exception
        with pytest.raises(ValueError):
            img.save(filename)


def test_init_simple_add_rgb():
    """
    simplest possible initilization -- no preset color palette
    """
    img = Image(width=400, height=400, preset_colors=None)

    img.add_color('white', (255, 255, 255))


def test_init_simple_add_rgba():
    """
    simplest possible initilization -- no preset color palette
    """
    img = Image(width=400, height=400, preset_colors=None)

    img.add_color('white', (255, 255, 255, 127))


def test_init_default_colors():
    """
    Initialize with the default palette
    """
    img = Image(width=400, height=300)

    colors = img.get_color_names()
    assert len(colors) == 17


def test_init_BW():
    img = Image(10, 10, preset_colors='BW')
    colors = img.get_color_names()
    assert len(colors) == 3


def test_init2():
    _img = Image(width=400, height=400)

    _img = Image(400, 400)  # noqa: F841

    # need to pass in width and height
    with pytest.raises(TypeError):
        Image()

    with pytest.raises(TypeError):
        Image(200)


def test_mem_limit():
    """
    test the limit for largest image.

    note that the 1GB max is arbitrary -- youc an change it iin the code.

    But my system, at least, will try to allocate much more memory that
    you'd want, bringing the system to an almost halt, before raising
    a memory error, so I sete a limit.
    """
    _img = Image(32768, 32768)  # 1 GB image

    with pytest.raises(MemoryError):
        # > 1 GB image
        _img = Image(32768, 32769)    # noqa: F841


def test_set_size():
    """
    you should not be able to set the size or width or height
    """
    img = Image(40, 30)

    assert img.size == (40, 30)
    assert img.height == 30
    assert img.width == 40

    with pytest.raises(AttributeError):
        img.size = (50, 60)

    with pytest.raises(AttributeError):
        img.height = 100

    with pytest.raises(AttributeError):
        img.width = 100


def test_info():
    img = Image(400, 300)

    assert str(img) == "py_gd.Image: width: 400, height: 300"
    assert repr(img) == "Image(width=400, height=300)"


def test_get_color_indices():
    img = Image(10, 10, preset_colors='xkcd')

    colors = img.get_color_indices(['white', 'lavender', 'aquamarine'])

    assert np.array_equal(colors, np.array([1, 22, 54], dtype=np.uint8))


def test_add_colors():
    img = Image(10, 10, preset_colors='BW')

    assert img.get_color_names() == ['transparent', 'black', 'white']

    img.add_color('light grey', (220, 220, 220))

    assert img.get_color_names() == ['transparent', 'black', 'white',
                                     'light grey']
    assert img.get_color_index('light grey') == 3

    img.draw_rectangle((2, 2), (7, 7), fill_color='light grey')
    img.save(outfile('test_image_grey.bmp'))

    with pytest.raises(ValueError):
        # color doesn't exist
        img.draw_rectangle((2, 2), (7, 7), fill_color='red')


def test_add_colors_repeat():
    img = Image(10, 10, preset_colors='BW')

    index_1 = img.add_color('blue', (0, 0, 255))

    with pytest.raises(ValueError):
        # adding one with the same name should raise an exception
        img.add_color('blue', (0, 0, 200))

    # Adding the same color with a different name:
    # adds another index -- should it?
    index_2 = img.add_color('full_blue', (0, 0, 255))

    assert index_1 != index_2


def test_add_colors_max():
    img = Image(10, 10, preset_colors='BW')

    # should be able to add this many:
    for i in range(253):
        img.add_color("color_%i" % i, (i, i, i))

    # adding one more should raise an exception:
    with pytest.raises(ValueError):
        img.add_color("color_max", (10, 100, 200))


@pytest.mark.parametrize("filetype", ["bmp", "jpg", "gif", "png"])
def test_save_image(filetype):
    img = Image(400, 300)

    img.draw_line((0, 0), (399, 299), 'white', line_width=4)
    img.draw_line((0, 299), (399, 0), 'green', line_width=4)

    fname = "test_image_save." + filetype
    img.save(outfile(fname), filetype)

    if filetype != "jpg":  # jpeg is lossy and thus can be inconsistent
        assert check_file(fname)

    with pytest.raises(ValueError):
        img.save(outfile("test_image1.something"), "random_string")


def test_clear():
    img = Image(100, 200)

    # just to put something in there to clear.
    img.draw_rectangle((-10, -10), (50, 100), fill_color='red')
    img.draw_rectangle((50, 100), (110, 210), fill_color='blue')

    img.save(outfile("test_image_clear_before.png"), "png")

    img.clear()
    assert np.all(np.asarray(img).flat == 0)

    img.save(outfile("test_image_clear_after.png"), "png")
    assert check_file("test_image_clear_after.png")


def test_clear_color():
    img = Image(100, 200)

    # just to put something in there to clear.
    img.draw_rectangle((-10, -10), (50, 100), fill_color='red')
    img.draw_rectangle((50, 100), (110, 210), fill_color='blue')

    img.save(outfile("test_image_clear_before2.png"), "png")
    img.clear(color='white')
    img.save(outfile("test_image_clear_after2.png"), "png")

    assert np.all(np.asarray(img).flat == img.get_color_index('white'))


def test_line():
    img = Image(100, 200)

    img.draw_line((0, 0), (99, 199), 'white')
    img.draw_line((0, 199), (99, 0), 'red', line_width=2)
    img.draw_line((0, 100), (99, 100), 'green', line_width=4)
    img.draw_line((50, 0), (50, 199), 'blue', line_width=8)

    img.save(outfile("test_image_line.bmp"))
    assert check_file("test_image_line.bmp")

    with pytest.raises(TypeError):
        img.draw_line((0, 0), (99, 199), 'white', line_width='fred')


def test_line_clip():
    img = Image(100, 200)

    img.draw_line((-30, -10), (150, 250), 'white')
    img.save(outfile("test_image_line_clip.bmp"))


def test_SetPixel():
    img = Image(5, 5)

    img.draw_pixel((0, 0), 'white')
    img.draw_pixel((1, 1), 'red')
    img.draw_pixel((2, 2), 'green')
    img.draw_pixel((3, 3), 'blue')

    img.save(outfile("test_image_pixel.bmp"))
    assert check_file("test_image_pixel.bmp")


def test_GetPixel():
    img = Image(5, 5)

    img.draw_pixel((0, 0), 'white')
    img.draw_pixel((1, 1), 'red')
    img.draw_pixel((2, 2), 'green')
    img.draw_pixel((3, 3), 'blue')

    assert img.get_pixel_color((0, 0)) == 'white'
    assert img.get_pixel_color((1, 1)) == 'red'
    assert img.get_pixel_color((2, 2)) == 'green'
    assert img.get_pixel_color((3, 3)) == 'blue'


def test_Polygon1():
    img = Image(100, 200)

    points = ((10, 10),
              (20, 190),
              (90, 10),
              (50, 50))

    img.draw_polygon(points, 'red')
    img.save(outfile("test_image_poly1.bmp"))


def test_Polygon2():
    img = Image(100, 200)

    points = ((10, 10),
              (20, 190),
              (90, 10),
              (50, 50))

    img.draw_polygon(points, fill_color='blue')

    img.save(outfile("test_image_poly2.bmp"))


def test_Polygon3():
    img = Image(100, 200)

    points = ((10, 10),
              (20, 190),
              (90, 10),
              (50, 50))

    img.draw_polygon(points, fill_color='blue', line_color='red', line_width=4)
    img.save(outfile("test_image_poly3.bmp"))


def test_polygon_clip():
    img = Image(100, 200)

    points = ((-20, 10),
              (20, 250),
              (120, 10),
              (50, 50))

    img.draw_polygon(points, fill_color='blue', line_color='red')
    img.save(outfile("test_image_polygon_clip.bmp"))


def test_polyline():
    img = Image(100, 200)

    points = ((10, 10),
              (20, 190),
              (90, 10),
              (50, 50))

    img.draw_polyline(points, 'red', line_width=3)

    points = ((50, 50),
              (90, 190),
              (10, 10))

    img.draw_polyline(points, 'blue', line_width=5)

    with pytest.raises(ValueError):
        # can't accept just one point
        img.draw_polyline(((10, 10),), 'blue')

    img.save(outfile("test_image_polyline.bmp"))


def test_rectangles():
    img = Image(100, 200)
#    print(img.get_color_names())
    img.clear('gray')

    img.draw_rectangle((10, 10), (30, 40), fill_color='blue')
    img.draw_rectangle((20, 50), (40, 70), line_color='blue', line_width=5)
    img.draw_rectangle((40, 80), (90, 220), fill_color='white',
                       line_color='green', line_width=2)

    img.save(outfile("test_image_rectangle.bmp"))


def test_arc():
    img = Image(400, 600)
    img.clear('gray')
    # possible flags:  "Arc", "Pie", "Chord", "NoFill", "Edged"
    # (Arc and Pie are the same)
    center = (200, 150)

    # just the lines
    img.draw_arc(center, 380, 280, start=-30, end=30, line_color='white',
                 style='arc', draw_wedge=False)
    img.draw_arc(center, 380, 280, start=30, end=90, line_color='white',
                 style='chord', draw_wedge=False, line_width=3)
    img.draw_arc(center, 380, 280, start=90, end=150, line_color='white',
                 style='arc', draw_wedge=True, line_width=5)
    img.draw_arc(center, 380, 280, start=150, end=210, line_color='white',
                 style='chord', draw_wedge=True)

    # just fill
    img.draw_arc(center, 380, 280, start=210, end=270, fill_color='purple',
                 style='arc')
    img.draw_arc(center, 380, 280, start=270, end=330, fill_color='teal',
                 style='chord')

    # line and fill
    center = (200, 450)

    img.draw_arc(center, 380, 280, start=30, end=90, line_color='white',
                 fill_color='green', style='chord')
    # img.draw_arc(center, 380, 280, start= 90, end= 150, line_color='white',
    #              fill_color='blue', styles=['NoFill'])
    img.draw_arc(center, 380, 280, start=150, end=210, line_color='green',
                 fill_color='white', style='arc')
    # img.draw_arc(center, 380, 280, start=210, end= 270, line_color='white',
    #              fill_color='purple', styles=['Chord','Edged', 'NoFill'])
    img.draw_arc(center, 380, 280, start=270, end=330, line_color='blue',
                 fill_color='red', line_width=3)

    img.save(outfile("test_image_arc.bmp"))

    # errors
    with pytest.raises(ValueError):
        img.draw_arc(center, 380, 280, start=30, end=90, line_color='white',
                     style='fred')

    assert check_file("test_image_arc.bmp")


def test_circle():
    img = Image(400, 400, preset_colors='web')
    img.clear('white')

    # just the outline: upper left
    center = (100, 100)
    img.draw_circle(center, diameter=100, line_color='black', line_width=2)

    # just the fill: lower left
    center = (100, 300)
    img.draw_circle(center, diameter=100, fill_color='teal')

    # fill and outline: Upper right
    center = (300, 100)
    img.draw_circle(center,
                    diameter=100,
                    fill_color='red',
                    line_color='green',
                    line_width=4)

    # fat outline: Lower right
    center = (300, 300)
    img.draw_circle(center,
                    diameter=150,
                    line_color='green',
                    line_width=8)

    img.save(outfile("test_image_circle.bmp"))

    assert check_file("test_image_circle.bmp")


def test_ellipse():
    img = Image(400, 400, preset_colors='web')
    img.clear('white')

    # just the outline: upper left
    center = (100, 100)
    w, h = 120, 60
    img.draw_ellipse(center,
                     width=w,
                     height=h,
                     line_color='black',
                     line_width=2)

    # just the fill: lower left
    center = (100, 300)
    w, h = 60, 120
    img.draw_ellipse(center,
                     width=w,
                     height=h,
                     fill_color='teal')

    # fill and outline: Upper right
    center = (300, 100)
    w, h = 60, 80
    img.draw_ellipse(center,
                     width=w,
                     height=h,
                     fill_color='red',
                     line_color='green',
                     line_width=4)

    # fat outline: Lower right
    center = (300, 300)
    w, h = 80, 60
    img.draw_ellipse(center,
                     width=w,
                     height=h,
                     line_color='green',
                     line_width=8)

    img.save(outfile("test_image_ellipse.bmp"))

    assert check_file("test_image_ellipse.bmp")


def test_text():
    img = Image(200, 200)

    img.draw_text("Some Tiny Text", (20, 20), font="tiny", color='white')
    img.draw_text("Some Small Text", (20, 40), font="small", color='white')
    img.draw_text("Some Medium Text", (20, 60), font="medium", color='white')
    img.draw_text("Some Large Text", (20, 80), font="large", color='white')
    img.draw_text("Some Giant Text", (20, 100), font="giant", color='white')

    img.save(outfile("test_image_text.bmp"), "bmp")

    assert check_file("test_image_text.bmp")


def test_text_align():
    img = Image(200, 200)

    img.draw_text("abcd", (0, 0), font="tiny", color='white')
    img.draw_text("abcd", (100, 0), font="small", color='white', align='ct')
    img.draw_text("abcd", (200, 0), font="medium", color='white', align='rt')
    img.draw_text("abcd", (200, 100), font="large", color='white', align='r')
    img.draw_text("abcd", (200, 200), font="tiny", color='white', align='rb')
    img.draw_text("abcd", (100, 200), font="small", color='white', align='cb')
    img.draw_text("abcd", (0, 200), font="medium", color='white', align='lb')
    img.draw_text("abcd", (0, 100), font="large", color='white', align='l')

    img.save(outfile("test_text_align.bmp"), "bmp")


def test_text_background():
    img = Image(200, 200)

    img.draw_text("abcd", (0, 0), font="tiny", color='white')
    img.draw_text("abcd", (100, 0), font="small", color='white', align='ct')
    img.draw_text("abcd", (200, 0), font="medium", color='white', align='rt',
                  background='red')
    img.draw_text("abcd", (200, 100), font="large", color='white', align='r')
    img.draw_text("abcd", (200, 200), font="tiny", color='white', align='rb')
    img.draw_text("abcd", (100, 200), font="small", color='white', align='cb',
                  background='green')
    img.draw_text("abcd", (0, 200), font="medium", color='white', align='lb')
    img.draw_text("abcd", (0, 100), font="large", color='white', align='l')
    img.draw_text("9999", (0, 0), font="tiny", color='white')
    img.draw_text("9999", (100, 0), font="small", color='red', align='ct')
    img.draw_text("9999", (200, 0), font="medium", color='white', align='rt',
                  background='red')
    img.draw_text("9999", (200, 100), font="large", color='blue', align='r')
    img.draw_text("9999", (200, 200), font="tiny", color='white', align='rb')
    img.draw_text("9999", (100, 200), font="small", color='white', align='cb',
                  background='green')
    img.draw_text("9999", (0, 200), font="medium", color='white', align='lb')
    img.draw_text("9999", (0, 100), font="large", color='white', align='l')

    img.save(outfile("test_text_background.bmp"), "bmp")


def test_draw_dot():
    img = Image(100, 100,)

    img.draw_dot((10, 10))
    img.draw_dot((20, 20), diameter=2, color='black')
    img.draw_dot((30, 30), diameter=3, color='red')
    img.draw_dot((40, 0), diameter=4, color='blue')
    img.draw_dot((50, 50), diameter=6, color='aqua')
    img.draw_dot((60, 60), diameter=8, color='lime')
    img.draw_dot((70, 70), diameter=10, color='fuchsia')
    img.draw_dot((80, 80), diameter=15, color='purple')

    img.save(outfile("test_image_dot.png"), "png")


def test_draw_dots():
    img = Image(20, 20)

    img.draw_dots(((2, 2),
                   (2, 18),
                   (10, 10)))

    img.draw_dots(((18, 18),
                   (18, 2)),
                  diameter=2,
                  color='red')

    img.save(outfile("test_image_points.png"), "png")


def test_draw_dots3():
    img = Image(20, 20)

    img.draw_dots(((2, 2),
                   (2, 18),
                   (10, 10)),
                  diameter=3)

    img.draw_dots(((18, 18),
                   (18, 2)),
                  diameter=4,
                  color='red')

    img.save(outfile("test_image_points3.png"), "png")


def test_draw_dots_large():
    img = Image(200, 200)

    img.draw_dots(((5, 5),),
                  diameter=3,
                  color='red')

    img.draw_dots(((15, 15),),
                  diameter=4,
                  color='red')

    img.draw_dots(((25, 25),),
                  diameter=5,
                  color='red')

    img.draw_dots(((35, 35),),
                  diameter=6,
                  color='red')

    img.draw_dots(((45, 45),),
                  diameter=7,
                  color='red')

    img.draw_dots(((55, 55),),
                  diameter=9,
                  color='red')

    img.draw_dots(((65, 65),),
                  diameter=12,
                  color='red')

    img.draw_dots(((80, 80),),
                  diameter=15,
                  color='red')

    img.draw_dots(((100, 100),),
                  diameter=20,
                  color='red')

    img.draw_dots(((120, 120),),
                  diameter=30,
                  color='red')

    img.draw_dots(((65, 65),),
                  diameter=12,
                  color='red')

    img.save(outfile("test_image_dots_large.png"), "png")


def test_draw_dots_lots():
    """
    test drawing a lot of dots
    """
    import random
    w, h, = 1000, 500
    img = Image(w, h)

    points = [(random.randint(0, w), random.randint(0, w))
              for _i in range(10000)]

    img.draw_dots(points, diameter=2, color='red')

    img.save(outfile("test_image_dots_lots.png"), 'png')


def test_draw_dots_multi_named_colors():
    """
    test drawing a lot of dots
    """
    w, h, = 500, 500
    img = Image(w, h, preset_colors='xkcd')

    points = [(x, y) for x in range(0, w, 50) for y in range(0, h, 50)]

    # print(points)
    colors = [img.get_color_names()[i+1] for i in range(len(points))]

    # colors =
    img.draw_dots(points, diameter=10, color=colors)

    img.save(outfile("test_draw_dots_multi_named_colors.png"), 'png')

    assert check_file("test_draw_dots_multi_named_colors.png")


def test_draw_dots_multi_color_indices():
    """
    test drawing a lot of dots
    """
    w, h, = 500, 500
    img = Image(w, h, preset_colors='xkcd')

    points = [(x, y) for x in range(0, w, 25) for y in range(0, h, 25)]

    colors = [i % 255 for i in range(len(points))]

    img.draw_dots(points, diameter=10, color=colors)

    img.save(outfile("test_draw_dots_multi_color_indices.png"), 'png')

    assert check_file("test_draw_dots_multi_color_indices.png")


def test_draw_dots_wrong_shape():
    """
    test passing in a wrong-shaped points
    """
    w, h, = 1000, 500
    img = Image(w, h)

    points = [(1, 2, 3),
              (4, 5, 6),
              (7, 8, 9),
              (10, 11, 12)]

    with pytest.raises(ValueError):
        img.draw_dots(points, diameter=2, color='red')

    assert True


def test_draw_x_lots():
    """
    test drawing a lot of dots
    """
    import random
    w, h, = 1000, 500
    img = Image(w, h)

    points = [(random.randint(0, w), random.randint(0, w))
              for _i in range(1000)]

    img.draw_xes(points, diameter=2, color='red')

    img.save(outfile("test_image_x_lots.png"), 'png')


def test_draw_x_large():
    img = Image(200, 200)

    img.draw_xes(((5, 5),),
                 diameter=3,
                 color='red')

    img.draw_xes(((15, 15),),
                 diameter=4,
                 color='red')

    img.draw_xes(((25, 25),),
                 diameter=5,
                 color='purple')

    img.draw_xes(((35, 35),),
                 diameter=6,
                 color='red')

    img.draw_xes(((45, 45),),
                 diameter=7,
                 color='red')

    img.draw_xes(((55, 55),),
                 diameter=9,
                 color='green')

    img.draw_xes(((65, 65),),
                 diameter=12,
                 color='red',
                 line_width=2)

    img.draw_xes(((80, 80),),
                 diameter=15,
                 color='blue',
                 line_width=3)

    img.draw_xes(((100, 100),),
                 diameter=20,
                 color='fuchsia',
                 line_width=4)

    img.draw_xes(((120, 120),),
                 diameter=30,
                 color='red',
                 line_width=5)

    img.draw_xes(((160, 160),),
                 diameter=40,
                 color='red',
                 line_width=10)

    img.save(outfile("test_image_x_large.png"), "png")


def test_colors():
    img = Image(5, 5)

    # this shold work
    img.get_color_index('black')

    # so should this:
    img.get_color_index(0)
    img.get_color_index(255)

    # will round floating point numbers
    # should this be changed?
    assert img.get_color_index(2.3) == 2

    with pytest.raises(ValueError):
        # error if index not in 0--255
        img.get_color_index(300)

    with pytest.raises(ValueError):
        # error if color is not in dict
        img.get_color_index('something else')

    with pytest.raises(TypeError):
        # error if color is not a number
        img.get_color_index((1, 2, 3))

    with pytest.raises(TypeError):
        # error if color is unhasable
        img.get_color_index(['a', 'random', 4])


def test_array():
    img = Image(10, 5)

    img.draw_line((0, 0), (9, 4), 'black', line_width=1)
    print("result from __array__", img.__array__())

    arr = np.asarray(img)
    assert np.array_equal(arr, [[1, 0, 0, 0, 0],
                                [1, 0, 0, 0, 0],
                                [0, 1, 0, 0, 0],
                                [0, 1, 0, 0, 0],
                                [0, 0, 1, 0, 0],
                                [0, 0, 1, 0, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 1],
                                [0, 0, 0, 0, 1]])


def test_set_pixel_value():
    """
    test if setting the pixel value directly works.
    """
    img = Image(4, 5)

    for i in range(4):
        for j in range(5):
            img.set_pixel_value((i, j), i)

    # check:
    for i in range(4):
        for j in range(5):
            assert img.get_pixel_value((i, j)) == i


def test_array_set():
    arr = np.array([[0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [9, 10, 11]],
                   dtype=np.uint8,
                   order='f')

    img = Image(arr.shape[0], arr.shape[1], preset_colors='web')

    img.set_data(arr)

    img.save(outfile('test_image_array1.bmp'))

    # print(img.get_color_names())

    for i in range(4):
        for j in range(3):
            print(img.get_pixel_color((i, j)), end=' ')
            print(img.get_pixel_value((i, j)))

    for y in range(img.height):
        for x in range(img.width):
            assert arr[x, y] == img.get_pixel_value((x, y))


def test_array_creation():
    arr = np.array([[0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [9, 10, 11]],
                   dtype=np.uint8,
                   order='c')

    img = from_array(arr)

    img.save(outfile('test_image_array2.bmp'))

    for y in range(img.height):
        for x in range(img.width):
            assert arr[x, y] == img.get_pixel_value((x, y))


def test_copy1():
    """
    test copying a full image
    """
    img1 = Image(5, 5)
    img2 = Image(5, 5)

    img1.draw_pixel((0, 0), 'white')
    img1.draw_pixel((1, 1), 'red')
    img1.draw_pixel((2, 2), 'green')
    img1.draw_pixel((3, 3), 'blue')
    img1.draw_pixel((4, 4), 'gray')

    img2.copy(img1)

    img2.save(outfile("image_copy.bmp"))

    assert np.array_equal(np.array(img1), np.array(img2))


def test_copy2():
    """
    test copying parts of an image
    """
    img1 = Image(10, 10)
    img2 = Image(10, 10)

    img1.draw_rectangle((1, 1), (8, 8), fill_color='red')
    img2.draw_rectangle((0, 0), (9, 9), fill_color='blue')

    img2.copy(img1, (3, 3), (3, 3), (4, 4))

    img1.save(outfile("image_copy_middle1.bmp"))
    img2.save(outfile("image_copy_middle2.bmp"))


def test_copy_ul():
    """
    test copying parts of an image
    """
    img1 = Image(10, 10)
    img2 = Image(10, 10)

    img1.draw_rectangle((1, 1), (8, 8), fill_color='red')
    img2.draw_rectangle((0, 0), (9, 9), fill_color='blue')

    img2.copy(img1, (0, 0), (7, 7), (4, 4))

    img2.save(outfile("image_copy_upper_left.bmp"))


def test_copy_transparent():
    """
    test copying parts of an image that are transparent
    """
    img1 = Image(10, 10)
    img2 = Image(10, 10)

    img1.draw_rectangle((0, 0), (9, 9), fill_color='red')
    img1.draw_rectangle((2, 2), (7, 7), fill_color='transparent')
    img2.draw_rectangle((0, 0), (9, 9), fill_color='blue')

    img2.copy(img1, (0, 0), (7, 7), (4, 4))

    img2.save(outfile("image_copy_trans.png"), file_type="png")


def test_equality():
    """
    test that an image is equal to itself and an identical image
    """
    img1 = Image(10, 10)
    img2 = Image(10, 10)
    img3 = Image(10, 11)

    img1.draw_rectangle((1, 1), (8, 8), fill_color='red')
    img2.draw_rectangle((1, 1), (8, 8), fill_color='red')
    img3.draw_rectangle((1, 1), (8, 8), fill_color='blue')

    assert img1 == img1
    assert img1 == img2
    assert img1 != img3
    assert (img1 == img3) is False


def test_size():
    """
    test the size property
    """
    img = Image(10, 15)

    assert img.size == (10, 15)


# Some tests of Clipping
def test_clip_getter():
    img1 = Image(100, 100)

    assert img1.clip_rect == ((0, 0), (99, 99))


def test_clip_setter():
    img1 = Image(100, 100)

    img1.clip_rect = ((20, 20), (79, 79))

    assert img1.clip_rect == ((20, 20), (79, 79))


def test_clip_deleter():
    img = Image(100, 100)

    # set to a non-default
    img.clip_rect = ((20, 20), (79, 79))

    assert img.clip_rect == ((20, 20), (79, 79))

    # delete it
    del img.clip_rect

    # it should be re-set to the image size.
    assert img.clip_rect == ((0, 0), (img.width - 1, img.height - 1))


def test_clip_draw():
    img = Image(100, 100)

    img.clip_rect = ((20, 20), (80, 80))

    img.draw_line((0, 0), (100, 100), color='red', line_width=4)
    img.draw_line((0, 100), (100, 0), color='blue', line_width=4)

    fname = "image_clip.bmp"
    img.save(outfile(fname))

    assert check_file(fname)


def rotating_line(size=200):
    """
    generate the endpoints of a rotating line

    for use in animation tests

    it's expecting to be used in a square image:

    (size,size)
    """
    endpoints = np.array(((-size / 2, 0), (size / 2, 0)))
    offset = np.array((size / 2, size / 2))

    for ang in range(0, 360, 10):
        rad = np.deg2rad(ang)
        rot_matrix = [(np.cos(rad), np.sin(rad)), (-np.sin(rad), np.cos(rad))]
        points = np.dot(endpoints, rot_matrix).astype(np.int32) + offset
        yield points


def test_animation():
    img = Image(200, 200)

    anim = Animation(outfile("test_animation.gif"))

    anim.begin_anim(img, 0)

    for points in rotating_line(200):
        img.draw_line(points[0], points[1], 'red')
        anim.add_frame(img)

    img.draw_line(np.array((0, 100)), np.array((200, 100)), 'green')
    anim.add_frame(img)

    anim.close_anim()

    # not much to auto-check here
    print(f"{anim.frames_written} frames were written")
    assert anim.frames_written == 22


def test_static_animation():
    """
    If subsequent frames are identical, then it should add tot he delay,
    rather than adding duplicate images

    Not sure how to actually test the delay, but looking at the animation
    you can tell it's slower than the previous test one, which is otherwise
    the same
    """
    img1 = Image(200, 200)
    img2 = Image(200, 200)

    anim = Animation(outfile("test_animation_static.gif"))
    anim.begin_anim(img1, 0)

    for points in rotating_line(200):
        img1.draw_line(points[0], points[1], 'red')
        img2.draw_line(points[0], points[1], 'red')

        assert img1 == img2

        anim.add_frame(img1)
        anim.add_frame(img2)

    anim.close_anim()
    print(f"{anim.frames_written} frames were written")
    # duplicate images should have added to delay, rather than adding an image
    assert anim.frames_written == 21


def test_animation_reuse_filename():
    """
    make an animation, then make another one with the same filename

    The final one should be green lines

    NOTE: we were having issues on Windows with permissions
    """

    for color in ('red', 'green'):
        img = Image(200, 200)

        anim = Animation(outfile("test_animation_reuse.gif"))
        anim.begin_anim(img, 0)

        for points in rotating_line(200):
            img.draw_line(points[0], points[1], color, line_width=3)
            anim.add_frame(img)
        anim.close_anim()

    # not much to auto-check here
    print(f"{anim.frames_written} frames were written")
    assert anim.frames_written == 21


def test_animation_reuse_filename_not_close():
    """
    make an animation, then make another one with the same filename

    The final one should be blue lines

    NOTE: we were having issues on Windows with permissions
    """

    for color in ('red', 'blue'):
        img = Image(200, 200)

        anim = Animation(outfile("test_animation_reuse_not_close.gif"))
        anim.begin_anim(img, 0)

        for points in rotating_line(200):
            img.draw_line(points[0], points[1], color, line_width=3)
            anim.add_frame(img)
        # anim.close_anim()

    # not much to auto-check here
    print(f"{anim.frames_written} frames were written")
    assert anim.frames_written == 21


def test_animation_reset_new_filename():
    """
    create an animation, then reset and make another one
    """
    anim = Animation(outfile("test_animation_reset1.gif"))
    img = Image(200, 200)

    anim.begin_anim(img, 0)

    for points in rotating_line(200):
        img.draw_line(points[0], points[1], 'red', line_width=3)
        anim.add_frame(img)

    assert anim.frames_written == 21

    anim.reset(file_path=outfile("test_animation_reset2.gif"))
    assert anim.frames_written == 0

    img = Image(300, 300)
    anim.begin_anim(img, 0)

    for points in rotating_line(300):
        img.draw_line(points[0], points[1], 'blue', line_width=3)
        anim.add_frame(img)

    anim.close_anim()

    # not much to auto-check here
    print(f"{anim.frames_written} frames were written")
    assert anim.frames_written == 21


def test_animation_reset_same_filename():
    """
    create an animation, then reset and make another one
    using the same filename (by default)
    """
    anim = Animation(outfile("test_animation_reset_same.gif"))
    img = Image(200, 200)

    anim.begin_anim(img, 0)

    for points in rotating_line(200):
        img.draw_line(points[0], points[1], 'red', line_width=3)
        anim.add_frame(img)

    assert anim.frames_written == 21

    anim.reset()
    assert anim.frames_written == 0

    img = Image(300, 300)
    anim.begin_anim(img, 0)

    for points in rotating_line(300):
        img.draw_line(points[0], points[1], 'blue', line_width=3)
        anim.add_frame(img)

    anim.close_anim()

    # not much to auto-check here
    print(f"{anim.frames_written} frames were written")
    assert anim.frames_written == 21


def test_animation_delete_before_use():
    """
    make sure the dealloc doesn't barf if the file hasn't
    been opened yet
    """

    filename = outfile("nothing.gif")

    filename.unlink(missing_ok=True)
    assert not filename.exists()

    anim = Animation(filename)
    del anim
    assert not filename.exists()

    # note: this creates a broken gif
    anim = Animation(filename)
    img = Image(200, 200)
    anim.begin_anim(img, 0)
    del anim
    assert filename.exists()


def test_animation_delete_one_frame():
    """
    make sure the dealloc creates a valid gif with only one frame added
    """
    filename = outfile("one_frame_delete.gif")
    anim = Animation(filename)
    img = Image(200, 200)
    anim.begin_anim(img, 0)
    img.draw_line((0, 0), (200, 200), color="white", line_width=4)
    anim.add_frame(img)
    del anim

    assert filename.exists()
