"""
script for building images for the docs for the colorschemes
"""

from py_gd import Image
from py_gd import colors

rst = open('color_images.rst', 'w')

for cname, ctype in colors.colorscheme_names:
    if ctype == "continuous":
        img = Image(600, 100, preset_colors=cname)
        img.draw_text(cname, (20, 20),
                      font="giant",
                      color=125,
                      background=255)
        for i in range(1, 256):
            x = 45 + 2 * i
            y1 = 40
            y2 = 60
            img.draw_rectangle((x, y1), (x + 2, y2), fill_color=i)
    else:
        continue
    filename = f'{cname}-colorbar.png'
    img.save(filename, 'png')
    rst.write(f"""
.. image:: examples/{filename}
   :width: 600
   :align: center
"""
)
rst.close()

