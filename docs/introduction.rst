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

Parameters of Drawing:
----------------------

Depedning in the object being draw, there are a number of parameters that can be set:

For Lines:
..........

| ``color``: string colorname
| ``line_width``: integer pixels


For Solid Color Objects:
........................

| ``color``: string colorname

For Objects with a Line and Fill:
.................................

| ``line_color``: string colorname
| ``fill_color``: string colorname
| ``line_width``: integer pixels

For Ojects Defined at a Single Point:
.....................................

| ``point``: (x, y) tuple

For Ojects Defined at a Multiple Points:
........................................

Polygon, Polyline

| ``points``: sequence of points: ``[(x1, y1), (x2, y2), (x3, y3), ...]`` (Nx2 numpy array)

For Objects with a Width or Height:
...................................

| ``width``: integer pixels
| ``height``: integer pixels

