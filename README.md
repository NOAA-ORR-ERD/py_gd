# `py_gd`

Python wrappers for libgd graphics drawing lib.

Welcome to the `py_gd` project.

py_gd aims to provide nice Pythonic wrappers around libgd -- a robust, fast, and simple drawing lib:

Docs here:

https://noaa-orr-erd.github.io/py_gd/

Code here:

https://github.com/libgd/libgd/

## Why gd?

For the project at hand we needed fast and simple drawing -- 8-bit color, no anti-aliasing.
We also wanted a nice simple API to work with. There are a number of newer drawing libs (AGG, Skia)
that produce some pretty results, but are not as simple to use, and are focused on 32 bit fully
anti-aliased drawing. If you want the prettiest rendering possible, I encourage you to check those out.

If you want something fast and simple -- `py_gd` may be for you.

## Why a new python wrapper for gd?

`gdmodule` (gitHub: https://github.com/Solomoriah/gdmodule) is a wrapper
for gd that has been around along time. However:
 - It appears to be unmaintained (last touched 12 years ago as of this writing)
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

### Run Time

At run time, `py_gd` currently requires the numpy package: http://www.numpy.org, but nothing else.

numpy is used to allow you to efficiently pass in data structures for things like vertices of large polygons, etc, and can be used to get a copy of the image buffer, and manipulate it in various ways, as well as passing it back to `py_gd`.

### Build Time

In order to build `py_gd`, the Cython package is also required: http://cython.org/

Most critically, `py_gd` requires the `libgd` libary, which itself requires a number of other libs, such as `libpng`, `libjpeg`, etc, etc...

See the Install section for more info

## Is `py_gd` a complete wrapper around gd?

In a word: no.

`py_gd` was developed to meet particular needs, and is not the least bit complete. It does, however have enough to be useful (at least to us).

Major Working features:
 * 8-bit "paletted" images
 * transparent background
 * built-in fonts for text
 * lines, polygons, arcs
 * cubic spline support (not in libgd itself)
 * copying between images
 * saving as gif, bmp, png, jpeg, and animated gif.
 * numpy arrays for input and image buffer exchange.

Major Missing features:
 * 32bit "truecolor" support
 * loading images from gif, png, etc... (not hard to add, just haven't needed it)
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

`py_gd` depends on libgd which, in turn, depends on libpng, and others -- this makes it a major pain to build yourself. We suggest using conda via miniconda, miniforge, or pixi, and the conda packages found in the conda-forge channel. It should be as easy as:

```
conda install -c https://conda.anaconda.org/conda-forge py_gd
```

This currently works on Mac, Windows and Linux

## pip installing

We try to maintain packages on PyPi, but they are only source packages -- they will need to be built to work. This is fairly straightforward on Linux, but a serious challenge on Windows and Mac.

NOTE: we are working on pre-built wheels for all major platforms -- stay tuned!

Contributions to the effort would be happily accepted: see:

https://github.com/NOAA-ORR-ERD/py_gd/issues/34

For progress.

# Building

## Windows

`py_gd` depends on libgd which, in turn, depends on libpng, and others -- this makes it a major pain to build on Windows.

So far, folks have had the most luck with using the vcpkg system.

https://vcpkg.io/en/index.html

`libgd` is on there, and theoretically can simply be installed::

  vcpkg install libgd

Once vcpkg is setup up properly -- I am no expert on this -- let us know if it works for you, and if you needed to do anything special.


## OS-X

`py_gd` depends on libgd which, in turn, depends on libpng, and others -- You can use macports or homebrew or vcpkg to roll your own to get these, and then the build should work.

We have not tested this ourselves -- let us know what works for you.

## Linux

`py_gd` depends on libgd, which may be available in your distro's repo (it's used heavily by PHP).


`py_gd` requires libgd version >= 2.3. If your Linux distro has an up to date version, you can probably simply install it (and the development headers) from the system repos. something like:

```bash
apt-get install libgd, libgd-dev
```
or similar yum command (maybe just ``gd`` rather than ``libgd``

Once the library and headers are installed to "normal" locations,
the py_gd build system should find them



## Building `py_gd`

### get the source:

You can get the source:

* From PyPI:

* From a [release on GitHub:](https://github.com/NOAA-ORR-ERD/py_gd/releases)

* By cloning the [`py_gd` repository](https://github.com/NOAA-ORR-ERD/py_gd) to your local machine


It's a good idea to create a venv, virtualenv or conda environment to scope your python installations to this project.

### Install the requirements

 * with conda:
   - `conda install --file conda_requirements.txt --file conda_requirements_dev.txt`

 * with pip:
   - pip install cython numpy pytest

 * cd into the repo

### Build and Install

Run these commands:

```bash
$ python -m pip install .
```

If you want to work on the source, you'll want an "editable" install:

```bash
$ python -m pip install -e .
```

### testing

The tests require pytest -- if you haven't used the conda_requirements_dev.txt, you will need to install it:

```bash
$ python -m pip install pytest
```
or

```bash
$ conda install pytest
```

Then run the tests:

```bash
$ pytest --pyargs py_gd
```

That will ensure the installed tests run.

or

```bash
$ pytest py_gd/test
```

That will run the tests in the source -- helpful if you want to debug or add tests.

The tests output a number of images -- these are checked against stored checksums for the tests.

But if anything doesn't match, a test may fail. You can look in `test_images_output` dir in the test dir.

