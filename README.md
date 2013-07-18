py_gd
=====

Python wrappers for libgd graphics drawing lib.

Welcome to the py_gd project.

py-gd aims to provide nice pythonic wrappers around libgd -- a nice, fast, and simple drawing lib:

http://libgd.bitbucket.org/

Why gd?
==========

For the project at hand we needed fast and simple drawing -- 8-bit color, no anti-aliasing.
We also wanted a nice simple API to work with. There are a number of newer drawing libs (AGG, Skia)
that produce some pretty results, but are not as simple to use, and are focused on 32 bit fully
anti-aliased drawing. If  you want the prettiest rendering possible, I encourage you to check those out.
If you want something fast and simple -- py_gd may be for you.

Why a new python wrapper for gd?
==================================

gdmodule (recently moved to gitHub: https://github.com/Solomoriah/gdmodule) is a wrapper
for gd that has been aaround along time. However:
 - It appears to be minimally maintained
 - It is a pretty direct wrapper around the gd old-style-C API
 - It is hand-written C extension code -- more or less the state of the art for 1995
   when it was first written, but I really don't want to work on that code!

On the other hand:
 - py_gd is being actively worked on now. While only supporting Py2 at the moment,
   it should be pretty easy to make a Py3k version.
 - py_gd is a "thick" wrapper -- we're trying to provide a nice object oriented, pythonic inteface.
 - py_gd uses numpy (and the PEP3118 buffer interface) to allow efficient transfer of data back and
   forth between Python and gd.
 - py_gd is written in cython, which is likely to be more robust and error free and easier to maintain.

However, there is some nice stuff in gdmodule (like including a truetype font) that I we want to borrow.

How is py_gd built?
=====================

py_gd is built using Cython: (www.cython.org). Cython allows us to both call into the existing gd C lib,
and to also write wrapper code to make a nicer API in a very efficient way. You shouldn't need Cython
to build and use py_gd, but you'll need it if you want to contribute to the wrappers.


Dependencies:
===============

py_gd currently requires the numpy package: www.numpy.org

numpy is used to allow you to very efficiently pass in data structures for things like vertexes of large
polygons, etc, and can be used to get a copy of the image buffer, and manipulate it in various ways,
as well as passing it back to py_gd.

Is py_gd a complete wrapper around gd?
=============================================

In a word: no.

py_gd is in its infancy, and not the lest bit complete. It does, however have enough to be useful (at least to us).

Major Working features:
 * 8-bit "paletted" images
 * transparent background
 * built-in fonts for text
 * lines, polygons, arcs
 * saving as gif, bmp, png, jpeg
 * numpy arrays for input and image buffer exchange.

Major Missing features:
 * 32bit "truecolor" support
 * loading images from gif, png, etc...
 * freetype fonts
 * image manipulations: scaling, etc

Can I contribute?
==================

You sure you can -- fork the source, and hack away -- you can actually add features pretty easily by taking
a look at what's there -- with just a little C and/or Cython knowledge (not much!) you should be able to
get stuff working.

Here's what you need to do:

 * find the function you want to wrap in gd.h
 * copy the prototype to py_gd.pxd, and edit to to make it Cython-compatible (copy what's done for the ones already there)
 * add a method to the Image class in py_gd.pyx -- look for similar methods already, and try to keep the API similar.
 * add a test to test_gd.py that tests your new method
 * re-build (setup.py develop or setup.py build_ext --inplace)
 * try out your test...
 * lather, rinse, repeat, 'till it all works

