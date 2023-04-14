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






"""
import cython
# from cython cimport view


# from py_gd cimport *

from libc.stdio cimport FILE, fopen, fclose
from libc.string cimport memcpy, strlen
from libc.stdlib cimport malloc, free
from libc.math cimport pow

from math import ceil, sqrt, nan


import os
import sys
import operator

import numpy as np
cimport numpy as cnp


cpdef bez_point(double t,
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

def distance_pt_to_line(pt, lineStart, lineEnd):
    """
    find the distance between a point and a line

    This really should be Cythonized
    """
    # from: https://gist.github.com/TimSC/0813573d77734bcb6f2cd2cf6cc7aa51
    # double PerpendicularDistance(const Point &pt, const Point &lineStart, const Point &lineEnd)
    # {
    #     double dx = lineEnd.first - lineStart.first;
    #     double dy = lineEnd.second - lineStart.second;

    #     //Normalise
    #     double mag = pow(pow(dx,2.0)+pow(dy,2.0),0.5);
    #     if(mag > 0.0)
    #     {
    #         dx /= mag; dy /= mag;
    #     }

    #     double pvx = pt.first - lineStart.first;
    #     double pvy = pt.second - lineStart.second;

    #     //Get dot product (project pv onto normalized direction)
    #     double pvdot = dx * pvx + dy * pvy;

    #     //Scale line direction vector
    #     double dsx = pvdot * dx;
    #     double dsy = pvdot * dy;

    #     //Subtract this from pv
    #     double ax = pvx - dsx;
    #     double ay = pvy - dsy;

    #     return pow(pow(ax,2.0)+pow(ay,2.0),0.5);
    # }

    dx = lineEnd[0] - lineStart[0]
    dy = lineEnd[1] - lineStart[1]

    # Normalise  # why do this?
    mag = pow(pow(dx, 2.0) + pow(dy, 2.0), 0.5)
    if mag == 0.0:
        return nan
    else:
        dx /= mag
        dy /= mag

    pvx = pt[0] - lineStart[0]
    pvy = pt[1] - lineStart[1]

    # Get dot product (project pv onto normalized direction)
    pvdot = dx * pvx + dy * pvy

    # Scale line direction vector
    dsx = pvdot * dx
    dsy = pvdot * dy

    # Subtract this from pv
    ax = pvx - dsx
    ay = pvy - dsy

    return pow(pow(ax, 2.0) + pow(ay, 2.0), 0.5)

def bezier_curve2(pt1, pt2, cp1, cp2, max_gap=0.5):
    # NOTE: this version is much slower than above -- it can't be vectorized
    #       but it produces many fewer points. If Cythonized, it could be much faster
    """
    This version automatically adjusts the spacing of the points as it goes.

    It enforces an maximum deviation from the curve.

    In the future, it could take linearity into account.

    Function that take input as Control Point x_coordinates and
    Control Point y_coordinates and draw bezier curve

    :param pt1: (x, y) pair: first end point
    :param pt2: (x, y) pair: second end point

    :param cp1: (x, y) pair: first control point
    :param cp2: (x, y) pair: second control point

    :max_gap=0.5: maximum allowable gap between actual spline and
                  piecewise-linear interpolation of the points computed.
                  smaller gap, is smoother, larger gap is fewer points.
    """
    min_gap = max_gap / 2

    x0 = pt1[0]
    x1 = cp1[0]
    x2 = cp2[0]
    x3 = pt2[0]
    y0 = pt1[1]
    y1 = cp1[1]
    y2 = cp2[1]
    y3 = pt2[1]

    # First guess at delta_t
#    N = np.hypot((x1 - x0), (y0 - y1)) / 5
    dt = 5 / np.hypot((x1 - x0), (y0 - y1))
    # print("computing with N=", N)
    XU = [x0]
    YU = [y0]
#    xu, yu = bez_point(dt, x0, y0, x1, y1, x2, y2, x3, y3)
    XU = [x0]
    YU = [y0]
    # T = np.linspace(0, 1, N)
    # print(T)
    # dt = 1 / (N - 1)
    t = 0
    use_prev_point = False
    xm = ym = None  # just to satisfy flake8)
    while True:
        tf = t + dt
        tf = 1.0 if tf >= 1.0 else tf

        tm = t + (dt / 2)
        # print(f"computing far point: {tf=}")
        if use_prev_point:
            xf, yf = xm, ym
        else:
            xf, yf = bez_point(tf, x0, y0, x1, y1, x2, y2, x3, y3)
        # print(f"computing mid point: {tm=}")
        xm, ym, = bez_point(tm, x0, y0, x1, y1, x2, y2, x3, y3)

        dist = distance_pt_to_line((xm, ym), (XU[-1], YU[-1]), (xf, yf))
        # check minimum segment length too?
        if min_gap <= dist <= max_gap:  # add the far point
            # print(f"looking good, adding: {xf, yf}")
            XU.append(xf)
            YU.append(yf)
            t += dt
            use_prev_point = False
        elif dist > max_gap:  # reduce dt and try again
            # print(f"gap to big, reducing dt")
            dt /= 2
            use_prev_point = True
        elif dist < min_gap:  # increase dt and try again
            # print(f"gap to small, increasing dt")
            dt *= 1.5
            use_prev_point = False

        if t >= 1.0:
            break

    xu = np.array(XU)
    yu = np.array(YU)

    points = np.c_[np.round(xu), np.round(yu)].astype(np.intc)

    return points

