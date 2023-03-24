# test of scanline:
"""
For histories sake -- not py_gd tests here
"""


import numpy as np  # to get an actual 32 bit int


def ip1(y, y1, y2, x1, x2):
    # Here is a python version of the code from gd:
    # print "in ip1"
    # print (x2 - x1).dtype
    # print (y - y1).dtype
    # print ((y - y1) * (x2 - x1)).dtype
    # print
    # print "end ip1"
    return (((y - y1) * (x2 - x1)).astype(np.float32)
            / ((y2 - y1)).astype(np.float32) + 0.5 + x1
            ).astype(np.int32)


def ip2(y, y1, y2, x1, x2):
    # refactored to minimize the overflow
    # this one fails at max value of 4234524 (about 2**22)
    return  (((y - y1).astype(np.float32) /  # noqa: E271
              (y2 - y1).astype(np.float32) *
              (x2 - x1).astype(np.float32)) + 0.5 + x1).astype(np.int32)


def ip3(y, y1, y2, x1, x2):
    # refactored to minimize the overflow
    return  (((y - y1).astype(np.float64) /  # noqa: E271
              (y2 - y1).astype(np.float64) *
              (x2 - x1).astype(np.float64)) + 0.5 + x1).astype(np.int32)


# def ip23(y, y1, y2, x1, x2):
#     #but python and C do different things with truncation negative integers
#     return (int( float( (y - y1) * (x2 - x1) ) /
#                  float( (y2 - y1) ) + 0.5 + x1
#                   ))

# for a easy analytical example:
# diagonal line


largest = 2**31 - 1
fail_orig = None
fail_float = None
fail_double = None
for max in range(32000, largest, 10):
    # put it in a numpy array to force int32
    max = np.array((max,), dtype=np.int32)

    x1, y1 = -max, -max
    x2, y2 = max, max

    y = 500  # arbitrary reasonable number
    ip_1 = ip1(y, y1, y2, x1, x2)[0]
    ip_2 = ip2(y, y1, y2, x1, x2)[0]
    ip_3 = ip3(y, y1, y2, x1, x2)[0]

#    print("intersecting points for max: {}, y: {}".format(max, y) , ip_1, ip_2, ip_3)

    if y != ip_1:
        if fail_orig is None:
            fail_orig = max
        print("original failed")
    if y != ip_2:
        if fail_float is None:
            fail_float = max
        print("new with float failed")
        break
    if y != ip_3:
        if fail_double is None:
            fail_double = max
        print("new with double failed")
        break

print("Original version failed at:", fail_orig)
print("New float version failed at:", fail_float)
print("New double version failed at:", fail_double)
