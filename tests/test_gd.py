#!/usr/bin/env python

"""
unit tests for the py_gd project

designed to be run with pytest:

py.test test_gd.py

"""



def outfile(file_name):
  # just to make it a little easier to type..
  output_dir = "./test_images_output"
  if not os.path.exists(output_dir):
      os.mkdir(output_dir)
  return os.path.join(output_dir, file_name)

import os
import pytest
import numpy as np
import py_gd

# def test_filenames():
#     """just to see what the output dir is.."""
#     print "output dir:", outfile("")
#     print "CWD:", os.getcwd()
#     assert False


def test_init_simple():
    """
    simplest possible initilization -- no preset color palette
    """
    img = py_gd.Image(width=400,
                      height=400,
                      preset_colors=None)

def test_cant_save_file():
    img = py_gd.Image(width=400,
                      height=400
                      )
    with pytest.raises(IOError):
        img.save("a/non_existant/file_path")


def test_init_simple_add_rgb():
    """
    simplest possible initilization -- no preset color palette
    """
    img = py_gd.Image(width=400,
                      height=400,
                      preset_colors=None)

    img.add_color('white', (255, 255, 255))

def test_init_simple_add_rgba():
    """
    simplest possible initilization -- no preset color palette
    """
    img = py_gd.Image(width=400,
                      height=400,
                      preset_colors=None)

    img.add_color('white', (255, 255, 255, 127))


def test_init_default_colors():
    """
    Initialize with the default palette
    """
    img = py_gd.Image(width=400, height=300)

def test_init_BW():
    img = py_gd.Image(10, 10, preset_colors='BW')

def test_init2():
    img = py_gd.Image(width=400, height=400)

    img = py_gd.Image(400, 400)

    ## need to pass in width and height
    with pytest.raises(TypeError):
        py_gd.Image()
    with pytest.raises(TypeError):
        py_gd.Image(200)

def test_mem_limit():
    """
    test the limit for largest image.

    note that the 1GB max is arbitrary -- youc an change it iin the code.

    But my system, at least, will try to allocate much more memory that
    you'd want, bringing the system to an almost halt, before raising
    a memory error, so I sete a limit.
    """
    img = py_gd.Image(32768, 32768) # 1 GB image

    with pytest.raises(MemoryError):
        img = py_gd.Image(32768, 32769) # > 1 GB image

def test_set_size():
    """
    you should not be able to set the size or width or height
    """
    img = py_gd.Image(40, 30)

    assert img.size == (40,30)
    assert img.height == 30
    assert img.width == 40

    with pytest.raises(AttributeError):
        img.size = (50, 60)
    with pytest.raises(AttributeError):
            img.height = 100
    with pytest.raises(AttributeError):
            img.width = 100



def test_info():
    img = py_gd.Image(400, 300)

    assert  str(img) == "py_gd.Image: width:400 and height:300"

    assert repr(img) == "Image(width=400, height=300)"

def test_add_colors():
    img = py_gd.Image(10, 10, preset_colors='BW')

    assert img.get_color_names() == ['transparent', 'black', 'white']

    img.add_color('light grey', (220,220,220) )
    assert img.get_color_names() == ['transparent', 'black', 'white', 'light grey']
    assert img.get_color_index('light grey') == 3

    img.draw_rectangle((2,2), (7,7), fill_color='light grey')
    img.save(outfile('test_image_grey.bmp'))

    with pytest.raises(ValueError):
        # color doesn't exist
        img.draw_rectangle((2,2), (7,7), fill_color='red')


def test_add_colors_repeat():
    img = py_gd.Image(10, 10, preset_colors='BW')

    index_1 = img.add_color('blue', (0, 0, 255))

    with pytest.raises(ValueError):
        # adding one with the same name should raise an exception
        img.add_color('blue', (0, 0, 200))

    # Adding the same color with a different name:
    # adds another index -- should it?
    index_2 = img.add_color('full_blue', (0, 0, 255))
    assert index_1 != index_2


def test_add_colors_max():
    img = py_gd.Image(10, 10, preset_colors='BW')

    # should be able to add this many:
    for i in range(253):
        img.add_color("color_%i"%i, (i, i, i) )

    # adding one more should raise an exception:
    with pytest.raises(ValueError):
        img.add_color("color_max", (10, 100, 200) )



