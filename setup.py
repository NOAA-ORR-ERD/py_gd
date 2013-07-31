#!/usr/bin/env python

"""
setup.py script for the py_gd package
"""

import sys, os

from setuptools import setup

#from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy #for the include dirs...

## total kludge here: for building libpng and gd itself:
## you should be able to replace these for an installed gd or png lib.

static_libs = ["./static_libs/lib/libgd.a",
              "./static_libs/lib/libpng.a"]

includes    = ["./static_libs/include/gd.h",
               "./static_libs/include/png.h",
               ]

include_dirs = [os.path.split(filename)[0] for filename in includes]
include_dirs = list(set(include_dirs)) # remove the duplicates

need_to_build = []
for lib in static_libs:
    if not os.path.isfile(lib):
        need_to_build.append(lib)

print need_to_build


all_args = " ".join(sys.argv[1:])
if 'build' in all_args or 'develop' in all_args:
     # check for static_libs dir
     if need_to_build:
        print "*** Need to build:", need_to_build, '\n'
        # libpng?
        lib_names = []
        if "libpng" in " ".join(need_to_build):
            lib_names.append("libpng-1.6.3")
        if "libgd" in " ".join(need_to_build):
            lib_names.append("libgd-2.1.0")

        import build_gd
        build_gd.do_it_all(lib_names)


ext_modules=[ Extension("py_gd.py_gd",
                        ["py_gd/py_gd.pyx"],
                        include_dirs = ["./static_libs/include/",
                                        numpy.get_include(),
                                        ],
                        libraries=["jpeg"],
                        extra_objects=["./static_libs/lib/libgd.a",
                                       "./static_libs/lib/libpng.a"],
                         )]
setup(
    name = "py_gd",
    version='0.1.1',
    description = "python wrappers around libgd graphics lib",
    #long_description=read('README'),
    author = "Christopher H. Barker",
    author_email = "chris.barker@Nnoaa.gov",
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


