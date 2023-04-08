"""
experimental code for a spline calculation

This version is derived from the C code found at:

https://www.geeksforgeeks.org/cubic-bezier-curve-implementation-in-c/


Refactored to called from Cython

/* Function that take input as Control Point x_coordinates and
Control Point y_coordinates and draw bezier curve */

void bezierCurve(int x[], int y[])
{
    double xu = 0.0 , yu = 0.0 , u = 0.0 ;
    int i = 0 ;
    for(u = 0.0 ; u <= 1.0 ; u += 0.0001)
    {
        xu = pow(1-u,3)*x[0]+3*u*pow(1-u,2)*x[1]+3*pow(u,2)*(1-u)*x[2]
            +pow(u,3)*x[3];
        yu = pow(1-u,3)*y[0]+3*u*pow(1-u,2)*y[1]+3*pow(u,2)*(1-u)*y[2]
            +pow(u,3)*y[3];
        SDL_RenderDrawPoint(renderer , (int)xu , (int)yu) ;
    }
}
"""

import numpy as np
from numpy import power as pow
from math import ceil, sqrt


def bezier_curve(pt1, pt2, cp1, cp2, max_gap=10):
    """
    /* Function that take input as Control Point x_coordinates and
Control Point y_coordinates and draw bezier curve */
void bezierCurve(int x[] , int y[])

    :param control_points: 4x2 numpy array of integer points
    """
    # points = np.asarray(control_points, dtype=np.intc)

    xu = 0.0
    yu = 0.0
    u = 0.0
    # i = 0

    x = [pt1[0], cp1[0], cp2[0], pt2[0]]
    y = [pt1[1], cp1[1], cp2[1], pt2[1]]

    # Save non-vectprized version -- for Cython?
    # also, could decide step size as you go..
    # x0 = control_points[1, 0]
    # x1 = control_points[1, 1]
    # x2 = control_points[1, 2]
    # x3 = control_points[1, 3]
    # points = []
    # for u in np.linspace(0, 1, 10):  # original used 10,000 - dynamic??
    #     xu = (pow(1 - u, 3)
    #           * x[0] + 3 * u
    #           * pow(1 - u, 2) * x[1] + 3
    #           * pow(u, 2) * (1 - u) * x[2]
    #           + pow(u, 3) * x[3])

    #     yu = (pow(1 - u, 3)
    #           * y[0] + 3 * u
    #           * pow(1 - u, 2) * y[1] + 3
    #           * pow(u, 2) * (1 - u) * y[2]
    #           + pow(u, 3) * y[3])

    # vectorized version

    # First guess at number of interior points
    N = int(np.hypot((x[1] - x[0]), (y[0] - y[1])) // (max_gap / 2))
    while True:  # loop until there are enough interior points
        # print("computing with N=", N)

        u = np.linspace(0, 1, N)  # original used 10,000 - dynamic??

        xu = (pow(1 - u, 3)
              * x[0] + 3 * u
              * pow(1 - u, 2) * x[1] + 3
              * pow(u, 2) * (1 - u) * x[2]
              + pow(u, 3) * x[3])

        yu = (pow(1 - u, 3)
              * y[0] + 3 * u
              * pow(1 - u, 2) * y[1] + 3
              * pow(u, 2) * (1 - u) * y[2]
              + pow(u, 3) * y[3])

        dist = np.hypot(np.diff(xu), np.diff(yu))
        # print(f"{dist.max()=}")
        # print(f"{dist.min()=}")
        max_dist = dist.max()
        if max_dist <= max_gap:
            break
        # print("Too big a gap -- recomputing")
        N = ceil(N * max_dist / max_gap * 1.1)  # bump up a bit to make sure.
    points = np.c_[np.round(xu), np.round(yu)].astype(np.intc)

    return points


def find_control_points(in_points, smooth_value=0.5):
    """
    find reasonable control points to make a smooth spline from a polyline / polygon

    :param points: Nx2 array of (x, y) points (integers)


    :param smooth_value=1.0: amount to smooth -- should be between 0 and 1.0

    Adapted from AGG code found here:

    https://agg.sourceforge.net/antigrain.com/research/bezier_interpolation/index.html

    """

    # // Assume we need to calculate the control
    # // points between (x1,y1) and (x2,y2).
    # // Then x0,y0 - the previous vertex,
    # //      x3,y3 - the next one.

    # double xc1 = (x0 + x1) / 2.0;
    # double yc1 = (y0 + y1) / 2.0;
    # double xc2 = (x1 + x2) / 2.0;
    # double yc2 = (y1 + y2) / 2.0;
    # double xc3 = (x2 + x3) / 2.0;
    # double yc3 = (y2 + y3) / 2.0;

    # double len1 = sqrt((x1-x0) * (x1-x0) + (y1-y0) * (y1-y0));
    # double len2 = sqrt((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1));
    # double len3 = sqrt((x3-x2) * (x3-x2) + (y3-y2) * (y3-y2));

    # double k1 = len1 / (len1 + len2);
    # double k2 = len2 / (len2 + len3);

    # double xm1 = xc1 + (xc2 - xc1) * k1;
    # double ym1 = yc1 + (yc2 - yc1) * k1;

    # double xm2 = xc2 + (xc3 - xc2) * k2;
    # double ym2 = yc2 + (yc3 - yc2) * k2;

    # // Resulting control points. Here smooth_value is mentioned
    # // above coefficient K whose value should be in range [0...1].
    # ctrl1_x = xm1 + (xc2 - xm1) * smooth_value + x1 - xm1;
    # ctrl1_y = ym1 + (yc2 - ym1) * smooth_value + y1 - ym1;

    # ctrl2_x = xm2 + (xc2 - xm2) * smooth_value + x2 - xm2;
    # ctrl2_y = ym2 + (yc2 - ym2) * smooth_value + y2 - ym2;

    num_verts = len(in_points)
    in_points = np.asarray(in_points)

    points = np.zeros((num_verts + 3, 2), dtype=np.float64)
    points[:-3, :] = in_points
    points[-3:] = in_points[:3]

    ctrl_points = np.zeros((num_verts * 2, 2), dtype=np.intc)

    for i in range(num_verts):

        # // Assume we need to calculate the control
        # // points between (x1,y1) and (x2,y2).
        # // Then x0,y0 - the previous vertex,
        # //      x3,y3 - the next one.

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

        # Resulting control points. Here smooth_value is mentioned
        # above coefficient K whose value should be in range [0...1].
        ctrl1_x = xm1 + (xc2 - xm1) * smooth_value + x1 - xm1
        ctrl1_y = ym1 + (yc2 - ym1) * smooth_value + y1 - ym1

        ctrl2_x = xm2 + (xc2 - xm2) * smooth_value + x2 - xm2
        ctrl2_y = ym2 + (yc2 - ym2) * smooth_value + y2 - ym2

        ctrl_points[2 * i, 0] = ctrl1_x
        ctrl_points[2 * i, 1] = ctrl1_y
        ctrl_points[2 * i + 1, 0] = ctrl2_x
        ctrl_points[2 * i + 1, 1] = ctrl2_y

    return ctrl_points


def poly_from_ctrl_points(points, ctrl_points):

    poly_points = []
    for i in range(len(points)-1):
        poly_points.extend(bezier_curve(points[i],
                                        points[i + 1],
                                        ctrl_points[2 * i - 2],
                                        ctrl_points[2 * i - 1]))
    poly_points.extend(bezier_curve(points[-1],
                                    points[0],
                                    ctrl_points[-4],
                                    ctrl_points[-3]))


    return poly_points
