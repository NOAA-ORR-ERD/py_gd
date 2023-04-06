.. _tutorial_colorramp:

Using a ``ColorRamp``
=====================

Full script here:  :download:`colorramp.py <examples/colorramp.py>`

This tutorial covers rendering a "heat map" wusing a color ramp.


Import the library
------------------

Most of the functionality you need are methods on the :class:Image object, so you import that directly::

  from py_gd import Image


Create the Image
----------------

In this case,the image is created as 800x800 with the "xkcd" colorscheme::

    img = Image(width=600, height=600, preset_colors='xkcd')

The xkcd colors are set to those named by a
`survey by Randall Monroe <https://xkcd.com/color/rgb/>`_
(py_gd only support 256 colors, so this is the first 256)

You can check what colors are set on the image with ``Image.get_color_names()``:

.. code-block:: ipython

    In [5]: img.get_color_names()
    Out[5]:
    ['transparent',
     'white',
     'black',
     'red',
     'blue',
     'green',
     'purple',
     'pink',
     'brown',
     'light blue',
    ...

The first color (in this case transparent) is the default background color.

Reset the Backgound
-------------------

If you want a different background color, or to clear the whole image, you can call clear with the color you want.

img.clear('lilac')


Draw a Line
-----------

The ``Image`` class has a number of drawing methods.

* To draw a line, you need to specify the start and end coordinates as (x, y) pairs. (0, 0) is at the top left, with x going down, and y going to the right.

* You can specify the color by name: it must be one of the named colors set on the image.

* Other parameters can be set as well. In the case of a line, the width can be set in pixels.

    img.draw_line((0, 0), (600, 600), color='red', line_width=10)


This will draw a 10 pixel wide red line from the top left corner to the bottom right corner.

Draw a Rectangle
----------------

* To draw a rectangle, you need to specify the upper left and bottom right corners.

* You can specify the color by name: it must be one of the named colors set on the image.

* Other parameters can be set as well. In the case of a line, the width can be set in pixels.

    img.draw_line((0, 0), (600, 600), color='red', line_width=10)


This will draw a 10 pixel wide red line from the top left corner to the bottom right corner.


Save the Image
--------------

The image can be saved in a number of formats. BMP is the default. Other formats will be available dependingon how libgd was compiled.::

    img.save("moderate_complex.png", 'png')

.. image:: examples/moderate_complex.png
   :width: 300
   :align: center