@pytest.mark.parametrize("filetype", ["bmp","jpeg","gif","png"])
def test_save_image(filetype):
    img = py_gd.Image(400, 300)

    img.draw_line( (0,   0), (399, 299), 'white', line_width=4)
    img.draw_line( (0, 299), (399, 0), 'green', line_width=4)

    img.save(outfile("test_image_save"+filetype), filetype)

    with pytest.raises(ValueError):
        img.save(outfile("test_image1.something"), "random_string")

def test_clear():
    img = py_gd.Image(100,200)

    # just to put something in there to clear.
    img.draw_rectangle( (-10, -10), (50, 100), fill_color='red' )
    img.draw_rectangle( (50, 100), (110, 210), fill_color='blue' )

    img.save(outfile("test_image_clear_before.png"), "png")
    img.clear()
    img.save(outfile("test_image_clear_after.png"), "png")

    assert np.all(np.asarray(img).flat == 0)

def test_clear_color():
    img = py_gd.Image(100,200)

    # just to put something in there to clear.
    img.draw_rectangle( (-10, -10), (50, 100), fill_color='red' )
    img.draw_rectangle( (50, 100), (110, 210), fill_color='blue' )

    img.save(outfile("test_image_clear_before2.png"), "png")
    img.clear(color='white')
    img.save(outfile("test_image_clear_after2.png"), "png")

    assert np.all(np.asarray(img).flat == img.get_color_index('white'))



def test_line():
    img = py_gd.Image(100,200)

    img.draw_line( (0, 0), (99, 199), 'white')
    img.draw_line( (0, 199), (99, 0), 'red', line_width=2)
    img.draw_line( (0, 100), (99, 100), 'green', line_width=4)
    img.draw_line( (50, 0), (50, 199), 'blue', line_width=8)
    img.save(outfile("test_image_line.bmp"))

    with pytest.raises(TypeError):
        img.draw_line( (0, 0), (99, 199), 'white', line_width='fred')


def test_line_clip():
    img = py_gd.Image(100,200)

    img.draw_line( (-30, -10), (150, 250), 'white')
    img.save(outfile("test_image_line_clip.bmp"))


def test_SetPixel():
    img = py_gd.Image(5,5)

    img.draw_pixel( (0, 0), 'white')
    img.draw_pixel( (1, 1), 'red')
    img.draw_pixel( (2, 2), 'green')
    img.draw_pixel( (3, 3), 'blue')

    img.save(outfile("test_image_pixel.bmp"))

def test_GetPixel():
    img = py_gd.Image(5,5)

    img.draw_pixel( (0, 0), 'white')
    img.draw_pixel( (1, 1), 'red')
    img.draw_pixel( (2, 2), 'green')
    img.draw_pixel( (3, 3), 'blue')

    assert img.get_pixel_color( (0, 0) ) == 'white'
    assert img.get_pixel_color( (1, 1) ) == 'red'
    assert img.get_pixel_color( (2, 2) ) == 'green'
    assert img.get_pixel_color( (3, 3) ) == 'blue'

def test_Polygon1():
    img = py_gd.Image(100,200)

    points = ( ( 10,  10),
               ( 20, 190),
               ( 90,  10),
               ( 50,  50),
              )

    img.draw_polygon( points, 'red')
    img.save(outfile("test_image_poly1.bmp"))

def test_Polygon2():
    img = py_gd.Image(100,200)

    points = ( ( 10,  10),
               ( 20, 190),
               ( 90,  10),
               ( 50,  50),
              )

    img.draw_polygon( points, fill_color='blue')


    img.save(outfile("test_image_poly2.bmp"))

def test_Polygon3():
    img = py_gd.Image(100,200)

    points = ( ( 10,  10),
               ( 20, 190),
               ( 90,  10),
               ( 50,  50),
              )

    img.draw_polygon( points, fill_color='blue',line_color='red', line_width=4)
    img.save(outfile("test_image_poly3.bmp"))

def test_polygon_clip():
    img = py_gd.Image(100,200)

    img = py_gd.Image(100,200)

    points = ( ( -20,  10),
               ( 20, 250),
               ( 120,  10),
               ( 50,  50),
              )

    img.draw_polygon( points, fill_color='blue',line_color='red')
    img.save(outfile("test_image_polygon_clip.bmp"))


