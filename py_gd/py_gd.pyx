"""
Cython wrapper around the gd drawing lib

provides an OO interface -- at least to the limited functionality wrapped
"""

import cython

from py_gd cimport *

from libc.stdio cimport FILE, fopen, fclose
from libc.string cimport memcpy
from libc.stdlib cimport malloc, free

import operator

import numpy as np
cimport numpy as cnp

from cython cimport view

## basic named color set
##  http://en.wikipedia.org/wiki/Web_colors#HTML_color_names

transparent_colors = [('transparent', (  0,  0,  0, 127) ) ]

BW_colors = transparent_colors + [('black',       (  0,  0,  0) ),  
                                     ('white',       (255, 255, 255) ),
                                     ]

web_colors = BW_colors + [ ('silver', (191, 191, 191) ),
                              ('gray',   (127, 127, 127) ),
                              ('red',    (255,   0,   0) ),
                              ('maroon', (127,   0,   0) ),
                              ('yellow', (255, 255,   0) ),
                              ('olive',  (127, 127,   0) ),
                              ('lime',   (  0, 255,   0) ),
                              ('green',  (  0, 127,   0) ),
                              ('aqua',   (  0, 255, 255) ),
                              ('teal',   (  0, 127, 127) ),
                              ('blue',   (  0,   0, 255) ),
                              ('navy',   (  0,   0, 127) ),
                              ('fuchsia',(255,   0, 255) ),
                              ('purple', (127,   0, 127) ),
                              ]

## note that the 1GB max is arbitrary -- you can change it after import,
## before initizing an Image. On my system going bigger than this brings
## the system to an almost halt before raising a memory error, so I set
## a limit here.
MAX_IMAGE_SIZE = 1073741824 #1 GB limit

