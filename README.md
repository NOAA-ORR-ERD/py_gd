# `py_gd`

Python wrappers for libgd graphics drawing lib.

Welcome to the `py_gd` project.

py-gd aims to provide nice Pythonic wrappers around libgd -- a robust, fast, and simple drawing lib:

https://github.com/libgd/libgd/

## Why gd?

For the project at hand we needed fast and simple drawing -- 8-bit color, no anti-aliasing.
We also wanted a nice simple API to work with. There are a number of newer drawing libs (AGG, Skia)
that produce some pretty results, but are not as simple to use, and are focused on 32 bit fully
anti-aliased drawing. If  you want the prettiest rendering possible, I encourage you to check those out.

If you want something fast and simple -- `py_gd` may be for you.

## Why a new python wrapper for gd?

`gdmodule` (recently moved to gitHub: https://github.com/Solomoriah/gdmodule) is a wrapper
for gd that has been around along time. However:
 - It appears to be minimally maintained
 - It is a pretty direct wrapper around the gd old-style-C API
 - It is hand-written C extension code -- more or less the state of the art for 1995
   when it was first written, but I really don't want to work on that code!

On the other hand:
 - `py_gd` is being actively maintained.
 - `py_gd` is a "thick" wrapper -- we're trying to provide a nice object oriented, Pythonic interface.
 - `py_gd` uses numpy (and the PEP3118 buffer interface) to allow efficient transfer of data back and forth between Python and gd.
 - `py_gd` is written in Cython, which is likely to be more robust and error free and easier to maintain.

However, there is some nice stuff in gdmodule (like including a truetype font) that we want to borrow at some point.

## How is `py_gd` built?

`py_gd` is built using Cython: (www.cython.org). Cython allows us to both call into the existing gd C lib, and to also write wrapper code to make a nicer API in an efficient way. You shouldn't need Cython to use `py_gd`, but you'll need it if you want to contribute to the wrappers or compile the code yourself.


## Dependencies:

`py_gd` currently requires the numpy package: http://www.numpy.org

numpy is used to allow you to efficiently pass in data structures for things like vertices of large polygons, etc, and can be used to get a copy of the image buffer, and manipulate it in various ways, as well as passing it back to `py_gd`.

In order to build `py_gd`, the Cython package is also required: http://cython.org/

## Is `py_gd` a complete wrapper around gd?

In a word: no.

`py_gd` was developed to meet particular needs, and is not the least bit complete. It does, however have enough to be useful (at least to us).

Major Working features:
 * 8-bit "paletted" images
 * transparent background
 * built-in fonts for text
 * lines, polygons, arcs
 * copying between images
 * saving as gif, bmp, png, jpeg, and animated gif.
 * numpy arrays for input and image buffer exchange.

Major Missing features:
 * 32bit "truecolor" support
 * loading images from gif, png, etc...
 * freetype fonts
 * image manipulations: scaling, etc

## Can I contribute?

You sure can -- fork the source, and hack away -- you can actually add features pretty easily by taking a look at what's there -- with just a little C and/or Cython knowledge (not much!) you should be able to get stuff working.

Here's what you need to do:

 * Find the function you want to wrap in gd.h
 * Copy the prototype to `py_gd.pxd`, and edit it to make it
   Cython-compatible (copy what's done for the ones already there)
 * Add a method to the Image class in `py_gd.pyx` -- look for similar
   methods already, and try to keep the API similar.
 * Add a test to `test_gd.py` (Or a new test file) that tests your new
   method
 * Re-build (``pip install -e ./``
 * Try out your test...
 * Lather, rinse, repeat, 'till it all works

# Install

`py_gd` depends on libgd which, in turn, depends on libpng, and others -- this makes it a major pain to build yourself. we suggest using conda via Anaconda or miniconda, and the conda packages found in the conda-forge channel. It should be as easy as:

```
conda install -c https://conda.anaconda.org/conda-forge py_gd
```

This currently works on Mac, Windows and Linux

## pip installing

We try to maintain pacakges on PyPi, but they are only source packages -- they will need to be built to work. This is fairly straightforward on Linux, but a serious challenge on Windows and Mac. NOTE: contributions of wheels would be happily accepted.

# Building

## Windows

`py_gd` depends on libgd which, in turn, depends on libpng, and others -- this makes it a major pain to build on Windows.

Folks have had some luck getting it going with the newer Windows clib providers.


## OS-X

`py_gd` depends on libgd which, in turn, depends on libpng, and others -- You can use macports or homebrew or roll your own to get these, and then the build should work.


## Linux

`py_gd` depends on libgd, which may be available in your distro's repo (it's used heavily by PHP). However your distro's version may be too old for `py_gd`, so you may have to built it yourself.

### building libgd

`py_gd` requires libgd version >= 2.3. If your Linux distro has an up to date version, you can probably simply install it (and the development headers) from the system repos. something like:

```bash
apt-get install libgd, libgd-dev
```
or similar yum command (maybe just ``gd`` rather than ``libgd``

### (CentOS 7)

centoOS 7 only has version 2.0 in it's standard repos, as of 10/22/2015, so you need to download the source and build it yourself.

 * Download the libgd version 2.1.1 tar file from [bitbucket](https://bitbucket.org/libgd/gd-libgd/downloads) (there are also tarballs on GitHub, but these don't have a configure script ready to go)
 * Build the tar file from source and install it. The usual:

```bash
$ ./configure
$ make
$ make install
```

dance. This will install into ``/usr/local/`` if you use the defaults. If your system is not yet set up to find libraries in ``/usr/local/``, then you need to add this line to your bashrc:

```bash 
export LD_LIBRARY_PATH='/usr/local/lib'
```
(or set that globally) It needs to be set whenever you are running `py_gd`.

Note: If you determine that you lack jpeg support these libs are known to be compatible and can be installed through yum:

* libjpeg-turbo-devel
* libjpeg-turbo

## Building `py_gd`

 * Clone the [`py_gd` repository](https://github.com/NOAA-ORR-ERD/py_gd) to your local machine
 * Create a virtualenv or conda environemnt to scope your python installations to this project (<i>optional</i>)

 * with conda:
   - `conda install --file conda_requirements.txt --file conda_requirements_dev.txt`
 * with pip:
   - pip install cython numpy pytest

 * cd into the repo

 * run these commands:

```bash
$ pip install ./
```

 * pip install pytest and run py.test to see that everything is working:

```bash
$ py.test --pyargs py_gd 
```
 
