#!/usr/bin/env python

"""
tests for buffer access to py_gd Image
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import pytest

from py_gd import Image


# skip this until we get it working...
@pytest.mark.skipif('True')
def test_mem_view():
    img = Image(5, 10)

    print(img)

    # get a memory view of it:
    m = memoryview(img)
    print(m)
    print(m.format)
    print(m.ndim)
    print(m.shape)
    print(m.suboffsets)
    print(m.itemsize)
    print(m.readonly)
    print(m.strides)
    print(m.tobytes())
    print(m.tolist())

    assert False
