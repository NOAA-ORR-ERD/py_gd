"""
test code for splines
"""

from py_gd import Image
from py_gd.spline import bezier_curve

from .test_gd import outfile, check_file


def test_bezier_curve():
    ctrl_pts = [(100, 200), (10, 500), (500, 50), (500, 300)]

    spline_pts = bezier_curve(ctrl_pts)

    # print(spline_pts)

    img = Image(600, 600)
    img.clear('white')

    img.draw_polyline(spline_pts, 'black', line_width=2)
    # img.draw_dots(spline_pts, diameter=7, color='red')
    img.draw_xes(ctrl_pts, diameter=7, color='black', line_width=3)


    filename = "test_spline_1.png"
    img.save(outfile(filename), 'png')
    assert check_file(filename)
