#!/usr/bin/env python

"""
py_gd package -- wrappers around the libgd graphics drawing package

The "real" code is in the Cython file: py_gd.pyx

This __init__ does some kludges to load libraries, and then does an

from .py_gd import *
"""

import sys
import os

__version__ = "2.3.3"

try:
    from .py_gd import *  # noqa: F401
except ImportError as err:
    if str(err).startswith("DLL load failed:"):
        raise RuntimeError("Can't find dlls for libgd, libpng, and/or libz.\n"
                           "This kludge is only written to support Anaconda installs\n",
                           "you may need to add some logic for other library locations",
                           ) from err
    else:
        raise