def test_polyline():
    img = py_gd.Image(100,200)

    points = ( ( 10,  10),
               ( 20, 190),
               ( 90,  10),
               ( 50,  50),
              )

    img.draw_polyline( points, 'red', line_width=3)

    points = ( ( 50,  50),
               ( 90, 190),
               ( 10,  10),
              )

    img.draw_polyline( points, 'blue', line_width=5)

    with pytest.raises(ValueError):
        # can't accept just one point
        img.draw_polyline( ((10,10),), 'blue')

    img.save(outfile("test_image_polyline.bmp"))


def test_rectangles():
    img = py_gd.Image(100,200)

    img.draw_rectangle( (10,10), (30,40), fill_color='blue')
    img.draw_rectangle( (20,50), (40,70), line_color='blue', line_width=5)
    img.draw_rectangle( (40,80), (90,220), fill_color='white',line_color='green', line_width=2)
    img.save(outfile("test_image_rectangle.bmp"))

def test_arc():
    img = py_gd.Image(400,600)
    # possible flags:  "Arc", "Pie", "Chord", "NoFill", "Edged" (Arc and Pie are the same)
    center = (200, 150)
    # just the lines

    img.draw_arc( center, 380, 280, start=-30, end= 30, line_color='white', style='arc',   draw_wedge=False)
    img.draw_arc( center, 380, 280, start= 30, end= 90, line_color='white', style='chord', draw_wedge=False, line_width=3)
    img.draw_arc( center, 380, 280, start= 90, end=150, line_color='white', style='arc',   draw_wedge=True, line_width=5)
    img.draw_arc( center, 380, 280, start=150, end=210, line_color='white', style='chord', draw_wedge=True)

    # just fill
    img.draw_arc( center, 380, 280, start=210, end= 270, fill_color='purple', style='arc')
    img.draw_arc( center, 380, 280, start=270, end= 330, fill_color='teal', style='chord')

    # line and fill
    center = (200, 450)

    img.draw_arc( center, 380, 280, start= 30, end= 90, line_color='white', fill_color='green', style='chord')
    #img.draw_arc( center, 380, 280, start= 90, end= 150, line_color='white', fill_color='blue', styles=['NoFill'])
    img.draw_arc( center, 380, 280, start=150, end= 210, line_color='green', fill_color='white', style='arc')
    # img.draw_arc( center, 380, 280, start=210, end= 270, line_color='white', fill_color='purple', styles=['Chord','Edged', 'NoFill'])
    img.draw_arc( center, 380, 280, start=270, end= 330, line_color='blue', fill_color='red', line_width=3)

    img.save(outfile("test_image_arc.bmp"))

    #errors
    with pytest.raises(ValueError):
        img.draw_arc( center, 380, 280, start= 30, end= 90, line_color='white', style='fred')


def test_text():
    img = py_gd.Image(200, 200)


    img.draw_text("Some Tiny Text", (20, 20), font="tiny", color='white')
    img.draw_text("Some Small Text", (20, 40), font="small", color='white')
    img.draw_text("Some Medium Text", (20, 60), font="medium", color='white')
    img.draw_text("Some Large Text", (20, 80), font="large", color='white')
    img.draw_text("Some Giant Text", (20, 100), font="giant", color='white')
    img.save(outfile("test_image_text.png"), "png")

def test_draw_dot():
    img = py_gd.Image(100, 100, )

    img.draw_dot( (10,10) )

    img.draw_dot( (20,20), diameter=2, color='black' )

    img.draw_dot( (30,30), diameter=3, color='red' )

    img.draw_dot( (40,40), diameter=4, color='blue' )

    img.draw_dot( (50,50), diameter=6, color='aqua' )

    img.draw_dot( (60,60), diameter=8, color='lime' )

    img.draw_dot( (70,70), diameter=10, color='fuchsia' )

    img.draw_dot( (80,80), diameter=15, color='purple' )

    img.save(outfile("test_image_dot.png"), "png")


def test_draw_dots():
    img = py_gd.Image(20, 20)

    img.draw_dots( ( (2, 2),
                       (2, 18),
                       (10,10)
                      )
                    )

    img.draw_dots( ( (18, 18),
                       (18, 2),
                      ),
                      diameter=2,
                      color='red'
                    )

    img.save(outfile("test_image_points.png"), "png")

