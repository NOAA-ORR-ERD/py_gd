"""
colormaps.py

Assorted colormaps you can use with py_gd

To see what they all are::

  print(py_gd.colors.colorscheme_names)

To access a particular one::

  py_gd.colors.colorscheme[name]

NOTE: there are both discrete and continuous colorschemes provided


To Do: a function to create a py_gd colormap from MPL colormaps
       directly

Some of these have been borrowed from the Matplotlib project, so are
licensed under the  MPL license:

1. This LICENSE AGREEMENT is between the Matplotlib Development Team
("MDT"), and the Individual or Organization ("Licensee") accessing and
otherwise using matplotlib software in source or binary form and its
associated documentation.

2. Subject to the terms and conditions of this License Agreement, MDT
hereby grants Licensee a nonexclusive, royalty-free, world-wide license
to reproduce, analyze, test, perform and/or display publicly, prepare
derivative works, distribute, and otherwise use matplotlib 3.2.2 alone
or in any derivative version, provided, however, that MDT's License
Agreement and MDT's notice of copyright, i.e., "Copyright (c) 2012-2013
Matplotlib Development Team; All Rights Reserved" are retained in
matplotlib 3.2.2 alone or in any derivative version prepared by
Licensee.

3. In the event Licensee prepares a derivative work that is based on or
incorporates matplotlib 3.2.2 or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to matplotlib 3.2.2.

4. MDT is making matplotlib 3.2.2 available to Licensee on an "AS IS"
basis. MDT MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.
BY WAY OF EXAMPLE, BUT NOT LIMITATION, MDT MAKES NO AND DISCLAIMS ANY
REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY
PARTICULAR PURPOSE OR THAT THE USE OF MATPLOTLIB 3.2.2 WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. MDT SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF MATPLOTLIB
3.2.2 FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING MATPLOTLIB
3.2.2, OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY
THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between MDT and
Licensee. This License Agreement does not grant permission to use MDT
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using matplotlib 3.2.2, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.
"""

from itertools import islice
import numpy as np

from . import _cm_listed
from . import _color_data


def hex_to_rgb(hex_value):
    """
    convert a hex string to rgb triple
    fixme: this could be done with bit twiddling ..
    """
    hex_value = hex_value.strip('#')
    return (int(hex_value[:2], 16),
            int(hex_value[2:4], 16),
            int(hex_value[4:], 16),
            )


def build_from_named_colors(named_colors):
    return [(name, hex_to_rgb(hex_color)) for name, hex_color in named_colors.items()]


colorschemes = {}

# just for transparent background, no other colors
colorschemes['transparent'] = [('transparent', (0, 0, 0, 127))]

colorschemes['BW'] = (colorschemes["transparent"] + [('black', (0, 0, 0)),
                                                     ('white', (255, 255, 255)),
                                                     ])

# Basic named HTTP color set
# http://en.wikipedia.org/wiki/Web_colors#HTML_color_names
colorschemes['web'] = (colorschemes["BW"] + [('silver', (191, 191, 191)),
                                             ('gray', (127, 127, 127)),
                                             ('red', (255, 0, 0)),
                                             ('maroon', (127, 0, 0)),
                                             ('yellow', (255, 255, 0)),
                                             ('olive', (127, 127, 0)),
                                             ('lime', (0, 255, 0)),
                                             ('green', (0, 127, 0)),
                                             ('aqua', (0, 255, 255)),
                                             ('teal', (0, 127, 127)),
                                             ('blue', (0, 0, 255)),
                                             ('navy', (0, 0, 127)),
                                             ('fuchsia', (255, 0, 255)),
                                             ('purple', (127, 0, 127))])


colorschemes['tableau'] = build_from_named_colors(_color_data.TABLEAU_COLORS)
colorschemes['css4'] = build_from_named_colors(_color_data.CSS4_COLORS)
# XKCD has 954 colors -- we're using the first 255
# but I don't know if they are in significant order
XKCD = dict(islice(_color_data.XKCD_COLORS.items(), 0, 255))
colorschemes['xkcd'] = build_from_named_colors(XKCD)

colorscheme_names = [(name, 'discrete') for name in colorschemes.keys()]

# build continuous colormaps
for dataname in dir(_cm_listed):
    if dataname.endswith("_data"):
        name = dataname[:-5].lstrip("_")
        scheme = getattr(_cm_listed, dataname)
        scheme = (np.array(scheme) * 255).round().astype(np.uint8).tolist()
        colorschemes[name] = [(str(i), tuple(c)) for i, c in enumerate(scheme)]
        colorscheme_names.append((name, 'continuous'))

# clean up the namespace
del dataname, scheme, np
