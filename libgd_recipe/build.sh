#!/bin/sh

# build script for libgd -- tested on OS-X

## this should let configure find the png, etc. libs
export CFLAGS="-I$PREFIX/include $CFLAGS"
export LDFLAGS="-L$PREFIX/lib $LDFLAGS"

## note: missing fontconfig and xpm, because those are not out of the box with anaconda
./configure --prefix=$PREFIX \
            --with-png=$PREFIX \
            --with-freetype=$PREFIX \
            --with-tiff=$PREFIX

make

make install




