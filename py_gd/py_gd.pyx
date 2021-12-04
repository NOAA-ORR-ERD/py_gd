"""
Cython wrapper around the gd drawing lib

Provides an OO interface -- at least to the limited functionality wrapped

NOTE: pixel coordinates are defined as c ints -- if you pass in values
      larger than a c int can take (usually +- 2**31 - 1), it will overflow,
      and who knows what you'll get.
"""

#cython: language_level=3

import cython
from cython cimport view

from py_gd cimport *

from libc.stdio cimport FILE, fopen, fclose
from libc.string cimport memcpy, strlen
from libc.stdlib cimport malloc, free

import os
import sys
import operator

import numpy as np
cimport numpy as cnp
from py_gd.colors import colorschemes

__gd_version__ = gdVersionString().decode('ascii')


# transparent_colors = [('transparent', (0, 0, 0, 127))]

# BW_colors = transparent_colors + [('black', (0,     0,  0)),
#                                   ('white', (255, 255, 255))]

# web_colors = BW_colors + [('silver',  (191, 191, 191)),
#                           ('gray',    (127, 127, 127)),
#                           ('red',     (255,   0,   0)),
#                           ('maroon',  (127,   0,   0)),
#                           ('yellow',  (255, 255,   0)),
#                           ('olive',   (127, 127,   0)),
#                           ('lime',    (0,   255,   0)),
#                           ('green',   (0,   127,   0)),
#                           ('aqua',    (0,   255, 255)),
#                           ('teal',    (0,   127, 127)),
#                           ('blue',    (0,     0, 255)),
#                           ('navy',    (0,     0, 127)),
#                           ('fuchsia', (255,   0, 255)),
#                           ('purple',  (127,   0, 127))]

# note that the 1GB max is arbitrary -- you can change it after import,
# before initializing an Image. On my system going bigger than this brings
# the system to an almost halt before raising a memory error, so I set
# a limit here.

MAX_IMAGE_SIZE = 2 ** 30  # 1 GB limit

cpdef cnp.ndarray[int, ndim=2, mode='c'] asn2array(obj, dtype):
    """
    converts the input object to an Nx2 array.

    returns the input if it is already an array,
    returns a new array if not.

    raises ValueError if the array is the wrong shape

    :param a: input obj -- should be something that can be converted to a
              Nx2 array

    :param dtype: the numpy data type you want the returned array to be
    """
    arr = np.asarray(obj, dtype)

    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError("input  must be convertible to a Nx2 array")

    return arr

cdef FILE* open_file(file_path) except *:
    """
    opens a file

    :param path: python str or PathLike

    :returns: File Pointer

    Note: On Windows, it uses a wchar, UTC-16 encoded
          On other platforms (Mac and Linux), it assumes utf-8
    """
    cdef FILE* fp

    file_path = os.fspath(file_path)

    fp = NULL

    IF UNAME_SYSNAME == 'Windows':
        fp = _wfopen(file_path, "wb")
    ELSE:
        fp = fopen(file_path.encode('utf-8'), 'wb')

    if fp is NULL:
        raise OSError('could not open the file: {}'.format(file_path))

    return fp


