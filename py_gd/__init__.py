#!/usr/bin/env python

"""
py_gd package -- wrappers around the libgd graphics drawing package

The "real" code is in the Cython file: py_gd.pyx

This __init__ does some kludges to load libraries, and then does an

from .py_gd import *
"""

__version__ = "2.3.3"

try:
    from .py_gd import *  # noqa: F401

except ImportError as err:
    raise RuntimeError("Can't find shared libs for libgd.\n"
                       "Make sure they are installed, and on a path where they can be found.\n"
                       "This may require some additional logic in this __init__.py,"
                       "But it would be better to use a standard system location"
                       ) from err
