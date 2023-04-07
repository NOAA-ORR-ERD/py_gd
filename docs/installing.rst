Installing
==========

py_gd is written in Cython (http://www.cython.org) and depends on the gd library (http://libgd.bitbucket.org/)

You need libgd compiled (with support for image formats you want..)


conda
-----

The easiest way to install is via conda -- we provide conda packages on conda-forge.

``conda install -c conda-forge py_gd``

pip
---

We try to maintain pacakges on PyPi, but they are only source packages -- they will need to be built to work. This is fairly straightforward on Linux, but a serious challenge on Windows and Mac. NOTE: contributions of wheels would be happily accepted.

Building it yourself
--------------------


Windows
.......

``py_gd`` depends on libgd which, in turn, depends on libpng, and others -- this makes it a major pain to build on Windows.

Folks have had some luck getting it going with the newer Windows clib providers.


OS-X
....

``py_gd`` depends on libgd which, in turn, depends on libpng, and others -- You can use macports or homebrew or roll your own to get these, and then the build should work.


Linux
.....

``py_gd`` depends on libgd, which may be available in your distro's repo (it's used heavily by PHP). However your distro's version may be too old for `py_gd`, so you may have to built it yourself.

Building libgd
,,,,,,,,,,,,,,

``py_gd`` requires libgd version >= 2.3. If your Linux distro has an up to date version, you can probably simply install it (and the development headers) from the system repos. something like:

.. code-block:: bash

    apt-get install libgd, libgd-dev

or similar yum command (maybe just ``gd`` rather than ``libgd``

(CentOS 7)
,,,,,,,,,,


centoOS 7 only has version 2.0 in it's standard repos, as of 10/22/2015, so you need to download the source and build it yourself.

 * Download the libgd version 2.1.1 tar file from [bitbucket](https://bitbucket.org/libgd/gd-libgd/downloads) (there are also tarballs on GitHub, but these don't have a configure script ready to go)
 * Build the tar file from source and install it. The usual:

.. code-block:: bash

    $ ./configure
    $ make
    $ make install

dance. This will install into ``/usr/local/`` if you use the defaults. If your system is not yet set up to find libraries in ``/usr/local/``, then you need to add this line to your bashrc:

.. code-block:: bash

  export LD_LIBRARY_PATH='/usr/local/lib'

(or set that globally) It needs to be set whenever you are running ``py_gd``.

Note: If you determine that you lack jpeg support these libs are known to be compatible and can be installed through yum:

* libjpeg-turbo-devel
* libjpeg-turbo

Building ``py_gd``
..................

 * Clone the [``py_gd`` repository](https://github.com/NOAA-ORR-ERD/py_gd) to your local machine
 * Create a virtualenv or conda environemnt to scope your python installations to this project (<i>optional</i>)

 * with conda:
   - `conda install --file conda_requirements.txt --file conda_requirements_dev.txt`
 * with pip:
   - pip install cython numpy pytest

 * cd into the repo

 * run these commands:

.. code-block:: bash

    $ pip install ./


 * pip install pytest and run py.test to see that everything is working:

.. code-block:: bash

    $ py.test --pyargs py_gd