cdef class Image:
    """
    class wrapper  around a gdImage object
    """
    # cdef readonly unsigned int _width, _height

    cdef gdImagePtr _image
    cdef unsigned char * _buffer_array

    cdef list color_names
    cdef list color_rgb
    cdef dict colors

    def __cinit__(self, int width, int height, preset_colors='web'):
        # self._width  = width
        # self._height = height

        if width * height > MAX_IMAGE_SIZE:
            raise MemoryError("Can't create a byte image larger than {} "
                              "(arbitrary...)\n"
                              "This limit can be changed by setting "
                              "MAX_IMAGE_SIZE"
                              .format(MAX_IMAGE_SIZE))

        self._image = gdImageCreatePalette(width, height)
        if self._image is NULL:
            raise MemoryError("could not create a gdImage")

        # set the default clipping to the image
        gdImageSetClip(self._image, 0, 0, width - 1, height - 1)

    def __dealloc__(self):
        """
        deallocate the image
        """
        if self._image is not NULL:
            gdImageDestroy(self._image)
            self._image = NULL

    def __init__(self, width, height, preset_colors='web'):
        """
        create a new Image object

        :param width: width of image in pixels
        :type width: integer

        :param height: height of image in pixels
        :type height: integer

        :param preset_colors=web_colors: which set of preset colors you want.
                                         options are:

                                         'web' - the basic named colors for
                                                 the web: transparent
                                                 background

                                         'BW' - transparent, black, and white:
                                                transparent background

                                         'transparent' - transparent background,
                                                         no other colors set

                                         None - no pre-allocated colors -- the
                                                first one you allocate will be
                                                the background color or any of
                                                the colors in py_gd.colors

        :type preset_colors: string or None

        The Image is created as a 8-bit Paletted Image.

        """
        # NOTE: the initilization of the C structs is happening in the __cinit__

        # set first color (background) to transparent
        # initialize the colors
        self.colors = {}
        self.color_names = []

        if preset_colors is not None:
            try:
                self.add_colors(colorschemes[preset_colors])
            except KeyError:
                raise ValueError("preset_colors needs to one of None, 'web', "
                                 "'BW', 'transparent', or any of the colors in "
                                 "py_gd.colors")

        # elif preset_colors == 'transparent':
        #     self.add_colors(transparent_colors)
        # elif preset_colors == 'BW':
        #     self.add_colors(BW_colors)
        # elif preset_colors == 'web':
        #     self.add_colors(web_colors)
        # else:
        #     raise ValueError("preset_colors needs to one of 'web', 'BW', "
        #                      "'transparent', or None")

    def __str__(self):
        return ('py_gd.Image: width: {}, height: {}'
                .format(self.width, self.height))

    def __repr__(self):
        return ('Image(width={}, height={})'.format(self.width, self.height))

    property size:
        def __get__(self):
            return (gdImageSX(self._image), gdImageSY(self._image))

    property width:
        def __get__(self):
            return gdImageSX(self._image)

    property height:
        def __get__(self):
            return gdImageSY(self._image)

    def __richcmp__(Image self, Image other not None, int op):
        # Thanks for this madness, cython!
        cdef int retval = -1

        retval = gdImageCompare(self._image, other._image)

        if op == 2:  # ==
            return retval == 0
        elif op == 3:  # !=
            return retval > 0
        else:
            return NotImplemented

    def clear(self, color=None):
        """
        clear the image

        :param color=None: color to set the image to if None, it will be set
                           to the first color set (index 0)
        """
        # Note: is there a call in gd for this?
        if color is None:
            color = 0

        gdImageFilledRectangle(self._image,
                               0, 0,  # upper left
                               self.width, self.height,  # lower right
                               self.get_color_index(color))

    def add_color(self, name, color):
        """
        Add a new color to the palette

        :param name: The name of the color
        :type name: string

        :param color: The value of the color.
        :type color: 3-tuple of integers (r,g,b) or
                     4-tuple of integers (r, g, b, a).
                     Red, green, and blue values range from 0 to 255.
                     Alpha ranges from 0 to 127.

        :returns color_index: The index of that new color
        """
        # fixme: should it check if the same color is already in the palette?
        #        not just the name?
        if name in self.colors:
            raise ValueError('{} is already in the palette'.format(name))

        cdef int color_index

        if len(color) == 4:
            color_index = gdImageColorAllocateAlpha(self._image,
                                                    color[0], color[1],
                                                    color[2], color[3])
        elif len(color) == 3:
            color_index = gdImageColorAllocate(self._image,
                                               color[0], color[1], color[2])
        else:
            raise ValueError('color must be an (r,g,b) triple '
                             'or (r,g,b,a) quad')

        if color_index == -1:
            raise ValueError('there are no more colors available to allocate')

        self.colors[name] = color_index
        self.color_names.append(name)

        return color_index

    def add_colors(self, color_list):
        """
        Add a list of colors to the palette

        :param color_list: list of colors - each element of the list
                           is a 2-tuple: ('color_name', (r, g, b))

        :returns indexes: list of color indexes.
        """
        indexes = []

        for name, color in color_list:
            indexes.append(self.add_color(name, color))

        return indexes

    @cython.boundscheck(False)
    def __array__(self):
        """
        :returns arr: numpy array object with a copy of the data

        Note that the array is (width, height) in size, in keeping
        with image conventions, but not array conventions. data is
        in Fortran order
        """
        cdef cnp.ndarray[cnp.uint8_t, ndim=2, mode='fortran'] arr
        arr = np.zeros((self.width, self.height), dtype=np.uint8, order='F')

        cdef unsigned int row, col

        # copy the data, item by item (copying into columns)
        for col in range(self.height):
            memcpy(&arr[0, col], self._image.pixels[col], self.width)

        return arr

    def set_data(self, char[:, :] arr not None):
        """
        Set the contents of the image from the input array.

        array must be the right size and data type (np.uint8)

        Note that the array is (width, height) in size.

        """
        # print "f-contig:", arr.is_f_contig()
        # print "c-contig:", arr.is_c_contig()
        # print "memview flags are:", arr.flags
        if arr.shape[0] != self.width or arr.shape[1] != self.height:
            raise ValueError('input array must be of shape: (width, height), '
                             'and the same size as image')

        cdef unsigned int row, col

        # copy the data, item by item
        for row in range(self.height):
            for col in range(self.width):
                self._image.pixels[row][col] = arr[col, row]

    def copy(self, Image src_img,
             dst_corner=(0, 0),
             src_corner=(0, 0),
             size=None):
        """
        draw a rectangular section of another image on top of this one

        default is to copy the whole image

        :param src_img: image you want to copy from
        :type src_img: Image

        :param dst_corner: corner of rectangle to copy to
        :type dst_corner: (x,y) tuple of integers

        :param src_corner: corner of rectangle to copy from in source image
        :type src_corner: (x,y) tuple of integers

        :param size: size of recatngle to copy (width, height)
        :type size: (w, h) tuple of integers
        """
        size = (self.width, self.height) if size is None else size

        gdImageCopy(self._image, src_img._image,
                    dst_corner[0], dst_corner[1],
                    src_corner[0], src_corner[1],
                    size[0], size[1])

    # def __getbuffer__(self, Py_buffer* buffer, int flags):
    #     # attempt to use buffer interface instaed of numpy arrays...
    #     # didn't quite work
    #     print "__getbuffer__ called"

    #     #allocate the array:
    #     self._buffer_array = <unsigned char*> malloc(self.width*self.height)

    #     cdef unsigned char i
    #     for i in range(self.width*self.height):
    #         self._buffer_array[i] = i

    #     cdef Py_ssize_t shape[2]
    #     shape[0] = 5
    #     shape[1] = 10

    #     print "shape is:", shape[0], shape[1]
    #     #shape[0] = <Py_ssize_t> self.width
    #     #shape[1] = <Py_ssize_t> self.height

    #     buffer.buf = <char*> self._buffer_array
    #     buffer.obj = self
    #     buffer.len = self.width*self.height
    #     buffer.readonly = 0
    #     buffer.format = "B"
    #     buffer.ndim = 2
    #     buffer.shape = &shape[0]
    #     buffer.strides =  NULL # NULL for c-contiguous
    #     buffer.suboffsets = NULL # NULL for C-contiguous
    #     buffer.itemsize = 1
    #     buffer.internal = NULL # NULL for the ordinary case

    # def __releasebuffer__(self, Py_buffer* buffer):
    #     print "releasing buffer!"

    #     free(self._buffer_array)

    property clip_rect:
        """
        The clipping region for the image -- when set, Establishes a clipping
        rectangle.Once set, all future drawing operations will remain within
        the specified clipping area, until a new clip_rect is set.

        a clip rect is defined by the two corners::
                  ((x1, y1)
                   (x2, y2))

        For instance, if a clipping rectangle of ( (25, 25)  (75, 75) )
        has been set within a 100x100 image, a diagonal line from 0,0 to 99,99
        will appear only between 25,25 and 75,75.
        """
        def __get__(self):
            cdef int x1, y1, x2, y2

            gdImageGetClip(self._image, &x1, &y1, &x2, &y2)

            return ((x1, y1), (x2, y2))

        def __set__(self, value):
            cdef int x1, y1, x2, y2

            x1 = value[0][0]
            y1 = value[0][1]
            x2 = value[1][0]
            y2 = value[1][1]

            gdImageSetClip(self._image, x1, y1, x2, y2)

        def __del__(self):
            gdImageSetClip(self._image, 0, 0,
                           gdImageSX(self._image) - 1,
                           gdImageSY(self._image) - 1)

    # Saving images
    def save(self, file_name, file_type="bmp", compression=None):
        """
        save the image to disk file format options are:
        - "bmp"
        - "gif"
        - "png"
        - "jpeg"

        NOTE: these may not always be available, depending on how libgd
              was compiled. But bmp and gif should always be there.

        :param file_name: full or relative path to file you want created
        :type file_name: str or PathLike

        :param file_type: type of file you want written
        :type file_type: string
        """
        cdef FILE *fp
        cdef int compression_level

        file_type_codes = {"bmp", "jpg", "jpeg", "gif", "GIF", "png", "PNG"}

        if file_type not in file_type_codes:
            raise ValueError('file_type must be one of: {}'
                             .format(file_type_codes))

        fp = open_file(file_name)
        # open the file here:

        # then call the right writer:
        if file_type in ["bmp", "BMP"]:
            gdImageBmp(self._image, fp, 0)
        elif file_type in ("jpg", "jpeg"):
            compression_level = 80 if compression is None else compression

            gdImageJpeg(self._image, fp, compression_level)
        elif file_type in ("gif", "GIF"):
            gdImageGif(self._image, fp)
        elif file_type in ("png", "PNG"):
            gdImagePng(self._image, fp)
        else:
            raise ValueError('"bmp", "gif", "png", and "jpeg" are the only '
                             'valid values for file_type')

        fclose(fp)

        return None

    def get_color_names(self):
        """
        :returns color_names: a list of all color names in use
        """
        return self.color_names

    def get_color_index(self, color):
        """
        returns the color index for a named or integer color
        """
        cdef int c = 0

        try:
            c = self.colors[color]
        except KeyError:
            try:
                if 0 <= color <= 255:
                    c = color
                else:
                    raise ValueError('you must provide an integer between 0 and 255')
            except TypeError:  # not an int
                raise ValueError('you must provide an existing named color '
                                 )
        return c

    def get_pixel_color(self, point):
        """
        returns the string value for the color at a point

        :param point: the (x,y) coord you want the color of

        """
        cdef int c

        c = gdImageGetPixel(self._image, point[0], point[1])

        return self.color_names[c]

    def get_pixel_value(self, point):
        """
        returns the value (index into palette) of the pixel at a point

        :param point: the (x,y) coord you want the value of

        """
        return gdImageGetPixel(self._image, point[0], point[1])

    def set_pixel_value(self, point, value):
        """
        returns the value (index into palette) of the pixel at a point

        :param point: the (x,y) coord you want the value of

        """
        gdImageSetPixel(self._image, point[0], point[1], value)

    # The drawing functions:
    def draw_pixel(self, point, color='black'):
        """
        set the pixel at the point:(x,y) to the color

        :param point: (x, y coordinate of the pixel of interest)
        :type point: 2-tuple of integers (or other sequence)
        """
        gdImageSetPixel(self._image,
                        point[0], point[1],
                        self.get_color_index(color))

    def draw_dot(self, point, color='black', int diameter=1):
        """
        draw a dot (filled circle) at the point:(x,y)

        :param point: (x, y coordinate of the pixel of interest)
        :type point: 2-tuple of integers (or other sequence)

        :param color='black': color to draw the dot
        :type color: string colorname of color index

        :param diameter=1: diamter of the dot
        :type diameter: integer
        """
        cdef cnp.uint8_t c

        c = self.get_color_index(color)

        if diameter == 1:
            gdImageSetPixel(self._image, point[0], point[1], c)
        elif diameter == 2:  # draw four pixels
            gdImageSetPixel(self._image, point[0],     point[1], c)
            gdImageSetPixel(self._image, point[0] + 1, point[1], c)
            gdImageSetPixel(self._image, point[0],     point[1] + 1, c)
            gdImageSetPixel(self._image, point[0] + 1, point[1] + 1, c)
        elif diameter > 2:
            gdImageFilledArc(self._image,
                             point[0], point[1],
                             diameter, diameter,
                             0, 360,
                             c, gdArc)
        else:
            raise NotImplementedError("only diameters >= 1 are supported.")

    def draw_dots(self, points, color='black', int diameter=1):
        """
        Draws a set of individual dots all in the same color

        :param points: the (x,y) coordianates of the center of the dots
        :type points: a Nx2 numpy array of integers, or something that can be
                      turned in to one

        :param diameter=1: diameter of the dots in pixels.
        :type diameter: integer

        :param color='black': color of points
        :type  color: color name or index
        """
        cdef cnp.uint8_t c
        cdef cnp.uint32_t i, n
        cdef cnp.ndarray[int, ndim=2, mode='c'] points_arr

        points_arr = asn2array(points, dtype=np.intc)
        n = points_arr.shape[0]

        c = self.get_color_index(color)

        if diameter == 1:
            for i in range(n):
                gdImageSetPixel(self._image,
                                points_arr[i, 0], points_arr[i, 1],
                                c)
        elif diameter == 2:  # draw four pixels
            for i in range(n):
                gdImageSetPixel(self._image,
                                points_arr[i, 0], points_arr[i, 1],
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0]+1, points_arr[i, 1],
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0], points_arr[i, 1]+1,
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0]+1, points_arr[i, 1]+1,
                                c)
        elif diameter > 2:
            for i in range(n):
                gdImageFilledArc(self._image,
                                 points_arr[i, 0], points_arr[i, 1],
                                 diameter, diameter,
                                 0, 360,
                                 c, gdArc)
        else:
            raise NotImplementedError("only diameters >= 1 are supported.")

    def draw_xes(self, points, color='black',
                 int diameter=2, int line_width=1):
        """
        Draws a set of individual Xs all in the same color

        :param points: the (x,y) coordianates of the center of the dots
        :type points: a Nx2 numpy array of integers, or something that can be
                      turned in to one

        :param color='black': color of X
        :type  color: color name or index

        :param diameter=2: diameter of the X in pixels.
        :type diameter: integer

        :param line_width=1: width of line in pixels.
        :type diameter: integer
        """
        cdef int r
        cdef cnp.uint8_t c
        cdef cnp.uint32_t i, n
        cdef cnp.ndarray[int, ndim=2, mode='c'] points_arr

        points_arr = asn2array(points, dtype=np.intc)
        n = points_arr.shape[0]

        c = self.get_color_index(color)

        if diameter == 2:  # draw five pixels
            for i in range(n):
                gdImageSetPixel(self._image,
                                points_arr[i, 0], points_arr[i, 1],
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0] + 1, points_arr[i, 1] + 1,
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0] - 1, points_arr[i, 1] - 1,
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0] + 1, points_arr[i, 1] - 1,
                                c)
                gdImageSetPixel(self._image,
                                points_arr[i, 0] - 1, points_arr[i, 1] + 1,
                                c)
        elif diameter > 2:
            gdImageSetThickness(self._image, line_width)

            r = diameter // 2

            for i in range(n):
                gdImageLine(self._image,
                            points_arr[i, 0] - r, points_arr[i, 1] - r,
                            points_arr[i, 0] + r, points_arr[i, 1] + r,
                            c)
                gdImageLine(self._image,
                            points_arr[i, 0] - r, points_arr[i, 1] + r,
                            points_arr[i, 0] + r, points_arr[i, 1] - r,
                            c)

            gdImageSetThickness(self._image, 1)
        else:
            raise NotImplementedError("only diameters >= 2 are supported.")

    def draw_line(self, pt1, pt2, color, int line_width=1):
        """
        draw a line from pt1 to pt2

        :param pt1: (x,y) coordinates of start point
        :type pt1: (x,y) sequence of integers

        :param pt2: (x,y) coordinates of end point
        :type pt2: (x,y) sequence of integers

        :param color: color to draw the line

        :param line_width=1: width of line
        :type line_width: integer
        """
        gdImageSetThickness(self._image, line_width)

        gdImageLine(self._image,
                    pt1[0], pt1[1], pt2[0], pt2[1],
                    self.get_color_index(color))

        gdImageSetThickness(self._image, 1)

    def draw_polygon(self, points, line_color=None, fill_color=None,
                     int line_width=1):
        """
        Draw a polygon

        :param points: sequence of points
        :type points: Nx2 array of integers (or somethign that can be turned
                      into one)

        :param line_color=None: the color of the outline
        :type line_color=None:  color name or index

        :param fill_color=None: the color of the filled polygon
        :type  fill_color=None: color name or index

        :param line_width=1: width of line
        :type line_width: integer

        """
        cdef int n
        cdef cnp.ndarray[int, ndim=2, mode='c'] points_arr

        points_arr = asn2array(points, dtype=np.intc)
        n = points_arr.shape[0]

        if n < 3:
            raise ValueError('There must be at least three points specified '
                             'for a polygon')

        if fill_color is not None:
            gdImageFilledPolygon(self._image,
                                 <gdPointPtr> &points_arr[0, 0],
                                 n,
                                 self.get_color_index(fill_color))

        if line_color is not None:
            gdImageSetThickness(self._image, line_width)

            gdImagePolygon(self._image,
                           <gdPointPtr> &points_arr[0, 0],
                           n,
                           self.get_color_index(line_color))

            gdImageSetThickness(self._image, 1)

    def draw_polyline(self, points, line_color, int line_width=1):
        """
        Draw a polyline

        :param points: sequence of points
        :type points: Nx2 array of integers (or somethign that can be turned
                      into one)

        :param line_color=None: the color of the outline
        :type line_color=None:  color name or index

        :param fill_color=None: the color of the filled polygon
        :type  fill_color=None: color name or index

        :param line_width: width of the line to be drawn, in pixels
        :type line_width: integer
        """
        cdef int n
        cdef cnp.ndarray[int, ndim=2, mode='c'] points_arr

        points_arr = asn2array(points, dtype=np.intc)
        n = points_arr.shape[0]

        if n < 2:
            raise ValueError('There must be at least two points specified '
                             'for a polyline')

        if line_color is not None:
            gdImageSetThickness(self._image, line_width)

            gdImageOpenPolygon(self._image,
                               <gdPointPtr> &points_arr[0,0],
                               n,
                               self.get_color_index(line_color))

            gdImageSetThickness(self._image, 1)

    def draw_rectangle(self, pt1, pt2, line_color=None, fill_color=None,
                       int line_width=1):
        """
        Draw a rectangle

        :param pt1: upper left corner of rectangle
        :type pt1: (x,y) tuple or sequence of integers

        :param pt2: lower right corner of rectangle
        :type pt2: (x,y) tuple or sequence of integers

        :param fill_color=None: the color of the filled rectangle
        :type  fill_color=None: color name or index

        :param line_width=1: width of line
        :type line_width: integer
        """
        if fill_color is not None:
            gdImageFilledRectangle(self._image,
                                   pt1[0], pt1[1],
                                   pt2[0], pt2[1],
                                   self.get_color_index(fill_color))

        if line_color is not None:
            gdImageSetThickness(self._image, line_width)

            gdImageRectangle(self._image,
                             pt1[0], pt1[1],
                             pt2[0], pt2[1],
                             self.get_color_index(line_color))

            gdImageSetThickness(self._image, 1)

    def draw_arc(self, center, width, height,
                 start=0, end=0,
                 line_color=None, fill_color=None,
                 int line_width=1,
                 style='arc',
                 draw_wedge=True):
        """
        Draw a partial ellipse centered at the given point, with the specified
        width and height in pixels. The arc begins at the position in degrees
        specified by start and ends at the position specified by end.

        :param center: center of arc
        :type center: (x,y) tuple or 2-sequence of integers

        :param width: width of ellipse
        :type width: integer

        :param height: height of ellipse
        :type height: integer

        :param start: start of ellipse in degrees from ???
        :type start: integer

        :param end: end of ellipse in degrees from ???
        :type end: integer

        :param fill_color=None: the color of the filled portion of the ellipse
        :type  fill_color=None: color name or index

        :param line_color=None: the color of the outline
        :type  line_color=None: color name or index

        :param line_width=1: width of line
        :type line_width: integer

        :param style='arc': styles used to draw the arc.
                            Options are: 'arc' or 'chord'.
                            'arc' draws the rounded curve,
                            'chord' connects the start and end points
                            with a line.
        :type style: string

        :param draw_wedge=True: whether to draw the wedge of the slice,
                                or just the outer arc
        :type draw_wedge: bool

        Degrees increase clockwise, starting from the right (east)

        A circle can be drawn by beginning from 0 degrees and ending at 360
        degrees, with width and height being equal.
        End must be greater than start.
        Values greater than 360 are interpreted modulo 360.
        """
        # set up the style flag:
        if style == 'chord':
            flag = gdChord
        elif style == 'arc':
            flag = gdArc
        else:
            raise ValueError('style must be one of "arc" or "chord"')

        # filled arc:
        if fill_color is not None:
            gdImageFilledArc(self._image,
                             center[0], center[1],
                             width, height,
                             start, end,
                             self.get_color_index(fill_color),
                             flag)

        if line_color is not None:
            flag |= gdNoFill

            if draw_wedge:
                flag |= gdEdged

            gdImageSetThickness(self._image, line_width)

            gdImageFilledArc(self._image,
                             center[0], center[1],
                             width, height,
                             start, end,
                             self.get_color_index(line_color),
                             flag)

            gdImageSetThickness(self._image, 1)

    def draw_text(self, text, point, font="medium", color='black', align='lt',
                  background='none'):
        """
        draw some text

        :param text: the text to draw
        :type text: string (ascii only for now)

        :param point: Coordinates at which to draw the text.  The point is the
                      upper left corner of the text bounding box.
        :type point: 2-tuple of (x,y) integers

        :param font: Desired font -- gd built in fonts are one of:
                     ``{"tiny", "small", "medium", "large", "giant"}``
        :type font: string

        :param color: Color of text
        :type  color=None: color name or index

        :param align: The principal point that the text box references
        :type align: one of the following: ``{'lt', 'ct', 'rt', 'r',
                     'rb', 'cb', 'lb', 'l'}``

        :param background: The background color of the text box.
                           Default is 'none' (nothing is drawn)
        :type background: str: name of the color, or 'none'.
        """
        cdef text_bytes

        try:
            text_bytes = text.encode('ascii')
        except UnicodeEncodeError as err:
            raise ValueError("can only accept ascii text") from err

        cdef gdFontPtr gdfont

        if font == 'tiny':
            gdfont = gdFontTiny
        elif font == 'small':
            gdfont = gdFontSmall
        elif font == 'medium':
            gdfont = gdFontMediumBold
        elif font == 'large':
            gdfont = gdFontLarge
        elif font == 'giant':
            gdfont = gdFontGiant
        else:
            raise ValueError('font must be one of: "tiny", "small", "medium", '
                             '"large", and "giant"')

        cdef int text_width, text_height

        text_width = len(text) * gdfont.w
        text_height = gdfont.h

        offsets = {'lt': (0, 0),
                   'ct': (text_width / 2, 0),
                   'rt': (text_width, 0),
                   'r': (text_width, text_height / 2),
                   'rb': (text_width, text_height),
                   'cb': (text_width / 2, text_height),
                   'lb': (0, text_height),
                   'l': (0, text_height / 2)
                   }

        if align not in offsets.keys():
            raise ValueError('invalid text alignment indicator. '
                             'Valid ones are: {}'.format(offsets.keys()))

        if background != 'none':
            pt1 = (point[0] - offsets[align][0], point[1] - offsets[align][1])
            pt2 = (pt1[0] + text_width, pt1[1] + text_height)

            self.draw_rectangle(pt1, pt2, fill_color=background)

        gdImageString(self._image, gdfont,
                      point[0] - offsets[align][0],
                      point[1] - offsets[align][1],
                      text_bytes,
                      self.get_color_index(color))

        # if line_color is not None:
        #     gdImageArc(self._image,
        #                center[0], center[1],
        #                width, height,
        #                start, end,
        #                self.get_color_index(line_color)
        #                )


