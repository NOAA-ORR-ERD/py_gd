"""

Cython version of

experimental code for a spline calculation

This version is derived from the C code found at:

https://www.geeksforgeeks.org/cubic-bezier-curve-implementation-in-c/

and some of AGG.

NOTE: This is bezier splines. Another option would be Catmull-Rom splines:

https://qroph.github.io/2018/07/30/smooth-paths-using-catmull-rom-splines.html

Some timings:

from py_gd.spline import bezier_curve2, bezier_curve

pre-cython:

pt1 = (100, 200)
pt2 = (500, 300)
cp1 = (10, 500)
cp2 = (500, 50)

In [3]: %timeit spline_pts = bezier_curve(pt1, pt2, cp1, cp2)
335 µs ± 5.64 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)

In [4]: %timeit spline_pts = bezier_curve2(pt1, pt2, cp1, cp2)
2.41 ms ± 23.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

bez_point untyped cython:

In [3]: %timeit spline_pts = bezier_curve2(pt1, pt2, cp1, cp2)
974 µs ± 19.5 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)

>2X speedup!

bez_point typed cython:

In [3]: %timeit spline_pts = bezier_curve2(pt1, pt2, cp1, cp2)
807 µs ± 40.3 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)

only a little better, surprizing

bezier_curve2 cython not typed

In [3]: %timeit spline_pts = bezier_curve2(pt1, pt2, cp1, cp2)
126 µs ± 1.38 µs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)

nice!

distance_pt_to_line typedefed

In [3]: %timeit spline_pts = bezier_curve2(pt1, pt2, cp1, cp2)
116 µs ± 2.31 µs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)

typedefed bezier_curve2
In [4]: %timeit spline_pts = bezier_curve2(pt1, pt2, cp1, cp2)
75 µs ± 2.54 µs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)

removed tuple unpacking in bez_point

In [3]: %timeit spline_pts = bezier_curve(pt1, pt2, cp1, cp2)
57 µs ± 957 ns per loop (mean ± std. dev. of 7 runs, 10,000 loops each)

Timing find_control_points

In [1]:     points = ((100, 100),
   ...:               (200, 500),
   ...:               (300, 300),
   ...:               (500, 400),
   ...:               (500, 100),
   ...:               (250, 250))

Pure Python:

In [3]: %timeit find_control_points(points)
73.4 µs ± 612 ns per loop (mean ± std. dev. of 7 runs, 10,000 loops each)

Cython -- only typed input arrays

In [7]: %timeit find_control_points(points)
9.27 µs ± 52 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)

Fully typed:

In [5]: %timeit find_control_points(points)
3.1 µs ± 54.9 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)

"""
import cython
# from cython cimport view


# from py_gd cimport *

from libc.stdio cimport FILE, fopen, fclose
from libc.string cimport memcpy, strlen
from libc.stdlib cimport malloc, free
from libc.math cimport pow, sqrt

from math import ceil, nan


import os
import sys
import operator

import numpy as np
cimport numpy as cnp


cdef bez_point(double t,
                 double x0,
                 double y0,
                 double x1,
                 double y1,
                 double x2,
                 double y2,
                 double x3,
                 double y3):
    """
    return a single point on a bezier curve
    """
    cdef double xu
    cdef double yu
    xu = (pow(1 - t, 3)
          * x0 + 3 * t
          * pow(1 - t, 2) * x1 + 3
          * pow(t, 2) * (1 - t) * x2
          + pow(t, 3) * x3)

    yu = (pow(1 - t, 3)
          * y0 + 3 * t
          * pow(1 - t, 2) * y1 + 3
          * pow(t, 2) * (1 - t) * y2
          + pow(t, 3) * y3)

    return xu, yu

# cpdef distance_pt_to_line(tuple point, tuple line_start, tuple line_end):
    """
    distance from a point (x, y) to the line defined by two points:
    (x1, y1) and (x2, y2)

    from:
    https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    """
