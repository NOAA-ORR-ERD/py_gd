.. _splines:

Splines
=======

Splines are curves that can smoothly fit arbitrary points.

``libgd`` does not natively include support for splines, py_gd includes this support natively.

.. warning: Splines are new and experimental to py_gd, and thus are poorly documented and may not work as expected. If you have issues, feedback is welcome on gitHub: https://github.com/NOAA-ORR-ERD/py_gd

The spline calculations are written in Cython, so should be fairly fast and efficient.

Cubic Bézier splines
--------------------

Spline support uses `cubic Bézier splines <https://en.wikipedia.org/wiki/B%C3%A9zier_curve>`_
-- a cubic Bézier spline is defined by two end points and two control points -- the curve starts and ends at the end points, with the curve in between controlled by the location of the control points. They are smooth, and the entire curve lies within the convex hull of all four points.


Drawing Splines
---------------

Smooth Lines:
.............

In order to draw a spline with libgd, the spline is approximated by a polyline, and then rendered as a polyline or polygon. The spacing of the vertices should be such that the curve looks smooth. This is non-trivial, as the spline is defined parametrically, but py_gd included code that determines appropriate spacing of the vertices.

Smooth Polygons:
................

Simple rendering of smoothed polygons is provided by the ``Image.draw_spline_polygon()`` method.
It uses a method `developed by the AGG <https://agg.sourceforge.net/antigrain.com/research/bezier_interpolation/index.html>`_ library for determining control points that result in a smooth curve through all the vertices of a polygon. The smoothness can be adjusted as desired.

For examples, see:

:download:`spline_star.py <examples/spline_star.py>`

