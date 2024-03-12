"""
declarations for the cython wrapper around the gd drawing lib
"""

#cython: language_level=3

import cython

from libc.stdio cimport FILE
IF UNAME_SYSNAME == "Windows":
    cdef extern from "<windows.h>":
#        ctypedef Py_UNICODE wchar_t
        FILE *_wfopen(const wchar_t *filename, const wchar_t *mode)

## access the gd header files:
cdef extern from "gd.h":

    cdef struct gdImageStruct:
        pass  # for now, all I need is to know it exists to pass along...
        # Palette-based image pixels
        unsigned char **pixels
        # lots more we might want here, but for now...
    ctypedef gdImageStruct *gdImagePtr

    cdef struct gdPoint:
        int x, y
    ctypedef gdPoint *gdPointPtr

    cdef struct gdFont:
        int w
        int h
    ctypedef gdFont *gdFontPtr

    ## The functions we want to wrap

    # get the version
    const char * gdVersionString()

    # utilities for creating, etc, images
    gdImagePtr gdImageCreatePalette(int width, int height)

    void gdImageDestroy (gdImagePtr im)

    int gdImageColorAllocate (gdImagePtr im, int r, int g, int b)
    int gdImageColorAllocateAlpha(gdImagePtr im, int r, int g, int b, int a)
    int gdImageGetPixel(gdImagePtr im, int x, int y)

    void gdImageSetClip(gdImagePtr im, int x1, int y1, int x2, int y2)
    void gdImageGetClip(gdImagePtr im, int *x1P, int *y1P, int *x2P, int *y2P)

    # drawing functions
    ## to set up line drawing
    void gdImageSetThickness(gdImagePtr im, int thickness)

    void gdImageSetPixel (gdImagePtr im, int x, int y, int color)

    void gdImageLine (gdImagePtr im, int x1, int y1, int x2, int y2, int color)

    void gdImagePolygon (gdImagePtr im, gdPointPtr p, int num_points, int color)
    void gdImageFilledPolygon (gdImagePtr im, gdPointPtr p, int num_points, int color)

    void gdImageOpenPolygon(gdImagePtr im, gdPointPtr points, int pointsTotal, int color)

    void gdImageRectangle(gdImagePtr im, int x1, int y1, int x2, int y2, int color)
    void gdImageFilledRectangle(gdImagePtr im, int x1, int y1, int x2, int y2, int color)

    void gdImageArc(gdImagePtr im, int cx, int cy, int w, int h, int s, int e, int color)
    void gdImageFilledArc(gdImagePtr im, int cx, int cy, int w, int h, int s, int e, int color, int style)

    void gdImageEllipse(gdImagePtr im, int mx, int my, int w, int h, int c)
    void gdImageFilledEllipse (gdImagePtr im, int mx, int my, int w, int h, int c)

    #copying, etc.
    void gdImageCopy(gdImagePtr dst, gdImagePtr src, int dstX, int dstY, int srcX, int srcY, int w, int h)

    # text drawing, etc.
    void gdImageString(gdImagePtr im, gdFontPtr font, int x, int y, unsigned char *s, int color)

    # image saving functions
    void gdImageBmp  (gdImagePtr im, FILE *outFile,  int compression)
    void gdImageJpeg (gdImagePtr im, FILE * outFile, int quality)
    void gdImageGif  (gdImagePtr im, FILE *outFile)
    void gdImagePng  (gdImagePtr im, FILE *outFile)

    # query functions
    int gdImageSX(gdImagePtr im) # MACRO
    int gdImageSY(gdImagePtr im) # MACRO
    int gdImageCompare (gdImagePtr im1, gdImagePtr im2);

    # constants (these are #define in gd.h)
    cdef int gdArc
    cdef int gdPie
    cdef int gdChord
    cdef int gdNoFill
    cdef int gdEdged

    #comparison constants (return values of gdImageCompare)
    cdef int GD_CMP_IMAGE          # 1 Actual image IS different
    cdef int GD_CMP_NUM_COLORS     # 2 Number of Colours in pallette differ
    cdef int GD_CMP_COLOR          # 4 Image colours differ
    cdef int GD_CMP_SIZE_X         # 8 Image width differs
    cdef int GD_CMP_SIZE_Y         # 16 Image heights differ
    cdef int GD_CMP_TRANSPARENT    # 32 Transparent colour
    cdef int GD_CMP_BACKGROUND     # 64 Background colour
    cdef int GD_CMP_INTERLACE      # 128 Interlaced setting
    cdef int GD_CMP_TRUECOLOR      # 256 Truecolor vs palette differs

    # animation
    void gdImageGifAnimBegin(gdImagePtr im, FILE *outFile, int GlobalCM, int Loops);
    void gdImageGifAnimAdd(gdImagePtr im, FILE *outFile, int LocalCM, int LeftOfs, int TopOfs, int Delay, int Disposal, gdImagePtr previm);
    void gdImageGifAnimEnd(FILE *outFile);

# fonts are in extra headers:
cdef extern from "gdfontt.h":
    gdFontPtr gdFontTiny
cdef extern from "gdfonts.h":
    gdFontPtr gdFontSmall
cdef extern from "gdfontmb.h":
    gdFontPtr gdFontMediumBold
cdef extern from "gdfontl.h":
    gdFontPtr gdFontLarge
cdef extern from "gdfontg.h":
    gdFontPtr gdFontGiant

## synonm
#cdef int gdPie = gdArc






