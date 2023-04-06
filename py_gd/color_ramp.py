"""
coloramp (or heatmap)

When you want to use a continuos color map
"""

import numpy as np
from .colors import colorschemes


class ColorRamp():
    def __init__(self,
                 colors,
                 min_value,
                 max_value,
                 num_colors=None,
                 reversed=False,
                 base_colorscheme='BW'):
        """
        :param colors: named color scheme supplied with py_gd
                       or a list of RGB triples. Note that this only
                       makes sense with a "continuous" colorscheme

        :param min_value: value to map to the first color in the scheme
        :param max_value: value to map to the last color in the scheme

        :param num_colors=None: Number of distinct colors to use. By default,
                          It will be scaled to how may colors are used by the
                          base_colorscheme.
        :param reversed=False: Whether to reverse the colorscheme

        :param base_colorscheme='BW': base colorscheme to use -- this reserves
               space for basic drawing. Or simply and integer specifying how many
               colors to reserve.
        """
        self.min_value = min_value
        self.max_value = max_value

        if isinstance(base_colorscheme, str):
            base_colorscheme = colorschemes[base_colorscheme]
        try:
            self.start_index = len(base_colorscheme)
        except TypeError:  # it should be an integer now
            self.start_index = base_colorscheme
        # else:
        #     self.start_index = len(base_colorscheme)

        self._num_colors = 256 - self.start_index if num_colors is None else num_colors
        self._delta = (self.max_value - self.min_value) / self._num_colors

        if isinstance(colors, str):
            colors = [c[1] for c in colorschemes[colors]]
            # otherwise assume it's in the right form
        if reversed:
            colors = reversed(colors)
        self.create_color_index(colors)

    def create_color_index(self, colors):
        # interpolate to the specific colors:
        num_colors = self._num_colors
        colors = np.asarray(colors, dtype=np.uint8).reshape((-1, 3))
        axis = np.linspace(0, num_colors-1, colors.shape[0])

        index = np.empty((num_colors, 3), dtype=np.uint8)

        for i in range(3):  # loop through R,G,B
            index[:, i] = np.interp(range(num_colors), axis, colors[:, i])

        self.color_index = index

    def get_color_indices(self, values):
        """
        returns the color indices that correspond to the values

        :param values: 1D list/array of (usually float) values

        :returns: 1D array of dtype uint8
        """
        values = np.asarray(values)

        inds = np.round((values - self.min_value) / self._delta) + self.start_index
        inds = np.clip(inds,
                       self.start_index,
                       self._num_colors + self.start_index - 1,
                       out=inds)
        inds = inds.astype(np.uint8)

        return inds

    def get_colors(self, values):
        """
        returns the colors as RGB triples corresponding to the values

        :param values: 1D list/array of (usually float) values

        :returns: (Nx3) array of uint8 dtype ``[(R, G, B), (R, G, B), ...]```
        """
        inds = self.get_color_indices(values)

        return self.color_index[inds - self.start_index, :]

    @property
    def colorlist(self):
        """
        returns a list of colors as needed by Image.add_colors
        """
        return [(str(tuple(c)), tuple(c)) for c in self.color_index]