cdef c_distance_pt_to_line(double x,
                           double y,
                           double x1,
                           double y1,
                           double x2,
                           double y2,
                           ):

    # function pDistance(x, y, x1, y1, x2, y2) {

    #   var A = x - x1;
    #   var B = y - y1;
    #   var C = x2 - x1;
    #   var D = y2 - y1;

    #   var dot = A * C + B * D;
    #   var len_sq = C * C + D * D;
    #   var param = -1;
    #   if (len_sq != 0) //in case of 0 length line
    #       param = dot / len_sq;

    #   var xx, yy;

    #   if (param < 0) {
    #     xx = x1;
    #     yy = y1;
    #   }
    #   else if (param > 1) {
    #     xx = x2;
    #     yy = y2;
    #   }
    #   else {
    #     xx = x1 + param * C;
    #     yy = y1 + param * D;
    #   }

    #   var dx = x - xx;
    #   var dy = y - yy;
    #   return Math.sqrt(dx * dx + dy * dy);
    # }

    cdef double A = x - x1
    cdef double B = y - y1
    cdef double C = x2 - x1
    cdef double D = y2 - y1

    cdef double xx, yy, param

    # should I do a closeness test?
    if x1 == x2 and y1 == y2:  # end points are the same
        xx = x1
        yy = y1
    else:
        dot = A * C + B * D
        len_sq = C * C + D * D

        param = dot / len_sq

        xx = x1 + param * C
        yy = y1 + param * D

    dx = x - xx
    dy = y - yy

    return sqrt(dx * dx + dy * dy)


def distance_pt_to_line(point, line_start, line_end):
    """
    python version -- takes 2-sequences of points
    """
    return c_distance_pt_to_line(point[0], point[1],
                                 line_start[0], line_start[1],
                                 line_end[0], line_end[1])


# cpdef double distance_pt_to_line(tuple pt, tuple lineStart, tuple lineEnd):
#     """
#     find the distance between a point and a line

#     This really should be Cythonized
#     """
#     # from: https://gist.github.com/TimSC/0813573d77734bcb6f2cd2cf6cc7aa51
#     # double PerpendicularDistance(const Point &pt, const Point &lineStart, const Point &lineEnd)
#     # {
#     #     double dx = lineEnd.first - lineStart.first;
#     #     double dy = lineEnd.second - lineStart.second;

#     #     //Normalise
#     #     double mag = pow(pow(dx,2.0)+pow(dy,2.0),0.5);
#     #     if(mag > 0.0)
#     #     {
#     #         dx /= mag; dy /= mag;
#     #     }

#     #     double pvx = pt.first - lineStart.first;
#     #     double pvy = pt.second - lineStart.second;

#     #     //Get dot product (project pv onto normalized direction)
#     #     double pvdot = dx * pvx + dy * pvy;

#     #     //Scale line direction vector
#     #     double dsx = pvdot * dx;
#     #     double dsy = pvdot * dy;

#     #     //Subtract this from pv
#     #     double ax = pvx - dsx;
#     #     double ay = pvy - dsy;

#     #     return pow(pow(ax,2.0)+pow(ay,2.0),0.5);
#     # }
#     cdef double dx = lineEnd[0] - lineStart[0]
#     cdef double dy = lineEnd[1] - lineStart[1]
#     cdef double mag

#     # Normalise  # why do this?
#     mag = pow(pow(dx, 2.0) + pow(dy, 2.0), 0.5)
#     if mag == 0.0:
#         return nan
#     else:
#         dx /= mag
#         dy /= mag

#     cdef double pvx = pt[0] - lineStart[0]
#     cdef double pvy = pt[1] - lineStart[1]

#     # Get dot product (project pv onto normalized direction)
#     cdef double pvdot = dx * pvx + dy * pvy

#     # Scale line direction vector
#     cdef double dsx = pvdot * dx
#     cdef double dsy = pvdot * dy

