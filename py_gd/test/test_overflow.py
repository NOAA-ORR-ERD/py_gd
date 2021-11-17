#!/usr/bin/env python
"""
tests for overflow in py_gd code

what happens when you use large coordinates? well outside the image?

It fails to properly fill polygons even when teh coords are well less than what
can fit in a 32 bit int. -- it seems as thoough there is a multiplication in
play -- the limit is around the square root of a max int.
"""
import numpy as np

import pytest

from py_gd import Image


class TestLine():
    # line drawing -- all seems to work fine

    # Create a sample array to test against
    img = Image(10, 10)
    img.draw_line((0, 0), (10, 10), 'white', line_width=2)

    # save this one as an array
    line_arr = np.array(img)

    def test_inside(self):
        '''just to make sure the comparing is working'''
        img = Image(10, 10)
        img.draw_line((0, 0), (10, 10), 'white', line_width=2)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.line_arr)

    def test_outside(self):
        '''second value too large'''
        img = Image(10, 10)
        img.draw_line((0, 0), (100, 100), 'white', line_width=2)

        # save this as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.line_arr)

    def test_negative(self):
        '''negative coords value too large'''
        img = Image(10, 10)
        img.draw_line((-100, -100), (10, 10), 'white', line_width=2)

        # save this as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.line_arr)

    def test_big(self):
        '''
        really big values, negative and positive, but not quite enough
        to overflow an integer
        '''
        img = Image(10, 10)
        val = int(2 ** 30)

        img.draw_line((-val, -val), (val, val), 'white', line_width=2)

        # save this as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.line_arr)

    def test_overflow(self):
        '''
        Big enough to overflow an 32 bit int
        '''
        img = Image(10, 10)
        val = int(2 ** 33)

        with pytest.raises(OverflowError):
            img.draw_line((-val, -val), (val, val), 'white', line_width=2)


class TestPolyLine():
    # polygon drawing -- with just a line

    # Create a sample array to test against
    img = Image(10, 10)

    # a triangle that divides the image
    points = ((-1, -1), (11, 11), (-1, 11))

    img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)

    # save this one as an array
    arr = np.array(img)

    def test_inside(self):
        '''just to make sure the comparing is working'''
        img = Image(10, 10)

        # a triangle that divides the image
        points = ((-1, -1), (11, 11), (-1, 11))

        img.draw_polygon(points, line_color='black', fill_color=None,
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_outside(self):
        '''second value too large'''
        img = Image(10, 10)

        # a triangle that divides the image
        points = ((-1, -1), (100, 100), (-1, 100))

        img.draw_polygon(points, line_color='black', fill_color=None,
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_negative(self):
        '''negative coords value too large'''
        img = Image(10, 10)

        # a triangle that divides the image
        points = ((-100, -100), (10, 10), (-100, 10))

        img.draw_polygon(points, line_color='black', fill_color=None,
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_big(self):
        '''
        really big values, negative and positive

        but not quite enough to overflow an integer
        '''
        img = Image(10, 10)
        val = int(2 ** 30)

        # a triangle that divides the image
        points = ((-val, -val), (val, val), (-val, val))

        img.draw_polygon(points, line_color='black', fill_color=None,
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_overflow(self):
        '''
        Big enough to overflow an 32 bit int
        '''
        img = Image(10, 10)
        val = int(2**33)

        # a triangle that divides the image
        points = ((-val, -val), (val, val), (-val, val))

        try:
            img.draw_polygon(points, line_color='black', fill_color=None,
                             line_width=1)
        except OverflowError:
            # Windows raises on overflow -- at least on the conda-forge CI
            assert True
        else:
            img.draw_polygon(points, line_color='black', fill_color=None,
                             line_width=1)
            # save this one as an array
            arr = np.array(img)
            # This isn't expect to draw correctly
            assert not np.array_equal(arr, self.arr)


class TestPolyFill():
    # polygon drawing -- with just a line

    # Create a sample array to test against
    img = Image(10, 10)

    # a traingle that divides the image
    points = ((-1, -1), (11, 11), (-1, 11))

    img.draw_polygon(points, line_color='black', fill_color='red',
                     line_width=1)

    # save this one as an array
    arr = np.array(img)

    def test_inside(self):
        '''just to make sure the comparing is working'''
        img = Image(10, 10)

        # a triangle that divides the image
        points = ((-1, -1), (11, 11), (-1, 11))

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_outside(self):
        '''second value too large'''
        img = Image(10, 10)

        # a triangle that divides the image
        points = ((-1, -1), (100, 100), (-1, 100))

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_negative(self):
        '''negative coords value too large'''
        img = Image(10, 10)

        # a triangle that divides the image
        points = ((-100, -100), (10, 10), (-100, 10))

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    # this is giving an overflow problem -- only on fill
    def test_huge(self):
        '''
        really big values, negative and positive, but not quite enough
        to overflow an integer

        But apparently big enough to screw up the fill algorithm

        '''
        img = Image(10, 10)
        val = int(2 ** 30)

        # a triangle that divides the image
        points = ((-val, -val), (val, val), (-val, val))

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert not np.array_equal(arr, self.arr)

    def test_large(self):
        '''
        large values, negative and positive
        just less than sqrt(max_int32)
        this seems to confirm that that's the limit
        '''
        img = Image(10, 10)
        val = int(2 ** 14)

        # a triangle that divides the image
        points = ((-val, -val), (val, val), (-val, val))

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_too_large(self):
        '''
        large values, negative and positive
        just more than sqrt(max_int32)
        this seems to confirm that that's the limit
        '''
        img = Image(10, 10)
        val = int(2 ** 15)

        # a triangle that divides the image
        points = ((-val, -val), (val, val), (-1, val))

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)

        # this is expected to not be equal -- we've found a too-big value
        assert not np.array_equal(arr, self.arr)

    def test_multi_segment(self):
        '''
        what if we break it down into smaller segments?
        '''
        img = Image(10, 10)
        val = int(2 ** 30)  # should work

        coords = np.linspace(-val, val, 100000)
        rev_coords = np.flipud(coords)

        diag = np.c_[coords, coords]
        bottom = np.c_[rev_coords, np.ones_like(coords) * val]
        side = np.c_[np.ones_like(coords) * -val, rev_coords, ]
        points = np.r_[diag, bottom, side]

        img.draw_polygon(points, line_color='black', fill_color='red',
                         line_width=1)

        # save this one as an array
        arr = np.array(img)
        print(arr)
        print(self.arr)

        # this is expected to not be equal -- we've found a too-big value
        assert np.array_equal(arr, self.arr)

    def test_overflow(self):
        '''
        Big enough to overflow an 32 bit int
        '''
        img = Image(10, 10)
        val = int(2 ** 33)

        # a triangle that divides the image
        points = ((-val, -val), (val, val), (-val, val))

        # with pytest.raises(OverflowError):
        #     img.draw_line( (-val, -val), (val, val), 'white', line_width=2)


        try:
            img.draw_polygon(points, line_color='black', fill_color='red',
                             line_width=1)
        except OverflowError:
            # raises on overflow on Windows -- at least sometimes
            assert True
        else:
            img.draw_polygon(points, line_color='black', fill_color='red',
                             line_width=1)

            # save this one as an array
            arr = np.array(img)

            # This isn't expect to draw correctly
            assert not np.array_equal(arr, self.arr)
