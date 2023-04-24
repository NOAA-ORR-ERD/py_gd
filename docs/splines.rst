.. _splines:

Splines
=======

Splines are curves that can smoothly fit arbitrary points.

``libgd`` does not natively include support for splines, py_gd includes this support natively. The spline calculations are written in Cython, so should be.

Spline support uses cubic bezier splines -- a cubic bezier spline is defined by two end points, and two control points -- the curve starts and ends at the end points, with the curve in between controlled by the location of the control points. They are smooth, and the entire curve lies within the convex hull of all four points.

Drawing Splines
---------------

In order to draw a spline with libgd, the spline is approximated by polyline, and then rendered as a polyline or polygon.

Simple rendering of smoothed polygons is provided by the ``Image.draw_spline_polygon()`` method. It uses a method `developed by the AGG <https://agg.sourceforge.net/antigrain.com/research/bezier_interpolation/index.html>`_ library for determining control points that result in a smooth curve through all the vertices of a polygon. The smoothness can be adjusted as desired.

For example:

To draw a star with a smooth spline:

vertices = [(),
(),
()]