cdef class Image:
    """
    class wrapper  around a gdImage object
    """
    cdef readonly unsigned int width, height
    cdef gdImagePtr _image
    cdef unsigned char* _buffer_array

    cdef list color_names
    cdef list color_rgb
    cdef dict colors 

    def __cinit__(self,
                  int width,
                  int height,
                  preset_colors='web'):

        self.width = width
        self.height = height

        if width*height > MAX_IMAGE_SIZE: 
            raise MemoryError("Can't create a larger than 1GB image (arbitrary...)")
        self._image = gdImageCreatePalette(width, height)
        if self._image is NULL:
            raise MemoryError("could not create a gdImage")

    def __dealloc__(self):
        """
        deallocate the image
        """
        if self._image is not NULL:
            gdImageDestroy(self._image)

    def __init__(self, width, height, preset_colors='web'):
        """
        create a new Image object

        :param width: width of image in pixels
        :type width: integer

        :param height: height of image in pixels
        :type height: integer

        :param preset_colors=web_colors: which set of preset colors you want. options are:
                                         
                                         'web' - the basic named colors for the web: transparent background
                                         
                                         'BW' - transparent, black, and white: transparent background
                                         
                                         'transparent' - transparent background, no other colors set
                                         
                                         None - no pre-allocated colors -- the first one you allocate will be the background color 
        :type preset_colors: string or None

        The Image is created as a 8-bit Paletted Image.

        NOTE: the initilization of the C structs is happening in the __cinit__
        """
        # set first color (background) to transparent
        ## initilize the colors
        self.colors = {}
        self.color_names = []
        if preset_colors is None:
            pass
        elif preset_colors == 'transparent':
            self.add_colors(transparent_colors)
        elif preset_colors == 'BW':
            self.add_colors(BW_colors)
        elif preset_colors == 'web':
            self.add_colors(web_colors)
        else:
            raise ValueError("preset_colors needs to one of 'web', 'BW', 'transparent', or None")

    def add_color(self, name, color):
        """
        add a new color to the palette

        :param name: the name of the color
        :type name: string 

        :param color: red, green, blue values for color - 0 to 255 or red, grenn, blue, alpha values (note: alpha is 0-127)
        :type color: 3-tuple of integers (r,g,b) or 4-tuple of integers (r, g, b, a)

        :returns color_index: the index of that new color
        """
        ##fixme: should it check if the same color is already in the palette?
        ##       not just the name?
        if name in self.colors:
            raise ValueError("%s already in the palette"%name)

        cdef int color_index            
        if len(color) == 4:
            self.colors.setdefault(name, gdImageColorAllocateAlpha(self._image, color[0], color[1], color[2], color[3]) )
        elif len(color) == 3:
            color_index = gdImageColorAllocate(self._image, color[0], color[1], color[2])
        else:
            raise ValueError("color must be an (r,g,b) triple or (r,g,b,a) quad")

        if color_index == -1:
            raise ValueError("there are no more colors available to allocate")

        self.colors[name] = color_index
        self.color_names.append(name)

        return color_index

    def add_colors(self, color_list):
        """
        Add a list of colors to the pallette

        :param color_list: list of colors - each elemnt of the list is a 2-tuple: ( 'color_name', (r,g,b) )
        
        :returns indexes: list of color indexes.
        """
        indexes = []
        for name, color in color_list:
            indexes.append( self.add_color(name, color) )
        return indexes
  
    @cython.boundscheck(False)
    def __array__(self):
        """
        :returns arr: numpy array object with a copy of the data

        Note that the array is (width, height) in size, in keeping
        with image convensions, but not array conventions. data is
        in Fortran order
        """
        cdef cnp.ndarray[cnp.uint8_t, ndim=2, mode='fortran'] arr
        arr = np.zeros((self.width, self.height), dtype=np.uint8, order='F')
        cdef unsigned int row, col

        ##copy the data, row by row (copying into columns)
        #for row in range(self.height):
        #    memcpy( &arr[0, row], self._image.pixels[row], self.width)
        ##copy the data, item by item (copying into columns)
        for col in range(self.height):
            memcpy( &arr[0, col], self._image.pixels[col], self.width)
            #for row in range(self.width):
            #    arr[row, col] = self._image.pixels[col][row]
        
        return arr

    #def set_data(self, cnp.ndarray[char, ndim=2, mode='c'] arr not None):
    def set_data(self, char[:,:] arr not None):
        """
        Set the contents of the image from the input array.

        array must be the right size and data type (np.uint8)

        Note that the array is (width, height) in size.

        """
        #print "f-contig:", arr.is_f_contig()
        #print "c-contig:", arr.is_c_contig()
        #print "memview flags are:", arr.flags
        if arr.shape[0] <> self.width or arr.shape[1] <> self.height:
            raise ValueError("input array must be of shape: (width, height), and the same size as image")

        cdef unsigned int row, col

        # ##copy the data, row by row
        #for row in range(self.height):
        #   memcpy(self._image.pixels[row], &arr[row, 0], self.width)
        # ##copy the data, item by item
        for row in range(self.height):
            for col in range(self.width):
                self._image.pixels[row][col] = arr[col, row]


    # def __getbuffer__(self, Py_buffer* buffer, int flags):
    ## attempt to use buffer interface instaed of numpy arrays...
    ## didn't quite work
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


    def __str__(self):
        return "py_gd.Image: width:%s and height:%s"%(self.width, self.height)

    def __repr__(self):
        return "Image(width=%i, height=%i)"%(self.width, self.height)

    ## Saving images
    def save(self, file_name, file_type="bmp", compression=None):
        """
        save the image to disk

        :param file_name: full or relative path to file you want created
        :type file_name: str or unicode object (but only ascii is supported for now)

        """
        cdef bytes file_path
        cdef FILE *fp
        cdef int compression_level

        try:
            file_path = file_name.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError("can only except ascii filenames")

        if file_type in ["bmp", "BMP"]:
            fp = fopen(file_path, "wb");
            gdImageBmp(self._image, fp, 0)
            fclose(fp)
        elif file_type in ("jpg","jpeg"):
            if compression is None:
               compression_level = 80
            else:
                compression_level = compression

            fp = fopen(file_path, "wb");
            gdImageJpeg(self._image, fp, compression_level)
            fclose(fp)
        elif file_type in ("gif", "GIF"):
            fp = fopen(file_path, "wb");
            gdImageGif(self._image, fp)
            fclose(fp)
        elif file_type in ("png", "PNG"):
            fp = fopen(file_path, "wb");
            gdImagePng(self._image, fp)
            fclose(fp)
        else:
            raise ValueError('"bmp", "gif", "png", and "jpeg" are the only valid file_type')

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
            if (color < 0) or (color > 255):
                raise ValueError("you must provide an existing named color or an integer between 0 and 255")
            c = color
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

    ### The drawing functions:
    def draw_pixel(self, point, color):
        """
        set the pixel at the point:(x,y) to the color

        :param point: (x, y cxoord inate of the pixel of interest)
        :type point: 2-tuple of integers (or other sequence)
        """
        gdImageSetPixel (self._image,
                         point[0], point[1],
                         self.get_color_index(color)
                         )

    def draw_line(self, pt1, pt2, color, int line_width=1):
        """
        draw a line from pt1 to pt2

        :param pt1: (x,y) coordinates of start point
        :type pt1: (x,y) sequence of integers

        :param pt2: (x,y) coordinates of end point
        :type pt2: (x,y) sequence of integers

        :param line_width=1: width of line
        :type line_width: integer
        """
        gdImageSetThickness(self._image, line_width)
        gdImageLine(self._image,
                    pt1[0], pt1[1], pt2[0], pt2[1],
                    self.get_color_index(color)
                    )  
        gdImageSetThickness(self._image, 1)

    def draw_polygon(self, points, line_color=None, fill_color=None, int line_width=1):
        """
        Draw a polygon

        :param points: sequence of points
        :type points: Nx2 array of integers (or somethign that can be turned into one)

        :param line_color=None: the color of the outline
        :type line_color=None:  color name or index

        :param fill_color=None: the color of the filled polygon
        :type  fill_color=None: color name or index

        :param line_width=1: width of line
        :type line_width: integer

        """
        cdef int n
        cdef cnp.ndarray[int, ndim=2, mode='c'] points_arr
        
        points_arr = np.asarray(points, dtype=np.int).reshape( (-1,2) )
        n = points_arr.shape[0]
        
        if n < 3:
            raise ValueError("There must be at least three points specified for a polygon")

        
        if fill_color is not None:
            gdImageFilledPolygon(self._image,
                                 <gdPointPtr> &points_arr[0,0],
                                 n,
                                 self.get_color_index(fill_color)
                                 )

        if line_color is not None:
            gdImageSetThickness(self._image, line_width)
            gdImagePolygon(self._image,
                           <gdPointPtr> &points_arr[0,0],
                           n,
                           self.get_color_index(line_color)
                           )
            gdImageSetThickness(self._image, 1)

    def draw_polyline(self, points, line_color, int line_width=1):
        """
        Draw a polyline

        :param points: sequence of points
        :type points: Nx2 array of integers (or somethign that can be turned into one)

        :param line_color=None: the color of the outline
        :type line_color=None:  color name or index

        :param fill_color=None: the color of the filled polygon
        :type  fill_color=None: color name or index

        :param line_width: width of the line to be drawn, in pixels
        :type line_width: integer
        """

        cdef int n
        cdef cnp.ndarray[int, ndim=2, mode='c'] points_arr
        
        points_arr = np.asarray(points, dtype=np.int).reshape( (-1,2) )
        n = points_arr.shape[0]
        
        if n < 3:
            raise ValueError("There must be at least three points specified for a polygon")

        if line_color is not None:
            gdImageSetThickness(self._image, line_width)
            gdImageOpenPolygon(self._image,
                           <gdPointPtr> &points_arr[0,0],
                           n,
                           self.get_color_index(line_color)
                           )
            gdImageSetThickness(self._image, 1)


    def draw_rectangle(self, pt1, pt2, line_color=None, fill_color=None, int line_width=1):
        """
        Draw a rectangle

        :param pt1: upper left corner of rectangle
        :type pt1: (x,y) tuple or sequence of integers

        :param pt2: lower left corner of rectangle
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
                                   self.get_color_index(fill_color)
                                   )

        if line_color is not None:
            gdImageSetThickness(self._image, line_width)
            gdImageRectangle(self._image,
                             pt1[0], pt1[1],
                             pt2[0], pt2[1],
                             self.get_color_index(line_color)
                             )
            gdImageSetThickness(self._image, 1)

    def draw_arc(self, center, width, height,
                 start=0, end=0,
                 line_color=None,
                 fill_color=None,
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

        :param style='arc': styles used to draw the arc. Options are: 'arc' or 'chord'. 'arc' draws the rounded curve, 'chord' connects the start and end points with a line.
        :type style: string

        :param draw_wedge=True: whether to draw the wedge of the slice, or just the outer arc
        :type draw_wedge: bool


        Degrees increase clockwise, starting from the right (east)

        A circle can be drawn by beginning from 0 degrees and ending at 360
        degrees, with width and height being equal. end must be greater than start.
        Values greater than 360 are interpreted modulo 360.

        """

        # set up the style flag:
        if style == 'chord':
            flag = gdChord
        elif style == 'arc':
            flag = gdArc
        else:
            raise ValueError('style must be one of "arc" or "chord"')

        ## filled arc:
        if fill_color is not None:
            gdImageFilledArc(self._image,
                             center[0], center[1],
                             width, height, 
                             start, end,
                             self.get_color_index(fill_color),
                             flag,
                             )
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
                             flag,
                             )
            gdImageSetThickness(self._image, 1)

    def draw_text(self, text, point, font="medium", color='black'):
        """
        draw some text

        :param text: the text to draw
        :type text: string (ascii only for now)

        :param point: coordinates at which to draw the text. the point is the upper left corner of the text bounding box.
        :type point: 2-tuple of (x,y) integers
        
        :param font: desired font -- gd built in fonts: "tiny", "small", "medium", "large", and "giant"
        :type font: string

        :param color: color of text
        :type  color=None: color name or index

        """
        cdef text_bytes
        try:
            text_bytes = text.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError("can only except ascii text")

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
            raise ValueError('font must be one of: "tiny", "small", "medium", "large", and "giant"')

        gdImageString(self._image,
                      gdfont,
                      point[0], point[1],
                      text_bytes,
                      self.get_color_index(color),
                      )


        # if line_color is not None:
        #     gdImageArc(self._image,
        #                center[0], center[1],
        #                width, height, 
        #                start, end,
        #                self.get_color_index(line_color)
        #                )


#def from_array(cnp.ndarray[char, ndim=2, mode='c'] arr not None):
def from_array(char [:,:] arr not None, *args, **kwargs):
    """
    Create an Image from a numpy array, or other object that exposed the PEP 3118 buffer interface.

    The image is the same size as the input array, with the contents copied.

    :param arr: the input array, shape (width, height)
    :type arr: an array, or other PEP 3118 buffer compliant object. Should be 2-d, and of type np.unit8 ('B')

    Other parameters are passed on to the Image() constructor.

    """
    img = Image(arr.shape[0], arr.shape[1], *args, **kwargs)
    img.set_data(arr)

    return img






