#!/usr/bin/env python

import math

def gen_number_row(value, x, y, size=9):

    r = ['0'] * size * size
    r[x * size + y] = '1'

    return ''.join(r)

def gen_row_row(value, x, y, size=9):

    r = ['0'] * size * size
    r[size * y + (value - 1)] = '1'

    return ''.join(r)

def gen_column_row(value, x, y, size=9):

    r = ['0'] * size * size
    r[size * x + (value - 1)] = '1'

    return ''.join(r)

def gen_region_row(value, x, y, size=9):

    r = ['0'] * size * size
    n = int(math.sqrt(size))
    r[size * ((y/n) * n + x/n) + (value - 1)] = '1'

    return ''.join(r)

def gen_row(value, x, y, size=9):

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

def values_from_row(row):
    '''
    given a row from the matrix, figure out the number and the x and y values.
    '''

    size = len(row) / 4
    size = int(math.sqrt(size))

    l = [k[0] for k in enumerate(row) if k[1] == '1']

    ni = l[1] % size + 1
    nx = l[0] / size 
    ny = l[0] % size

    return (ni, nx, ny)

def rownum_from_tuple(t, size=9):
    '''
    t = (value, x, y)
    '''

    return (t[0] - 1) * (size * size) + t[1] * size + t[2]

def tuple_from_rownum(rownum, size=9):

    n = rownum / (size * size) + 1
    r = rownum % (size * size)
    x = r / size
    y = r % size

    return (n, x, y)

if __name__ == '__main__':
    gen_matrix()
