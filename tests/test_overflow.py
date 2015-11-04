#!/usr/bin/env python

"""
tests for overflow in py_gd code

what happens when you use large coordinates? well outside the image?

It fails to properly fill polygons even when teh coords are well less than what
can fit in a 32 bit int. -- it seems as thoough there is a multiplication in
play -- the limit is around the square root of a max int.

"""
import math
import numpy as np
import py_gd
import pytest



class TestLine():
    # line drawing -- all seems to work fine

    # Create a sample array to test against
    img = py_gd.Image(10, 10)
    img.draw_line( (0, 0), (10, 10), 'white', line_width=2)
    # save this one as an array
    line_arr = np.array(img)

    def test_inside(self):
        '''just to make sure the comparing is working'''
        img = py_gd.Image(10, 10)
        img.draw_line( (0, 0), (10, 10), 'white', line_width=2)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.line_arr)

    def test_outside(self):
        '''second value too large'''
        img = py_gd.Image(10, 10)
        img.draw_line( (0, 0), (100, 100), 'white', line_width=2)
        # save this as an array
        arr = np.array(img)
        assert np.array_equal(arr, self.line_arr)


    def test_negative(self):
        '''negative coords value too large'''
        img = py_gd.Image(10, 10)
        img.draw_line( (-100, -100), (10, 10), 'white', line_width=2)
        # save this as an array
        arr = np.array(img)
        assert np.array_equal(arr, self.line_arr)


    def test_big(self):
        '''
        really big values, negative and positive

        but not quite enough to overflow an integer
        '''

        img = py_gd.Image(10, 10)
        val = int(2**30)
        img.draw_line( (-val, -val), (val, val), 'white', line_width=2)
        # save this as an array
        arr = np.array(img)
        assert np.array_equal(arr, self.line_arr)

    def test_overflow(self):
        '''
        Big enough to overflow an 32 bit int
        '''

        img = py_gd.Image(10, 10)
        val = int(2**33)
        with pytest.raises(OverflowError):
            img.draw_line( (-val, -val), (val, val), 'white', line_width=2)

class TestPolyLine():
    # polygon drawing -- with just a line

    # Create a sample array to test against
    img = py_gd.Image(10, 10)
    points = ((-1,-1),(11,11),(-1,11))# a traingle that divides the image
    img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)
    # save this one as an array
    arr = np.array(img)

    def test_inside(self):
        '''just to make sure the comparing is working'''
        img = py_gd.Image(10, 10)
        points = ((-1,-1),(11,11),(-1,11))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_outside(self):
        '''second value too large'''
        img = py_gd.Image(10, 10)
        points = ((-1,-1),(100,100),(-1,100))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)


    def test_negative(self):
        '''negative coords value too large'''
        img = py_gd.Image(10, 10)
        points = ((-100,-100),(10,10),(-100,10))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)


    def test_big(self):
        '''
        really big values, negative and positive

        but not quite enough to overflow an integer
        '''

        img = py_gd.Image(10, 10)
        val = int(2**30)
        points = ((-val,-val),(val,val),(-val,val))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_overflow(self):
        '''
        Big enough to overflow an 32 bit int
        '''

        img = py_gd.Image(10, 10)
        val = int(2**33)
#        with pytest.raises(OverflowError):
#            img.draw_line( (-val, -val), (val, val), 'white', line_width=2)
        points = ((-val,-val),(val,val),(-val,val))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color=None, line_width=1)
        # save this one as an array
        arr = np.array(img)

        # This isn't expect to draw correctly
        assert not np.array_equal(arr, self.arr)

class TestPolyFill():
    # polygon drawing -- with just a line

    # Create a sample array to test against
    img = py_gd.Image(10, 10)
    points = ((-1,-1),(11,11),(-1,11))# a traingle that divides the image
    img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
    # save this one as an array
    arr = np.array(img)

    def test_inside(self):
        '''just to make sure the comparing is working'''
        img = py_gd.Image(10, 10)
        points = ((-1,-1),(11,11),(-1,11))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_outside(self):
        '''second value too large'''
        img = py_gd.Image(10, 10)
        points = ((-1,-1),(100,100),(-1,100))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)


    def test_negative(self):
        '''negative coords value too large'''
        img = py_gd.Image(10, 10)
        points = ((-100,-100),(10,10),(-100,10))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    @pytest.mark.xfail # this is giving an overflow problem -- only on fill
    def test_huge(self):
        '''
        really big values, negative and positive

        but not quite enough to overflow an integer
        '''

        img = py_gd.Image(10, 10)
        val = int(2**30)
        points = ((-val,-val),(val,val),(-val,val))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_large(self):
        '''
        large values, negative and positive

        just less than sqrt(max_int32)

        this seems to confirm that that's the limit
        '''

        img = py_gd.Image(10, 10)
        val = int(2**14)
        points = ((-val,-val),(val,val),(-val,val))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        assert np.array_equal(arr, self.arr)

    def test_too_large(self):
        '''
        large values, negative and positive

        just more than sqrt(max_int32)

        this seems to confirm that that's the limit
        '''

        img = py_gd.Image(10, 10)
        val = int(2**15)
        points = ((-val,-val),(val,val),(-1,val))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        ## this is expected to not be equal -- we've found a too-big value
        assert not np.array_equal(arr, self.arr)


    def test_overflow(self):
        '''
        Big enough to overflow an 32 bit int
        '''

        img = py_gd.Image(10, 10)
        val = int(2**33)
#        with pytest.raises(OverflowError):
#            img.draw_line( (-val, -val), (val, val), 'white', line_width=2)
        points = ((-val,-val),(val,val),(-val,val))# a triangle that divides the image
        img.draw_polygon(points, line_color='black', fill_color='red', line_width=1)
        # save this one as an array
        arr = np.array(img)

        # This isn't expect to draw correctly
        assert not np.array_equal(arr, self.arr)
