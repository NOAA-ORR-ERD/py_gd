#!/usr/bin/env python
"""
unit tests for Animation features of py_gd

designed to be run with pytest:
"""

import sys
import hashlib
from pathlib import Path
import numpy as np

import pytest

from py_gd import Image, Animation, asn2array, from_array  # noqa: F821
from py_gd.color_ramp import ColorRamp

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
         'test_animation.gif': '3abc5d1963116b1a05701978b048ac8a',
         'test_animation_reset1.gif': 'a53e5aaebcf441f002927b913c12f213',
         'test_animation_reset2.gif': 'ec5961189acd876f73f8132707f13c82',
         'test_animation_reset_same.gif': 'ec5961189acd876f73f8132707f13c82',
         'test_animation_reuse.gif': 'a45117a3d17f1093d5e395fcc20e69e1',
         'test_animation_reuse_not_close.gif': '7587576ac36cd0e2e8bcd8ee4ff52b82',
         'test_animation_static.gif': '4639911d250a50f9a76a24bb23031921',
        }

    cs = hashlib.md5(open(outfile(name), 'rb').read()).hexdigest()
    if checksums[name] == cs:
        return True
    else:
        print("Checksum did not match for file:", name)
        return False

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

    fname = "test_animation.gif"
    img = Image(200, 200)

    anim = Animation(outfile(fname))

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

    # should check checksum!
    assert check_file(fname)


def test_animation_multi_images_colors():
    """
    check that animation works with a new image every time

    and different colors!
    """
    # Initial frame:
    first_frame = Image(200, 200)

    existing_colors = first_frame.get_color_names()

    print(existing_colors)

    cr = ColorRamp('inferno', 0, 36, base_colorscheme=len(existing_colors))
    first_frame.add_colors(cr.colorlist)

    # Initial frame:
    anim = Animation(outfile("test_animation_multi_colors.gif"))

    anim.begin_anim(first_frame, 0)

    count = 0
    for points in rotating_line(200):
        color = cr.get_color_indices([count])[0]
        next_frame = Image(200, 200)
        next_frame.draw_line(points[0], points[1], color)
        anim.add_frame(next_frame)
        count += 1

    last_frame = Image(200, 200)
    last_frame.draw_line(np.array((0, 100)), np.array((200, 100)), 'green')
    anim.add_frame(last_frame)
    count += 1

    print(f"total frames written: {count}")

    anim.close_anim()

    # not much to auto-check here
    print(f"{anim.frames_written} frames were written")
    assert anim.frames_written == count

    # should check the checksum



def test_static_animation():
    """
    If subsequent frames are identical, then it should add to the delay,
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
