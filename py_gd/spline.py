"""
experimental code for a spline calculation

This version is derived from the C code found at:

https://www.geeksforgeeks.org/cubic-bezier-curve-implementation-in-c/

and some of AGG.

NOTE: This is bezier splines. Another option would be Catmull-Rom splines:

https://qroph.github.io/2018/07/30/smooth-paths-using-catmull-rom-splines.html

"""

import numpy as np
from numpy import power as pow
from math import ceil, sqrt, nan

from ._spline import bezier_curve, distance_pt_to_line


# def bezier_curve(pt1, pt2, cp1, cp2, max_gap=10):
#     """
#     /* Function that take input as Control Point x_coordinates and
# Control Point y_coordinates and draw bezier curve */
# void bezierCurve(int x[] , int y[])

#     :param control_points: 4x2 numpy array of integer points
#     """
#     # points = np.asarray(control_points, dtype=np.intc)

#     xu = 0.0
#     yu = 0.0
#     u = 0.0
#     # i = 0

#     x = [pt1[0], cp1[0], cp2[0], pt2[0]]
#     y = [pt1[1], cp1[1], cp2[1], pt2[1]]

#     # First guess at number of interior points
#     N = int(np.hypot((x[1] - x[0]), (y[0] - y[1])) // (max_gap / 2))
#     while True:  # loop until there are enough interior points
#         # print("computing with N=", N)

#         u = np.linspace(0, 1, N)  # original used 10,000 - dynamic??

#         xu = (pow(1 - u, 3)
#               * x[0] + 3 * u
#               * pow(1 - u, 2) * x[1] + 3
#               * pow(u, 2) * (1 - u) * x[2]
#               + pow(u, 3) * x[3])

#         yu = (pow(1 - u, 3)
#               * y[0] + 3 * u
#               * pow(1 - u, 2) * y[1] + 3
#               * pow(u, 2) * (1 - u) * y[2]
#               + pow(u, 3) * y[3])

#         dist = np.hypot(np.diff(xu), np.diff(yu))
#         # print()
#         # print(f"{dist.max()=}")
#         # print(f"{dist.min()=}")
#         max_dist = dist.max()
#         if max_dist <= max_gap:
#             break
#         # print("Too big a gap -- recomputing")
#         N = ceil(N * max_dist / max_gap * 1.1)  # bump up a bit to make sure.
#     points = np.c_[np.round(xu), np.round(yu)].astype(np.intc)

#     return points


# def bez_point(t, x0, y0, x1, y1, x2, y2, x3, y3):
#     """
#     return a single point on a bezier curve
#     """
#     xu = (pow(1 - t, 3)
#           * x0 + 3 * t
#           * pow(1 - t, 2) * x1 + 3
#           * pow(t, 2) * (1 - t) * x2
#           + pow(t, 3) * x3)

#     yu = (pow(1 - t, 3)
#           * y0 + 3 * t
#           * pow(1 - t, 2) * y1 + 3
#           * pow(t, 2) * (1 - t) * y2
#           + pow(t, 3) * y3)

#     return xu, yu


# def dist_sq(pt1, pt2):
#     """
#     return the square of the distance between two points
#     """
#     pow((pt2[0] - pt1[0]), 2) + pow((pt2[1] - pt1[1]), 2)

# def bezier_curve_recursive(pt1, pt2, cp1, cp2, max_gap=2):
#     """
#     How to do this? I have no idea what the control points are
#     for a sub-section of the curve

      # or how to keep the points in order -- if they are genenerated
      # out of order, they would need to be sorted.
#     """
#     # if the two points are too close
#     if dist_sq(pt1, pt2) < 4:
#         return pt2
#     # add a point in the middle:
#     x, y = bez_point(t, pt1[0], pt1[1], cp1[0], cp1[1], cp2[0], cp2[1], pt2[0], pt2[1])


# def bezier_curve2(pt1, pt2, cp1, cp2, max_gap=0.5):
#     # NOTE: this version is much slower than above -- it can't be vectorized
#     #       but it produces many fewer points. If Cythonized, it could be much faster
#     """
#     This version automatically adjusts the spacing of the points as it goes.

#     It enforces an maximum deviation from the curve.

#     In the future, it could take linearity into account.

#     Function that take input as Control Point x_coordinates and
#     Control Point y_coordinates and draw bezier curve

#     :param pt1: (x, y) pair: first end point
#     :param pt2: (x, y) pair: second end point

#     :param cp1: (x, y) pair: first control point
#     :param cp2: (x, y) pair: second control point

