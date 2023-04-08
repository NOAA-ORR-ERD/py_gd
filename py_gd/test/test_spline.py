"""
test code for splines
"""

from py_gd import Image
from py_gd.spline import bezier_curve, find_control_points, poly_from_ctrl_points

from .test_gd import outfile, check_file


def test_bezier_curve():
    # ctrl_pts = [(100, 200), (10, 500), (500, 50), (500, 300)]
    pt1 = (100, 200)
    pt2 = (500, 300)
    cp1 = (10, 500)
    cp2 = (500, 50)

    spline_pts = bezier_curve(pt1, pt2, cp1, cp2)

    # print(spline_pts)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polyline(spline_pts, 'black', line_width=2)
    # img.draw_dots(spline_pts, diameter=7, color='red')
    img.draw_xes([pt1, pt2, cp1, cp2], diameter=7, color='black', line_width=3)

    filename = "test_spline_1.png"
    img.save(outfile(filename), 'png')
    assert check_file(filename)


def test_find_control_points():
    points = ((100, 100),
              (200, 500),
              (300, 300),
              (500, 400),
              (500, 100),
              (250, 250))

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
    points = ((100, 100),
              (200, 500),
              (300, 300),
              (500, 400),
              (500, 100),
              (250, 250),
              )

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
    # assert check_file(filename)

    assert False
