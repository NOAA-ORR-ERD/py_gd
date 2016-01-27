#!/usr/bin/env python

"""
tests for buffer access to py_gd Image
"""

import py_gd

import pytest

## skip this until we get it working...
@pytest.mark.skipif('True')
def test_mem_view():
    img = py_gd.Image(5,10)

    print img

    #get a memoryview of it:
    m = memoryview(img)
    print m
    print m.format
    print m.ndim    
    print m.shape  
    print m.suboffsets
    print m.itemsize
    print m.readonly
    print m.strides
    print m.tobytes()
    print m.tolist()

    assert False
