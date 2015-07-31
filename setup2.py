#!/usr/bin/env python

"""
This version builds all of gd into the extension, rather than separately.

setup.py script for the py_gd package

not sure when/if this worked, but it's not maintained.

"""

import sys, os

from setuptools import setup

#from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy #for the include dirs...

## total kludge here: for building libpng 
## you should be able to replace these for an installed  png lib.

static_libs = ["./static_libs/lib/libpng.a"]

includes    = ["./static_libs/include/png.h",
               ]

include_dirs = [os.path.split(filename)[0] for filename in includes]
include_dirs = list(set(include_dirs)) # remove the duplicates

need_to_build = []
for lib in static_libs:
    if not os.path.isfile(lib):
        need_to_build.append(lib)

print need_to_build

all_args = " ".join(sys.argv[1:])
if 'build' in all_args or 'develop' in all_args or 'install' in all_args:
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


## code for building gd into the extension...
gd_source_dir = os.path.join('.','libgd-2.1.0/','src/')
gd_source_files = gd_source_files = [ name for name in os.listdir(gd_source_dir)
                                      if ( name.split('.')[-1] =='c'
                                           and ( name.startswith('gd_')
                                                 or name.startswith('gdfont')
                                                 or name in ('gd.c', 'gdtables.c', 'wbmp.c', 'gdhelpers.c')
                                                )
                                           ) ]

gd_source_files = [os.path.join(gd_source_dir, name) for name in gd_source_files]
print gd_source_files

## setting some macros for gd compilation 
macros = []
if sys.platform == 'win32':
    pass

elif sys.platform == 'darwin':
    macros.extend( [ ('HAVE_STDINT_H', 1),
                     ('HAVE_LIBJPEG', 1),
                     ('HAVE_LIBPNG', 1)
                     ] )

elif sys.platform == "linux2":
    macros.append( ('HAVE_STDINT_H', 1) ) # just guessing here..

ext_modules=[ Extension("py_gd.py_gd",
                        gd_source_files + ["py_gd/py_gd.pyx"],
                        define_macros=macros,
                        include_dirs = [gd_source_dir,
                                        "./static_libs/include/",
                                        numpy.get_include(),
                                        ],
                        libraries=["jpeg"],
                        #library_dirs=["/usr/local/lib", #for jpeg
                        #             ],
                        extra_objects=["./static_libs/lib/libpng.a"],
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


