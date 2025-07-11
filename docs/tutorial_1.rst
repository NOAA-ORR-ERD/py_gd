.. _tutorial_ultra_simple:

Ultra Simple Example
====================

Full script here:  :download:`ultra_simple.py <examples/0-ultra_simple.py>`

For a first introduction to the py_gd, we create a very simple image with a single line on it:

Import the library
------------------

Most of the functionality you need are methods on the :class:Image object, so you import that directly::

  from py_gd import Image


Create the Image
----------------

The minimal information you need to provide is what size to create the image::

    img = Image(width=400, height=400)

That will create a 400 X 400 pixel image with the default color scheme ('web' colors)


Draw a Line
-----------

The ``Image`` class has a number of drawing methods.

* To draw a line, you need to specify the start and end coordinates as (x, y) pairs. (0, 0) is at the top left, with x going down, and y going to the right.

* You can specify the color by name: it must be one of the named colors set on the image.

* Other parameters can be set as well. In the case of a line, the width can be set in pixels.

    img.draw_line((0, 0), (400, 300), color='red', line_width=10)

This will draw a 10 pixel wide red line from the top left diagonally down toward the bottom right:

Save the Image
--------------

The image can be saved in a number of formats. BMP is the default. Other formats will be available dependingon how libgd was compiled.::

    img.save('my_image.png', 'png')

Note that the default background is transparent.

.. image:: examples/0-ultra_simple.png
   :width: 200
   :align: center