def test_draw_dots3():
    img = py_gd.Image(20, 20)

    img.draw_dots( ( (2, 2),
                       (2, 18),
                       (10,10)
                      ),
                      diameter = 3
                    )

    img.draw_dots( ( (18, 18),
                       (18, 2),
                      ),
                      diameter=4,
                      color='red'
                    )

    img.save(outfile("test_image_points3.png"), "png")

def test_draw_dots_large():
    img = py_gd.Image(200, 200)

    img.draw_dots( ((5, 5),),
                      diameter = 3,
                      color='red',
                    )

    img.draw_dots( ((15, 15),),
                      diameter = 4,
                      color='red',
                    )

    img.draw_dots( ((25, 25),),
                      diameter = 5,
                      color='red',
                    )

    img.draw_dots( ((35, 35),),
                      diameter = 6,
                      color='red',
                    )

    img.draw_dots( ((45, 45),),
                      diameter = 7,
                      color='red',
                    )

    img.draw_dots( ((55, 55),),
                      diameter = 9,
                      color='red',
                    )

    img.draw_dots( ((65, 65),),
                      diameter = 12,
                      color='red',
                    )

    img.draw_dots( ((80, 80),),
                      diameter = 15,
                      color='red',
                    )

    img.draw_dots( ((100, 100),),
                      diameter = 20,
                      color='red',
                    )

    img.draw_dots( ((120, 120),),
                      diameter = 30,
                      color='red',
                    )

    img.draw_dots( ((65, 65),),
                      diameter = 12,
                      color='red',
                    )

    img.save(outfile("test_image_dots_large.png"), "png")

def test_draw_dots_lots():
    """
    test drawing a lot of dots
    """
    import random
    w, h, = 1000, 500
    img = py_gd.Image(w, h)

    points = [ (random.randint(0,w), random.randint(0,w)) for i in range(10000) ]

    img.draw_dots(points, diameter=2, color = 'red')

    img.save(outfile("test_image_dots_lots.png"), 'png')

def test_draw_x_lots():
    """
    test drawing a lot of dots
    """
    import random
    w, h, = 1000, 500
    img = py_gd.Image(w, h)

    points = [ (random.randint(0,w), random.randint(0,w)) for i in range(1000) ]

    img.draw_xes(points, diameter=2, color = 'red')

    img.save(outfile("test_image_x_lots.png"), 'png')



def test_draw_x_large():
    img = py_gd.Image(200, 200)

    img.draw_xes( ((5, 5),),
                      diameter = 3,
                      color='red',
                    )

    img.draw_xes( ((15, 15),),
                      diameter = 4,
                      color='red',
                    )

    img.draw_xes( ((25, 25),),
                      diameter = 5,
                      color='purple',
                    )

    img.draw_xes( ((35, 35),),
                      diameter = 6,
                      color='red',
                    )

    img.draw_xes( ((45, 45),),
                      diameter = 7,
                      color='red',
                    )

    img.draw_xes( ((55, 55),),
                      diameter = 9,
                      color='green',
                    )

    img.draw_xes( ((65, 65),),
                  diameter = 12,
                  color='red',
                  line_width=2,
                    )

    img.draw_xes( ((80, 80),),
                  diameter = 15,
                  color='blue',
                  line_width=3,
                    )

    img.draw_xes( ((100, 100),),
                  diameter = 20,
                  color='fuchsia',
                  line_width=4,
                    )

    img.draw_xes( ((120, 120),),
                  diameter = 30,
                  color='red',
                  line_width=5,
                    )

    img.draw_xes( ((160, 160),),
                  diameter = 40,
                  color='red',
                  line_width=10,
                  )

    img.save(outfile("test_image_x_large.png"), "png")


def test_colors():
    img = py_gd.Image(5, 5)

    # this shold work
    img.get_color_index('black')

    # so should this:
    img.get_color_index(0)
    img.get_color_index(255)

    # will round floating point numbers
    # shoul dthi sbe changed?
    assert img.get_color_index(2.3) == 2

    with pytest.raises(ValueError):
        # error if index not in 0--255
        img.get_color_index(300)

    with pytest.raises(ValueError):
        # error if color is not in dict
        img.get_color_index('something else')

    with pytest.raises(ValueError):
        # error if color is not anumber
        img.get_color_index((1,2,3))

    with pytest.raises(TypeError):
        # error if color is unhasable
        img.get_color_index(['a', 'random', 4])



