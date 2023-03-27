Working with Color
==================

8-bit color
-----------
`py_gd` works with colors in (RGB) space. But an interface is provided to work with colors by name. With 8-bit color (The only option in the current version), up to 255 colors can be used.

Before a new color can be used, it needs to be added to the image's "palette" (mapping between integer value and RGB color). Colors cannot be removed from the palette once added.

Transparency:
.............

``py_gd`` support RGBA colors for transparency. Many of the default colorschemes have a transparent background by default.

.. note Some back-ends do not support transparency backgrounds -- BMP, GIF, JPEG. PNG is a good option if you want a transparent background.

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

Other colorschemes are available for initialization -- see ``py_gd.colors.colorscheme_names`` will show them all:

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


Builtin ColorSchemes:
---------------------

Continuous
..........

.. image:: examples/cividis-colorbar.png
   :width: 600
   :align: center

.. image:: examples/inferno-colorbar.png
   :width: 600
   :align: center

.. image:: examples/magma-colorbar.png
   :width: 600
   :align: center

.. image:: examples/plasma-colorbar.png
   :width: 600
   :align: center

.. image:: examples/turbo-colorbar.png
   :width: 600
   :align: center

.. image:: examples/twilight-colorbar.png
   :width: 600
   :align: center

.. image:: examples/viridis-colorbar.png
   :width: 600
   :align: center