def from_array(char[:, :] arr not None, *args, **kwargs):
    """
    Create an Image from a numpy array, or other object that exposed
    the PEP 3118 buffer interface.

    The image is the same size as the input array, with the contents copied.

    :param arr: The input array, shape (width, height)
    :type arr: An array, or other PEP 3118 buffer compliant object.
               Should be 2-d, and of type np.unit8 ('B')

    Other parameters are passed on to the Image() constructor.

    """
    img = Image(arr.shape[0], arr.shape[1], *args, **kwargs)
    img.set_data(arr)

    return img


cdef class Animation:
    cdef Image cur_frame
    cdef int _cur_delay
    cdef Image prev_frame
    cdef int base_delay
    cdef FILE *_fp
    cdef int _has_begun
    cdef int _has_closed
    cdef int _frames_written
    cdef int _global_colormap
    cdef object _file_path

    def __cinit__(self, file_name, int delay=50, int global_colormap=1):
        """
        :param file_name: The name/file path of the animation that will be
                          saved
        :type file_name: str or PathLike object

        :param delay: the default delay between frames
        :type delay: int

        :param global_colormap=1: Whether to use a global colormap.
                                  If 1, the same colormap is used for
                                  all images in the animation. If 0,
                                  a new colormap is used for each frame.
        """

        self._fp = NULL
        self.base_delay = delay
        self._has_begun = 0
        self._has_closed = 0
        self._frames_written = 0
        self._cur_delay = delay
        self._global_colormap = global_colormap


    def __init__(self,  file_name, delay=50, global_colormap=1):
        """
        :param file_name: The name/file path of the animation that will be
                          saved
        :type file_name: path_like e.g. str or pathlib.Path

        :param delay: the default delay between frames
        :type delay: int

        :param global_colormap=1: Whether to use a global colormap.
                                  If 1, the same colormap is used for
                                  all images in the animation. If 0,
                                  a new colormap is used for each frame.
        """
        self._file_path = file_name
        self.cur_frame = None
        self.prev_frame = None

    def __dealloc__(self):
        """
        closes the file and file pointer if animation was started
        and not closed.

        also calls gdImageGifAnimEnd to hopefully result in a valid file.
        """
        if self._has_begun > 0:
            self.close_anim()

        if self._fp is not NULL:
            fclose(self._fp)
            self._fp = NULL

    def begin_anim(self, Image first, int loops=0):
        """
        Begins the animation. This creates the file pointer and infers size and
        palette information from the initial Image

        :param first: First frame of the animation.
                      Also determines palette and size
        :type first: Image

        :param loops: Specifies the looping behavior of the animation.
                      (0 -> loop, -1 -> no loop, n > 0 -> loop n times)
        :type loops: int
        """

        if self._has_begun == 1:
            raise RuntimeError('Animation has already been started')

        if self._has_closed == 1:
            raise RuntimeError('Cannot re-begin closed animation')
        self._fp = open_file(self._file_path)

        self.cur_frame = Image(first.width, first.height)
        self.cur_frame.copy(first)

        gdImageGifAnimBegin(self.cur_frame._image,
                            self._fp,
                            self._global_colormap,
                            loops)

        self._has_begun = 1

    def add_frame(self, Image image, int delay=-1):
        """
        Adds the image to the animation with the specified delay

        :param image: The image to be added.
        :type image: Image

        :param delay: The delay between the current frame and the next.
                      <1 reverts to default delay
        :type delay: int
        """
        if self._has_begun == 0:
            raise IOError('Cannot add frame to non-started animation')

        if self._has_closed == 1:
            raise IOError('Cannot add frame to closed animation')

        if self.cur_frame is None or image is None:
            raise IOError('Cannot add NULL image to animation')

        if delay < 1:
            delay = self.base_delay

        cdef gdImagePtr prev
        prev = NULL

        if self.cur_frame == image:
            # if next image is the same as the image in the queue,
            # just add to the delay and leave
            self._cur_delay += delay

            return
        else:
            if self.prev_frame is not None:
                prev = self.prev_frame._image
            # really wierd gd flag values!
            local_colormap = 0 if self._global_colormap == 1 else 1
            gdImageGifAnimAdd(self.cur_frame._image,
                              self._fp,
                              local_colormap,
                              0,
                              0,
                              self._cur_delay,
                              1,
                              prev)

            self.prev_frame = self.cur_frame

            self.cur_frame = Image(self.cur_frame.width, self.cur_frame.height)
            self.cur_frame.copy(image)

            self._cur_delay = delay

            self._frames_written += 1

    def close_anim(self):
        if self._has_begun == 0:

            raise RuntimeError("Cannot close animation that hasn't been "
                               "opened (begun)")

        cdef gdImagePtr prev

        if self._fp is not NULL:
            prev = NULL

            if self.prev_frame is not None:
                prev = self.prev_frame._image

            gdImageGifAnimAdd(self.cur_frame._image, self._fp,
                              0, 0, 0, self._cur_delay, 1, prev)

            gdImageGifAnimEnd(self._fp)

            fclose(self._fp)
            self._fp = NULL

        self._has_closed = 1

    def reset(self, file_path=None):
        """
        Resets the object state so it can be used again to create
        another animation

        NOTE: begin_anim needs to be called again

        :param file_path=None: filename of new animation. Will reuse existing
                               name if not specified
        :param file_path: pathlike
        """
        self.prev_frame = None

        if file_path is not None:
            self._file_path = file_path

        if self._fp is not NULL:
            fclose(self._fp)

        self._fp = NULL

        self.base_delay = 50
        self._has_begun = 0
        self._has_closed = 0
        self._frames_written = 0

    @property
    def frames_written(self):
        return self._frames_written


def animation_from_images(images, file_name, delay=50):
    a = Animation(file_name, delay)
    a.begin_anim(images[0])

    for img in images[1:]:
        a.add_frame(img)
    a.close_anim()