#     :max_gap=0.5: maximum allowable gap between actual spline and
#                   piecewise-linear interpolation of the points computed.
#                   smaller gap, is smoother, larger gap is fewer points.
#     """
#     min_gap = max_gap / 2

#     x0 = pt1[0]
#     x1 = cp1[0]
#     x2 = cp2[0]
#     x3 = pt2[0]
#     y0 = pt1[1]
#     y1 = cp1[1]
#     y2 = cp2[1]
#     y3 = pt2[1]

#     # First guess at delta_t
# #    N = np.hypot((x1 - x0), (y0 - y1)) / 5
#     dt = 5 / np.hypot((x1 - x0), (y0 - y1))
#     # print("computing with N=", N)
#     XU = [x0]
#     YU = [y0]
# #    xu, yu = bez_point(dt, x0, y0, x1, y1, x2, y2, x3, y3)
#     XU = [x0]
#     YU = [y0]
#     # T = np.linspace(0, 1, N)
#     # print(T)
#     # dt = 1 / (N - 1)
#     t = 0
#     use_prev_point = False
#     xm = ym = None  # just to satisfy flake8)
#     while True:
#         tf = t + dt
#         tf = 1.0 if tf >= 1.0 else tf

#         tm = t + (dt / 2)
#         # print(f"computing far point: {tf=}")
#         if use_prev_point:
#             xf, yf = xm, ym
#         else:
#             xf, yf = bez_point(tf, x0, y0, x1, y1, x2, y2, x3, y3)
#         # print(f"computing mid point: {tm=}")
#         xm, ym, = bez_point(tm, x0, y0, x1, y1, x2, y2, x3, y3)

#         dist = distance_pt_to_line((xm, ym), (XU[-1], YU[-1]), (xf, yf))
#         # check minimum segment length too?
#         if min_gap <= dist <= max_gap:  # add the far point
#             # print(f"looking good, adding: {xf, yf}")
#             XU.append(xf)
#             YU.append(yf)
#             t += dt
#             use_prev_point = False
#         elif dist > max_gap:  # reduce dt and try again
#             # print(f"gap to big, reducing dt")
#             dt /= 2
#             use_prev_point = True
#         elif dist < min_gap:  # increase dt and try again
#             # print(f"gap to small, increasing dt")
#             dt *= 1.5
#             use_prev_point = False

#         if t >= 1.0:
#             break

#     xu = np.array(XU)
#     yu = np.array(YU)

#     points = np.c_[np.round(xu), np.round(yu)].astype(np.intc)

#     return points


# def bezier_curve_agg():
#     """
#     bezier code from the AGG website:

#     https://agg.sourceforge.net/antigrain.com/research/bezier_interpolation/index.html

#     I don't quite get it, but should give it a try some day
#     """
#     # This one is iterative, to
#     # // Number of intermediate points between two source ones,
#     # // Actually, this value should be calculated in some way,
#     # // Obviously, depending on the real length of the curve.
#     # // But I don't know any elegant and fast solution for this
#     # // problem.
#     # #define NUM_STEPS 20

#     # void curve4(Polygon* p,
#     #             double x1, double y1,   //Anchor1
#     #             double x2, double y2,   //Control1
#     #             double x3, double y3,   //Control2
#     #             double x4, double y4)   //Anchor2
#     # {
#     #     double dx1 = x2 - x1;
#     #     double dy1 = y2 - y1;
#     #     double dx2 = x3 - x2;
#     #     double dy2 = y3 - y2;
#     #     double dx3 = x4 - x3;
#     #     double dy3 = y4 - y3;

#     #     double subdiv_step  = 1.0 / (NUM_STEPS + 1);
#     #     double subdiv_step2 = subdiv_step*subdiv_step;
#     #     double subdiv_step3 = subdiv_step*subdiv_step*subdiv_step;

#     #     double pre1 = 3.0 * subdiv_step;
#     #     double pre2 = 3.0 * subdiv_step2;
#     #     double pre4 = 6.0 * subdiv_step2;
#     #     double pre5 = 6.0 * subdiv_step3;

#     #     double tmp1x = x1 - x2 * 2.0 + x3;
#     #     double tmp1y = y1 - y2 * 2.0 + y3;

#     #     double tmp2x = (x2 - x3)*3.0 - x1 + x4;
#     #     double tmp2y = (y2 - y3)*3.0 - y1 + y4;

#     #     double fx = x1;
#     #     double fy = y1;

