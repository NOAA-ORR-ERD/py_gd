"""
test code for splines
"""
import math
import numpy as np

from py_gd import Image
from py_gd.spline import (bezier_curve,
                          find_control_points,
                          poly_from_ctrl_points,
                          distance_pt_to_line,
                          )

# from .test_gd import outfile, check_file
from py_gd.test.test_gd import outfile, check_file


def test_bezier_curve():
    # ctrl_pts = [(100, 200), (10, 500), (500, 50), (500, 300)]
    pt1 = (100, 200)
    pt2 = (500, 300)
    cp1 = (10, 500)
    cp2 = (500, 50)

    spline_pts = bezier_curve(pt1, pt2, cp1, cp2)

    spline_pts = np.round(spline_pts).astype(np.intc)

    # print(spline_pts)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polyline(spline_pts, 'black', line_width=2)
    # img.draw_dots(spline_pts, diameter=7, color='red')
    img.draw_xes([pt1, pt2, cp1, cp2], diameter=7, color='black', line_width=3)

    filename = "test_spline_1.png"
    img.save(outfile(filename), 'png')
    assert check_file(filename)


def test_bezier_curve_flat():
    # ctrl_pts = [(100, 200), (10, 500), (500, 50), (500, 300)]
    pt1 = (100, 100)
    pt2 = (500, 500)
    cp1 = (200, 200)
    cp2 = (300, 300)

    spline_pts = bezier_curve(pt1, pt2, cp1, cp2)

    print(spline_pts)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polyline(spline_pts, 'black', line_width=2)
    # img.draw_dots(spline_pts, diameter=7, color='red')
    img.draw_xes([pt1, pt2, cp1, cp2], diameter=7, color='black', line_width=3)

    filename = "test_spline_flat.png"
    img.save(outfile(filename), 'png')
    assert check_file(filename)


def test_find_control_points():
    points = np.array([(100, 100),
                       (200, 500),
                       (300, 300),
                       (500, 400),
                       (500, 100),
                       (250, 250)],
                      dtype=np.float64
                      )

    ctrl_points = find_control_points(points)

    print(ctrl_points)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polygon(points, 'black', line_width=2)
    img.draw_dots(points, diameter=8, color='red')
    img.draw_dots(ctrl_points, diameter=10, color='blue')

    filename = "test_control_points.png"
    img.save(outfile(filename), 'png')
    # assert check_file(filename)


def test_poly_from_ctrl_points():
    points = np.array([(100, 100),
                       (200, 500),
                       (300, 300),
                       (500, 400),
                       (500, 100),
                       (250, 250),
                       ], dtype=np.float64)

    ctrl_points = find_control_points(points)

    print(f"{points=}")
    print(f"{ctrl_points=}")

    poly_points = poly_from_ctrl_points(points, ctrl_points)

    print(ctrl_points)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polygon(points, 'black', line_width=2)
    img.draw_polygon(poly_points, 'red', line_width=2)
    img.draw_dots(points, diameter=8, color='red')
    img.draw_dots(ctrl_points, diameter=10, color='blue')

    filename = "test_smooth_poly.png"
    img.save(outfile(filename), 'png')
    assert check_file(filename)


def test_poly_line():
    points = np.array([(100, 100),
                       (200, 500),
                       (300, 300),
                       (500, 400),
                       (500, 100),
                       (250, 250),
                       ], dtype=np.float64)

    ctrl_points = find_control_points(points)

    print(f"{points=}")
    print(f"{ctrl_points=}")

    poly_points = poly_from_ctrl_points(points, ctrl_points)

    print(ctrl_points)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polygon(points, 'black', line_width=2)
    img.draw_polygon(poly_points, 'red', line_width=2)
    img.draw_dots(points, diameter=8, color='red')
    img.draw_dots(ctrl_points, diameter=10, color='blue')

    filename = "test_smooth_polyline.png"
    img.save(outfile(filename), 'png')

    assert check_file(filename)


def test_distance_pt_to_line():
    """
    A few quick checks -- points on either side should be same dist

    reversing line should be the same
    """
    line_start = (0.0, 0.0)
    line_end = (10.0, 10.0)

    point = (6.0, 5.0)
    d1 = distance_pt_to_line(point, line_start, line_end)
    print(d1)

    assert math.isclose(d1, 0.7071067811865476)

    point = (5.0, 6.0)
    d2 = distance_pt_to_line(point, line_start, line_end)

    assert d1 == d2

    # reverse the order of the line:
    d3 = distance_pt_to_line(point, line_end, line_start)

    assert d3 == d1


def test_distance_pt_to_line_neg():
    """
    A few quick checks -- points on either side should be same dist

    negative coords should work too
    """
    line_start = (-2.0, -2.0)
    line_end = (-10.0, -10.0)

    point = (-6.0, -5.0)
    d1 = distance_pt_to_line(point, line_start, line_end)
    print(d1)

    point = (-5.0, -6.0)
    d2 = distance_pt_to_line(point, line_start, line_end)

    assert d1 == d2


def test_distance_pt_to_line_zero():
    """
    point on line should be close to zero
    """
    line_start = (0.0, 0.0)
    line_end = (10.0, 10.0)

    point = (5.0, 5.0)
    d1 = distance_pt_to_line(point, line_start, line_end)
    print(d1)

    assert d1 <= 1e-14


def test_distance_pt_to_line_zero_length_line():
    """
    Zero Length line should return distance to the point
    """
    line_start = (10.0, 20.0)
    line_end = (10.0, 20.0)

    point = (10.0, 20.0)
    d1 = distance_pt_to_line(point, line_start, line_end)
    print(d1)

    assert d1 == 0.0

    point = (10.0, 10.0)
    d2 = distance_pt_to_line(point, line_start, line_end)
    print(d2)

    assert d2 == 10.0


def test_distance_pt_to_line_beyond():
    """
    does it work beyond the points?
    """
    line_start = (0.0, 0.0)
    line_end = (4.0, 4.0)

    point = (6.0, 5.0)
    d1 = distance_pt_to_line(point, line_start, line_end)
    print(d1)

    assert math.isclose(d1, 0.7071067811865476)

    point = (5.0, 6.0)
    d2 = distance_pt_to_line(point, line_start, line_end)

    assert d1 == d2

    # reverse the order of the line:
    d3 = distance_pt_to_line(point, line_end, line_start)

    assert d3 == d1



# if __name__ == "__main__":
#     test_bezier_curve2()
