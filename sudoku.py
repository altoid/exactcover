#!/usr/bin/env python

import math

def gen_number_row(value, x, y, size):

    r = ['0'] * size * size
    r[x * size + y] = '1'

    return ''.join(r)

def gen_row_row(value, x, y, size):

    r = ['0'] * size * size
    r[size * y + (value - 1)] = '1'

    return ''.join(r)

def gen_column_row(value, x, y, size):

    r = ['0'] * size * size
    r[size * x + (value - 1)] = '1'

    return ''.join(r)

def gen_region_row(value, x, y, size):

    r = ['0'] * size * size
    n = int(math.sqrt(size))
    r[size * ((y/n) * n + x/n) + (value - 1)] = '1'

    return ''.join(r)

def gen_row(value, x, y, size):

    npart = gen_number_row(value, x, y, size)
    rowpart = gen_row_row(value, x, y, size)
    colpart = gen_column_row(value, x, y, size)
    regpart = gen_region_row(value, x, y, size)

    result = npart + rowpart + colpart + regpart

    return result

def gen_matrix(size=9):

    # gratuitous column header
    print 'x' * 4 * size * size
    for i in range(1, size + 1):
        for x in range(size):
            for y in range(size):
                print gen_row(i, x, y, size)

if __name__ == '__main__':
    gen_matrix()