def test_array():
    img = py_gd.Image(10, 5)
    img.draw_line( (0, 0), (9, 4), 'black', line_width=1)
    print "result from __array__", img.__array__()
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
                                [0, 0, 0, 0, 1]]
                          )

def test_set_pixel_value():
    """
    test if setting the pixel value directly works.
    """
    img = py_gd.Image(4, 5)
    for i in range(4):
        for j in range(5):
            img.set_pixel_value( (i, j), i)

    #check:
    for i in range(4):
        for j in range(5):
            assert img.get_pixel_value( (i,j) ) == i


def test_array_set():
    arr = np.array( [[ 0, 1, 2],
                     [ 3, 4, 5],
                     [ 6, 7, 8],
                     [ 9, 10, 11] ],
                     dtype=np.uint8,
                     order='f')

    img = py_gd.Image(arr.shape[0], arr.shape[1], preset_colors='web')
    img.set_data(arr)

    img.save(outfile('test_image_array1.bmp'))

    print img.get_color_names()
    for i in range(4):
        for j in range(3):
            print img.get_pixel_color( (i,j) ),
            print img.get_pixel_value( (i,j) )


    for y in range(img.height):
        for x in range(img.width):
            assert arr[x,y] == img.get_pixel_value( (x,y) )


def test_array_creation():
    arr = np.array( [[ 0,  1,  2],
                     [ 3,  4,  5],
                     [ 6,  7,  8],
                     [ 9, 10, 11] ],
                     dtype=np.uint8,
                     order='c')

    img = py_gd.from_array(arr)

    img.save(outfile('test_image_array2.bmp'))

    for y in range(img.height):
        for x in range(img.width):
            assert arr[x,y] == img.get_pixel_value( (x,y) )

def test_copy1():
    """
    test copying a full image
    """
    img1 = py_gd.Image(5,5)

    img2 = py_gd.Image(5,5)

    img1.draw_pixel( (0, 0), 'white')
    img1.draw_pixel( (1, 1), 'red')
    img1.draw_pixel( (2, 2), 'green')
    img1.draw_pixel( (3, 3), 'blue')
    img1.draw_pixel( (4, 4), 'gray')

    img2.copy(img1)

    img2.save(outfile("image_copy.bmp"))

    assert np.array_equal(np.array(img1), np.array(img2))

def test_copy2():
    """
    test copying parts of an image
    """
    img1 = py_gd.Image(10,10)
    img2 = py_gd.Image(10,10)

    img1.draw_rectangle( (1,1), (8,8), fill_color='red' )
    img2.draw_rectangle( (0,0), (9,9), fill_color='blue' )

    img2.copy(img1, (3,3), (3,3), (4,4))

    img1.save(outfile("image_copy_middle1.bmp"))
    img2.save(outfile("image_copy_middle2.bmp"))


def test_copy_ul():
    """
    test copying parts of an image
    """
    img1 = py_gd.Image(10,10)
    img2 = py_gd.Image(10,10)

    img1.draw_rectangle( (1,1), (8,8), fill_color='red' )
    img2.draw_rectangle( (0,0), (9,9), fill_color='blue' )

    img2.copy(img1, (0,0), (7,7), (4,4))

    img2.save(outfile("image_copy_upper_left.bmp"))

def test_copy_transparent():
    """
    test copying parts of an image that are transparent
    """
    img1 = py_gd.Image(10,10)
    img2 = py_gd.Image(10,10)


    img1.draw_rectangle( (0,0), (9,9), fill_color='red' )
    img1.draw_rectangle( (2,2), (7,7), fill_color='transparent' )
    img2.draw_rectangle( (0,0), (9,9), fill_color='blue' )

    img2.copy(img1, (0,0), (7,7), (4,4))

    img2.save(outfile("image_copy_trans.png"), file_type="png")

def test_size():

    """
    test the size property
    """
    img = py_gd.Image(10, 15)

    assert img.size == (10, 15)





if __name__ == "__main__":
    # just run these tests..
    #test_init_default_palette()
    #test_init_BW()
    #test_init_simple_add_rgb()
    test_init_simple_add_rgba()



