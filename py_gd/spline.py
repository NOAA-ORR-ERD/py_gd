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
import math


def bezier_curve(control_points, max_gap=10):
    """
    /* Function that take input as Control Point x_coordinates and
Control Point y_coordinates and draw bezier curve */
void bezierCurve(int x[] , int y[])

    :param control_points: 4x2 numpy array of integer points
    """
    control_points = np.asarray(control_points, dtype=np.intc)

    xu = 0.0
    yu = 0.0
    u = 0.0
    i = 0

    x = control_points[:, 0]
    y = control_points[:, 1]

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
        N = math.ceil(N * max_dist / max_gap * 1.1)  # bump up a bit to make sure.
    points = np.c_[np.round(xu), np.round(yu)].astype(np.intc)

    return points
