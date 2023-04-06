"""
script for building images for the docs for the colorschemes
"""
import math

from py_gd import Image
from py_gd import colors

with open('../color_images.rst', 'w') as rst:

    for cname, ctype in colors.colorscheme_names:
        if cname == 'transparent':
            # no point in rendering this one
            continue
        if ctype == "continuous":
            img = Image(510, 40, preset_colors=cname)
            # starting at 1 to avoid the transparent color-0
            for i in range(1, 256):
                x = 2 * (i - 1)
                y1 = 0
                y2 = 40
                img.draw_rectangle((x, y1), (x + 2, y2), fill_color=i)
            try:
                img.draw_rectangle((0, 0), (509, 39), line_color='black')
            except ValueError:
                pass  # no black in colorscheme
        else:
            # just to get the colors
            img = Image(1, 1, preset_colors=cname)
            all_colors = img.get_colors()
            num_colors = len(img.get_colors())
            height = math.ceil(num_colors / 3) * 50
            img = Image(510, height, preset_colors=cname)
            x, y = 0, 0
            for color in all_colors:
                try:
                    img.draw_text(color, (x + 95, y + 25), color='black', align='r', font='medium')
                except ValueError as err:
                    if "existing named color" in str(err): 
                        print(f"{cname} does not have black")
                    else:
                        raise
                rect = (x + 100, y), (x + 169, y + 49)
                img.draw_rectangle(*rect, fill_color=color)
                try:
                    img.draw_rectangle(*rect, line_color='black')
                except ValueError:
                    pass  # no black in colorscheme

                x += 170
                if x > 350:
                    y += 50
                    x = 0
        filename = f'colorbars/{cname}-colorbar.png'
        img.save(filename, 'png')
        rst.write(f"\n{cname}:\n")
        rst.write(f"""
.. image:: examples/{filename}
   :align: center
""")

