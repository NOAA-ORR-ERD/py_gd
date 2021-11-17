.. _reference:

``py_gd`` Reference
===========================

``py_gd`` is a python wrapper around the GD graphics library. For the real detail, see the source and docs of GD itself:

https://github.com/libgd/libgd

This is the documentation for the python inteface -- it more or less mirrors the GD API, but makes it more object oriented and generally uses "pythonic" names and style.

Notes:
------

There is a module attribute: ``MAX_IMAGE_SIZE``. It is currently set 1GB. It can be changed after import, before initializing an Image. On the develoment system, creating images greater than 1GB brings the system to an almost halt before raising a memory error. But your machine may be able to tolerae larger images. Hoever, as of this writting, pixel coordintes are C ``int`` type, so very parge images may have issues anyway

If you want to change it:

from py_gd import py_gd  # to get the actual cython module

py_gd.MAX_IMAGE_SIZE = 4 * 1024**3  # 4 GB

Then you can create a larger Image


Class Reference:
----------------

.. automodule:: py_gd
   :members:

``py_gd.Image`` -- the gd image class
-------------------------------------
.. autoclass:: py_gd.Image 
   :members:

Factory functions
-----------------
.. autofunction:: py_gd.from_array
