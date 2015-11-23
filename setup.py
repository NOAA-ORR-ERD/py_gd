#!/usr/bin/env python

"""
setup.py script for the py_gd package

Tested with:
  Anaconda on OS_X
  Anaconda on Win64

  Python 2.7.5 on CentOS 7
  Python 2.7.10

libgd is assumed to be installed (and its dependencies) already.
The Anaconda package at:
   http://anaconda.org/noaa-orr-erd/libgd
is a good way to get it

"""

import sys, os

from setuptools import setup, Extension

from Cython.Build import cythonize

import numpy #for the include dirs...

include_dirs = [numpy.get_include(),]
library_dirs = []
libraries = ['gd']
compile_args = []
link_args = []

if sys.platform.startswith('win'):
    # need the library and include for Windows Anaconda... <PREFIX>/Library
    include_dirs.append(os.path.join(sys.prefix, r'Library\include'))
    # dlls go in bin, rather than lib (??)
    library_dirs.append(os.path.join(sys.prefix, r'Library\lib'))

    compile_args.append('EHsc')
    link_args.append('/MANIFEST')
elif sys.platform.startswith('linux'):
    library_dirs.append('/usr/local/lib')
    include_dirs.append('/usr/local/include')

## This setup requires libgd
## It expects to find them in the "usual" locations
##   or where Anaconda put it...

ext_modules=[ Extension("py_gd.py_gd",
                        ["py_gd/py_gd.pyx"],
                        include_dirs = include_dirs,
                        library_dirs = library_dirs,
                        libraries=libraries,
                        extra_compile_args = compile_args,
                        extra_link_args = link_args,
                         )]

setup(
    name = "py_gd",
    version='0.1.2',
    description = "python wrappers around libgd graphics lib",
    #long_description=read('README'),
    author = "Christopher H. Barker",
    author_email = "chris.barker@noaa.gov",
    url="https://github.com/NOAA-ORR-ERD/py_gd",
    license = "Public Domain",
    keywords = "graphics cython drawing",
    ext_modules = cythonize(ext_modules),
    zip_safe = False, # dont want a compiled extension in a zipfile...
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