#     # Subtract this from pv
#     cdef double ax = pvx - dsx
#     cdef double ay = pvy - dsy

#     return pow(pow(ax, 2.0) + pow(ay, 2.0), 0.5)


def bezier_curve(pt1, pt2, cp1, cp2, double max_gap=0.5):
    """
    Compute a polyline aproximation to a cubic bezier spline.

    Spline from pt1 to pt2, with control points cp1 and cp2.

    Number of vertices detrmined to assure that the polyline is
    within a given gap of the actual curve.

    :param pt1: (x, y) pair: first end point
    :param pt2: (x, y) pair: second end point

    :param cp1: (x, y) pair: first control point
    :param cp2: (x, y) pair: second control point

    :max_gap=0.5: maximum allowable gap between actual spline and
                  piecewise-linear interpolation of the points computed.
                  smaller gap, is smoother, larger gap is fewer points.
    """
    cdef double x0 = pt1[0]
    cdef double y0 = pt1[1]

    cdef double x1 = cp1[0]
    cdef double y1 = cp1[1]

    cdef double x2 = cp2[0]
    cdef double y2 = cp2[1]

    cdef double x3 = pt2[0]
    cdef double y3 = pt2[1]

    return c_bezier_curve(x0, x1,
                          x2, x3,
                          y0, y1,
                          y2, y3,
                          max_gap)

cdef c_bezier_curve(double x0, double x1,
                    double x2, double x3,
                    double y0, double y1,
                    double y2, double y3,
                    double max_gap
                    ):
    # Pure Cython function that does the real work for bezier_curve

    # Takes the coordinates of the end points and control points as
    # individual doubles.

    # See docstring for the Python version for details.


    # :max_gap=0.5: maximum allowable gap between actual spline and
    #               piecewise-linear interpolation of the points computed.
    #               smaller gap, is smoother, larger gap is fewer points.
    cdef double min_gap = max_gap / 2.0

    # First guess at delta_t
    cdef double dt = 5.0 / sqrt(pow((x1 - x0), 2) + pow((y0 - y1), 2))

    cdef list XU = [x0]
    cdef list YU = [y0]

    cdef double t = 0.0
    cdef char use_prev_point = 0
    cdef double xm, ym, xf, yf, tf, tm
    while True:
        tf = t + dt
        # make sure final point is exactly t=1.0
        tf = 1.0 if tf >= 1.0 else tf

        tm = t + (dt / 2)
        # print(f"computing far point: {tf=}")
        if use_prev_point:
            xf, yf = xm, ym
        else:
            # compute the far point
            xf, yf = bez_point(tf, x0, y0, x1, y1, x2, y2, x3, y3)
        # compute the mid point
        xm, ym, = bez_point(tm, x0, y0, x1, y1, x2, y2, x3, y3)

        dist = c_distance_pt_to_line(xm, ym, XU[-1], YU[-1], xf, yf)
        if min_gap <= dist <= max_gap:  # add the far point
            # print(f"looking good, adding: {xf, yf}")
            XU.append(xf)
            YU.append(yf)
            t += dt
            use_prev_point = 0
        elif dist > max_gap:  # reduce dt and try again
            dt /= 2
            use_prev_point = 1
        elif dist < min_gap:  # increase dt and try again
            dt *= 1.5
            use_prev_point = 0

        if t >= 1.0:
            break

    xu = np.array(XU)
    yu = np.array(YU)

    points = np.c_[xu, yu]

    return points


