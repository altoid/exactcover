#!/usr/bin/env python

def xyz_to_cell(t, size=5):

    x, y, z = t
    return z * size * size + y * size + x

def cell_to_xyz(n, size=5):

    z = n / (size * size)
    r = n % (size * size)
    y = r / size
    x = r % size

    return x, y, z
