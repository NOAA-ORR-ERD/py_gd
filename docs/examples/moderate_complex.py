"""
py_gd demo with moderate complexity -- showing a number of the features

CAn you tell what's being drawn without looking at the results?

"""

# Everything you need is in the Image object

from math import sin, cos, radians

from py_gd import Image

img = Image(width=800, height=600, preset_colors='xkcd')

img.clear('sky blue')

img.draw_rectangle((0, 500), (799, 599), fill_color='grass green')

img.draw_rectangle((200, 300), (600, 500), fill_color='goldenrod')

img.draw_polygon(((400, 200), (180, 300), (620, 300)), fill_color='raspberry')

img.draw_rectangle((320, 400), (400, 500), fill_color='burnt orange')

corner = (230, 320)
w, h = 50, 60
for i in range(4):
    rect = (corner, (corner[0] + w, corner[1] + h))
    img.draw_rectangle(*rect, fill_color='white')
    y = corner[1] + h // 4
    for _ in range(2):
        img.draw_line((corner[0], y),
                      (corner[0] + w, y),
                      color='burnt umber',
                      line_width=2)
        y += h // 4

    x = corner[0] + w // 3
    for _ in range(2):
        img.draw_line((x, corner[1]),
                      (x, corner[1] + h // 2),
                      color='burnt umber',
                      line_width=2)
        x += w // 3
    img.draw_rectangle(*rect,
                       line_color='black',
                       line_width=3,
                       )

    corner = (corner[0] + 95, corner[1])


center = (700, 150)
img.draw_circle(center, diameter=100, fill_color='light yellow')

for i in range(15):
    end = (sin(radians(360 / 15 * i)) * 70 + center[0],
           cos(radians(360 / 15 * i)) * 70 + center[1])
    img.draw_line(center, end, color='light yellow', line_width=3)


img.save("moderate_complex.png", 'png')

