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

if sys.platform.startswith('win'):
    # This only works for Anaconda / miniconda
    # On other  systems, logic needs to be added here.
    # there must be a better way to do this -- why doesn't conda take care of it?
    libpath = os.path.join(os.path.split(sys.executable)[0], "Library", "bin")

    # Add lib dir to PATH:
    if (os.path.isfile(os.path.join(libpath, 'libpng16.dll')) and
            os.path.isfile(os.path.join(libpath, 'zlib.dll')) and
            os.path.isfile(os.path.join(libpath, 'libgd.dll'))):
        os.environ['PATH'] = libpath + os.pathsep + os.environ['PATH']

try:
    from .py_gd import *  # noqa: F401

except ImportError as err:
    if str(err).startswith("DLL load failed:"):
        if not (os.path.isfile(os.path.join(libpath, 'libpng16.dll')) and
                os.path.isfile(os.path.join(libpath, 'zlib.dll')) and
                os.path.isfile(os.path.join(libpath, 'libgd.dll'))):
            raise RuntimeError("Can't find dlls for libgd, libpng, and libz.\n"
                               "This kludge is only written to support Anaconda installs\n",
                               "you may need to add some logic for other library locations",
                               )
        else:
            raise
    else:
        raise
    print(err.args)
