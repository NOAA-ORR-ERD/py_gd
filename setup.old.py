#!/usr/bin/env python

"""
setup.py script for the py_gd package

This version links in static versions of the required libs, which must be build  separately.

The "regular" version, finds the dynamic libs.
"""

import sys, os

from setuptools import setup

#from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy #for the include dirs...

include_dirs = [numpy.get_include(), './static_libs/include']
library_dirs = ['./static_libs/lib']

## This setup requires libgd and libpng
## It expects to find them in ./static_libs
## if they are not there, or on a "usual path", 
## you can set them below, or override them with the following 
## environmment variables:
# LIBGD_LOCATION
# LIBPNG_LOCATION
# it will look for 'include' and 'lib' in those locations

## check for environment variables:
for loc in [os.environ.get('LIBGD_LOCATION', ''),
            os.environ.get('LIBPNG_LOCATION', ''),
            ]:
    if loc:
        include_dirs.append(os.path.join(loc,'include') )
        library_dirs.append(os.path.join(loc, 'lib') )

ext_modules=[ Extension("py_gd.py_gd",
                        ["py_gd/py_gd.pyx"],
                        include_dirs = include_dirs,
                        library_dirs = library_dirs,
                        libraries=["gd","png","jpeg"],
                         )]
setup(
    name = "py_gd",
    version='0.1.1',
    description = "python wrappers around libgd graphics lib",
    #long_description=read('README'),
    author = "Christopher H. Barker",
    author_email = "chris.barker@noaa.gov",
    #url="",
    license = "Public Domain",
    keywords = "graphics cython drawing",
    ext_modules = cythonize(ext_modules), 
    packages = ["py_gd",],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: Public Domain",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Multimedia :: Graphics",
    ],
)