#     #     double dfx = (x2 - x1)*pre1 + tmp1x*pre2 + tmp2x*subdiv_step3;
#     #     double dfy = (y2 - y1)*pre1 + tmp1y*pre2 + tmp2y*subdiv_step3;

#     #     double ddfx = tmp1x*pre4 + tmp2x*pre5;
#     #     double ddfy = tmp1y*pre4 + tmp2y*pre5;

#     #     double dddfx = tmp2x*pre5;
#     #     double dddfy = tmp2y*pre5;

#     #     int step = NUM_STEPS;

#     #     // Suppose, we have some abstract object Polygon which
#     #     // has method AddVertex(x, y), similar to LineTo in
#     #     // many graphical APIs.
#     #     // Note, that the loop has only operation add!
#     #     while(step--)
#     #     {
#     #         fx   += dfx;
#     #         fy   += dfy;
#     #         dfx  += ddfx;
#     #         dfy  += ddfy;
#     #         ddfx += dddfx;
#     #         ddfy += dddfy;
#     #         p->AddVertex(fx, fy);
#     #     }
#     #     p->AddVertex(x4, y4); // Last step must go exactly to x4, y4
#     # }
#     pass


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
    for i in range(len(points) - 1):
        poly_points.extend(bezier_curve(points[i],
                                        points[i + 1],
                                        ctrl_points[2 * i - 2],
                                        ctrl_points[2 * i - 1]))
    poly_points.extend(bezier_curve(points[-1],
                                    points[0],
                                    ctrl_points[-4],
                                    ctrl_points[-3]))

    return poly_points

# cy_distance_pt_to_line = distance_pt_to_line

# def distance_pt_to_line(point, line_start, line_end):
#     """
#     python version -- takes 2-sequences of points
#     """
#     return cy_distance_pt_to_line(point[0], point[1],
#                                   line_start[0], line_start[1],
#                                   line_end[0], line_end[1])


# def distance_pt_to_line(point, line_start, line_end):
#     """
#     distance from a point (x, y) to the line defined by two points:
#     (x1, y1) and (x2, y2)

#     from:
#     https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
#     """

#     x, y = point
#     x1, y1 = line_start
#     x2, y2 = line_end

#     # function pDistance(x, y, x1, y1, x2, y2) {

#     #   var A = x - x1;
#     #   var B = y - y1;
#     #   var C = x2 - x1;
#     #   var D = y2 - y1;

#     #   var dot = A * C + B * D;
#     #   var len_sq = C * C + D * D;
#     #   var param = -1;
#     #   if (len_sq != 0) //in case of 0 length line
#     #       param = dot / len_sq;

#     #   var xx, yy;

#     #   if (param < 0) {
#     #     xx = x1;
#     #     yy = y1;
#     #   }
#     #   else if (param > 1) {
#     #     xx = x2;
#     #     yy = y2;
#     #   }
#     #   else {
#     #     xx = x1 + param * C;
#     #     yy = y1 + param * D;
#     #   }

#     #   var dx = x - xx;
#     #   var dy = y - yy;
#     #   return Math.sqrt(dx * dx + dy * dy);
#     # }

#     A = x - x1
#     B = y - y1
#     C = x2 - x1
#     D = y2 - y1

#     if x1 == x2 and y1 == y2:  # end points are the same
#         xx = x1
#         yy = y1
#     else:
#         dot = A * C + B * D
#         len_sq = C * C + D * D

#         param = dot / len_sq

#         xx = x1 + param * C
#         yy = y1 + param * D

#     dx = x - xx
#     dy = y - yy

#     return sqrt(dx * dx + dy * dy)



# def distance_pt_to_line(pt, lineStart, lineEnd):
#     """
#     find the distance between a point and a line

#     NOTE: this one is a lot slower that the other one :=)
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

#     dx = lineEnd[0] - lineStart[0]
#     dy = lineEnd[1] - lineStart[1]

#     # Normalise  # why do this?
#     mag = pow(pow(dx, 2.0) + pow(dy, 2.0), 0.5)
#     if mag == 0.0:
#         return nan
#     else:
#         dx /= mag
#         dy /= mag

#     pvx = pt[0] - lineStart[0]
#     pvy = pt[1] - lineStart[1]

#     # Get dot product (project pv onto normalized direction)
#     pvdot = dx * pvx + dy * pvy

#     # Scale line direction vector
#     dsx = pvdot * dx
#     dsy = pvdot * dy

#     # Subtract this from pv
#     ax = pvx - dsx
#     ay = pvy - dsy

#     return pow(pow(ax, 2.0) + pow(ay, 2.0), 0.5)
