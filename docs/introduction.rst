Introduction
============

``py_gd`` is a set of "Pythonic" bindings to the libgd rendering library

``py_gd`` aims to provide nice Pythonic wrappers around libgd -- a robust, fast, and simple drawing lib:

``https://github.com/libgd/libgd/``

Why gd?
-------

For the project at hand we needed fast and simple drawing -- 8-bit color, no anti-aliasing.
We also wanted a nice simple API to work with. There are a number of newer drawing libs (AGG, Skia)
that produce some pretty results, but are not as simple to use, and are focused on 32 bit fully
anti-aliased drawing. If  you want the prettiest rendering possible, I encourage you to check those out.

If you want something fast and simple -- `py_gd` may be for you.

General Structure:
------------------

``py_gd`` provides an Object-Oriented interface for rendering.

At the core is the ``Image`` class -- it gets created with a given set of parameters, at least the size of the image::

  img = Image(width=400, height=400)

once created, you can draw to with a variety of drawing functions::

   img.draw_line((1, 1), (350, 200), color='red', line_width=3)

Drawing of an object is usually accomplished with a single call -- you can set the properties of the object you want to draw all at once: color, line width, etc.

The image can be saved out in various formats::

    img.save('my_image.png', 'png')


Managing Colors
...............

`py_gd` works with colors in (RGB) space. But an interface is provided to work with colors by name. With 8-bit color (The only option in the current version), up to 255 colors can be used. By default, `Image` is created with the "web" colorscheme, so you have access to the standard html colors by name. You can see what colors are available in the currennt Image:

.. code-block:: ipython

    In [6]: img.get_color_names()
    Out[6]:
    ['transparent',
     'black',
     'white',
     'silver',
     'gray',
     'red',
     'maroon',
     'yellow',
     'olive',
     'lime',
     'green',
     'aqua',
     'teal',
     'blue',
     'navy',
     'fuchsia',
     'purple']

Note that the first color in the list is the background color.

In order to use a different color, it needs to be added to the image's color pallet first.
Colors can be added to the image by providing a name and an RGB triple (or RGBA quad for alpha::

    img.add_color('grey', (100, 100, 100))