def find_control_points(cnp.ndarray[double, ndim=2, mode='c'] in_points,
                        double smoothness=0.5):
    """
    Find reasonable control points to make a smooth spline from a polyline / polygon

    :param points: Nx2 array of (x, y) points (np.float64)

    :param smoothness=0.5: amount to smooth -- should be between 0 and 1.0


    :returns ctrl_points: two points for each line seg

    Adapted from AGG code found here:

    https://agg.sourceforge.net/antigrain.com/research/bezier_interpolation/index.html
    """

    cdef cnp.uint16_t i, num_verts

    # in_points = np.asarray(in_points)
    num_verts = in_points.shape[0]

    cdef cnp.ndarray[double, ndim=2, mode='c'] points
    cdef cnp.ndarray[double, ndim=2, mode='c'] ctrl_points

    points = np.zeros((num_verts + 3, 2), dtype=np.float64)
    points[:-3, :] = in_points
    points[-3:] = in_points[:3]

    ctrl_points = np.zeros((num_verts * 2, 2), dtype=np.float64)

    # Fixme: are this many temp variables needed?
    cdef double x0
    cdef double y0
    cdef double x1
    cdef double y1
    cdef double x2
    cdef double y2
    cdef double x3
    cdef double y3

    cdef double xc1
    cdef double yc1
    cdef double xc2
    cdef double yc2
    cdef double xc3
    cdef double yc3

    cdef double len1
    cdef double len2
    cdef double len3

    cdef double k1
    cdef double k2

    cdef double xm1
    cdef double ym1

    cdef double xm2
    cdef double ym2

    for i in range(num_verts):
        # // calculate the control
        # // points between (x1, y1) and (x2, y2)
        # // Then (x0, y0) - the previous vertex,
        # //      (x3, y3) - the next one.

        x0 = points[i, 0]
        y0 = points[i, 1]
        x1 = points[i + 1, 0]
        y1 = points[i + 1, 1]
        x2 = points[i + 2, 0]
        y2 = points[i + 2, 1]
        x3 = points[i + 3, 0]
        y3 = points[i + 3, 1]

        xc1 = (x0 + x1) / 2.0
        yc1 = (y0 + y1) / 2.0
        xc2 = (x1 + x2) / 2.0
        yc2 = (y1 + y2) / 2.0
        xc3 = (x2 + x3) / 2.0
        yc3 = (y2 + y3) / 2.0

        len1 = sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
        len2 = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        len3 = sqrt((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2))

        k1 = len1 / (len1 + len2)
        k2 = len2 / (len2 + len3)

        xm1 = xc1 + (xc2 - xc1) * k1
        ym1 = yc1 + (yc2 - yc1) * k1

        xm2 = xc2 + (xc3 - xc2) * k2
        ym2 = yc2 + (yc3 - yc2) * k2

        # Resulting control points. Here smoothness is mentioned
        # above coefficient K whose value should be in range [0...1].
        ctrl1_x = xm1 + (xc2 - xm1) * smoothness + x1 - xm1
        ctrl1_y = ym1 + (yc2 - ym1) * smoothness + y1 - ym1

        ctrl2_x = xm2 + (xc2 - xm2) * smoothness + x2 - xm2
        ctrl2_y = ym2 + (yc2 - ym2) * smoothness + y2 - ym2

        ctrl_points[2 * i, 0] = ctrl1_x
        ctrl_points[2 * i, 1] = ctrl1_y
        ctrl_points[2 * i + 1, 0] = ctrl2_x
        ctrl_points[2 * i + 1, 1] = ctrl2_y

    return ctrl_points


def poly_from_ctrl_points(cnp.ndarray[cnp.float64_t, ndim=2, mode='c'] points,
                          cnp.ndarray[cnp.float64_t, ndim=2, mode='c'] ctrl_points):

    cdef list poly_points = []
    cdef cnp.uint16_t i

    for i in range(len(points) - 1):
        poly_points.extend(bezier_curve(points[i],
                                        points[i + 1],
                                        ctrl_points[2 * i - 2],
                                        ctrl_points[2 * i - 1]).tolist())

    poly_points.extend(bezier_curve(points[-1],
                                    points[0],
                                    ctrl_points[-4],
                                    ctrl_points[-3]).tolist())


    return np.array(poly_points, dtype=np.float64)

