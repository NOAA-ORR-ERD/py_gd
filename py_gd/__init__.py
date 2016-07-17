#!/usr/bin/env python

"""
py_gd package -- wrappers around the libgd graphics drawing package

The "real" code is in the cython file: py_gd.pyx

"""
__version__ = "0.1.6"
__gd_version__ = "2.2.2" # note -- should do a runtime check for version, yes???

import sys, os
if sys.platform.startswith('win'):
    ## This only works for Anaconda / miniconda
    ## On other  systems, logic needs to be added here.
    libpath = os.path.join(os.path.split(sys.executable)[0], "Library", "bin")

    # ## UGLY kludge for Windows: load the libgd dll with ctypes so it can be used by the extension
    # import ctypes
    # # note: need to load up the dependencies, too
    # #       this is a serious kludge!
    # try:
    #     libpng = ctypes.cdll.LoadLibrary(os.path.join(libpath,'libpng16.dll'))
    #     zlib = ctypes.cdll.LoadLibrary(os.path.join(libpath,'zlib.dll'))
    #     libgd = ctypes.cdll.LoadLibrary(os.path.join(libpath,'libgd.dll'))
    # except WindowsError as err:
    #     raise WindowsError("Can't find dlls for libgd, libpng, and libz.\n"
    #                        "This kludge is only written to support Anaconda installs")

    # alternative ugly kludge: add lib dir to PATH:
    if not (os.path.isfile(os.path.join(libpath,'libpng16.dll')) and
            os.path.isfile(os.path.join(libpath,'zlib.dll')) and
            os.path.isfile(os.path.join(libpath,'libgd.dll')) ):
        raise RuntimeError("Can't find dlls for libgd, libpng, and libz.\n"
                           "This kludge is only written to support Anaconda installs\n",
                           "you may need to add some logic for other library locations",
                              )
    os.environ['PATH'] = libpath + os.pathsep + os.environ['PATH']
try:
    from py_gd import *
except ImportError as err:
    if err.message.startswith("DLL load failed:"):
        if not (os.path.isfile(os.path.join(libpath,'libpng16.dll')) and
                os.path.isfile(os.path.join(libpath,'zlib.dll')) and
                os.path.isfile(os.path.join(libpath,'libgd.dll')) ):
            raise RuntimeError("Can't find dlls for libgd, libpng, and libz.\n"
                           "This kludge is only written to support Anaconda installs\n",
                           "you may need to add some logic for other library locations",
                              )
        else:
            raise
    else:
        raise
    print err.args
