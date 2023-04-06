.. _working_with_color:

Working with Color
==================

8-bit color
-----------
`py_gd` works with colors in (RGB) space. But an interface is provided to work with colors by name. With 8-bit color (The only option in the current version), up to 255 colors can be used.

Before a new color can be used, it needs to be added to the image's "palette" (mapping between integer value and RGB color). Colors cannot be removed from the palette once added.

Transparency:
.............

``py_gd`` support RGBA colors for transparency. Many of the default colorschemes have a transparent background by default.

.. note:: Some backends do not support transparency backgrounds -- BMP, GIF, JPEG. PNG is a good option if you want a transparent background.

If you draw with a semi-transparent color, the blending will be done directly when drawing.


colorschemes
------------

By default, an ``Image`` is created with the "web" colorscheme, so you have access to the standard html colors by name. You can see what colors are available in the current ``Image`` by calling the ``get_color_names`` method:

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

``Image.get_colors`` will return the names and associated RGB values:

.. code-block:: ipython

    img.get_colors()
    Out[2]:
    {'transparent': (0, 0, 0, 127),
     'white': (255, 255, 255),
     'black': (0, 0, 0),
     'red': (229, 0, 0),
     'blue': (3, 67, 223),
     'green': (21, 176, 26),
     'purple': (126, 30, 156),
     'pink': (255, 129, 192),
     'brown': (101, 55, 0),


Note that the first color in the list is the background color.

Other colorschemes are available for initialization -- ``py_gd.colors.colorscheme_names`` will show them all:

.. code-block:: ipython

    py_gd.colors.colorscheme_names
    Out[6]:
    [('transparent', 'discrete'),
     ('BW', 'discrete'),
     ('web', 'discrete'),
     ('tableau', 'discrete'),
     ('css4', 'discrete'),
     ('xkcd', 'discrete'),
     ('cividis', 'continuous'),
     ('inferno', 'continuous'),
     ('magma', 'continuous'),
     ('plasma', 'continuous'),
     ('turbo', 'continuous'),
     ('twilight', 'continuous'),
     ('viridis', 'continuous')]

The "discrete" colorshemes are a set of colors that are specific colors designed to contrast with one another. The "continuous" colorshemes are a smoothly varying range of colors -- good for use with "heat maps" or the built in ``ColorRamp`` system.


In order to use a different color, it needs to be added to the image's color pallet first.
Colors can be added to the image by providing a name and an RGB triple (or RGBA quad for alpha::

    img.add_color('grey', (100, 100, 100))

After adding the color, it can be used by name::

    img.draw_rectangle((10, 20), (60, 70), color = 'grey')


Color Ramps:
------------

A color ramp (also called a color gradient) is continuous colr scheme that maps a color to a value. They can be used to draw a "heat map", or other image where the color is a function of some value.

To work with a color ramp, you need to have a continuous set of colors to pick from, and a way to map a value to particular color. The :class:`~py_gd.color_ramp.ColorRamp` class provided a way to make all this easy.


Using a ColorRamp
.................

A color ramp requires the following information to be useful:

Colors:
    What colors to use -- this needs to be a sequence of RGB colors that form a continuum of some sort. ``py_gd`` provides a set of color ramps borrowed from the Matplotlib package -- these have been carefully designed by the MPL folks.

Range of values:
    in order to map a color to a value, you need to specify what the highest and lowest values that you want to consider are. These are specified by the ``min_value`` and ``max_value`` parameters -- the first color will be mapped to the ``min_value``, and the last color will be mapped to the ``max_value``, with value in between liniearly interpolated to the closest color.


                 num_colors=None,
                 reversed=False,
                 base_colorscheme='BW'):

The Trick of 8-bit Color
........................

``py_gd`` (currently) only support 8-bit color, which means there can be only 256 total colors in a given image. This works fine for the most part 256 colors is enough to create about as much distinction as a person can see (particularly on a computer screen). However, in a given m image, you may want the color ramp, but also a few other colors, such as black and white, etc that can be used to draw other things in the image, so you need a color ramp that can use an arbitrary number of colors.

To accommodate this, the :class:`~py_gd.color_ramp.ColorRamp` class allows you to set the number of colors you want to use for the ramp, either explicitly by setting ``num_colors`` parameter, or specifying the color scheme currently used (or specifying how many colors have been reserved already).

Once a :class:`~py_gd.color_ramp.ColorRamp` has been defined, you can get the color indexes corresponding to given values with the ``get_colors_indices()`` method, and the full set of colors used with the ``colorlist`` property.

For an example of using a ColorRamp, see: :ref:`tutorial_colorramp`



Builtin ColorSchemes:
---------------------

The following are the built-in colorschemes. 


.. include:: color_images.rst








