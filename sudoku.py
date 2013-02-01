#!/usr/bin/env python

import math
import sys
import dl

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

def rows_to_tableau(row_nums, size):

    # this doesn't work
#    tableau = [[0] * size] * size

    tableau = []
    for i in range(size):
        tableau.append([0] * size)

    for rn in row_nums:
        value, x, y = tuple_from_rownum(rn, size)
        tableau[y][x] = value

    return tableau

def tableau_from_file(filename):
    '''
    file format:
    first line is sudoku size, e.g. 4 or 9
    rest of file is the tableau, with 0 for missing values.

    returns the size and a list of the row numbers in the data matrix that correspond to
    the values in the tableau.
    '''

    f = open(filename)
    line = f.readline()
    size = int(line)

    row_vectors = []
    initial_rows = []
    y = 0
    for line in f:
        elements = [int(x) for x in line.split()]

        x = 0
        for n in elements:
            if n > 0:
                r = rownum_from_tuple((n, x, y), size)
                initial_rows.append(r)
                row = gen_row(n, x, y, size)
                row_vector = [int(b) for b in list(row)]
    
#                print ''.join(['1' if b else '.' for b in row_vector]),
#                print '(n = %d, x = %d, y = %d) ==> %d' % (n, x, y, r)
                row_vectors.append(row_vector)
            x += 1
        y += 1

    # sum each the columns.  4 is fixed; it is the number
    # of sets of columns in the data matrix, one for each of
    # (value, row, column, region)

    rowlength = 4 * size * size
    for i in range(rowlength):
        c = [v[i] for v in row_vectors]
        if sum(c) > 1:
            print 'this tableau is ca-ca.'
            sys.exit(1)

    return size, initial_rows

def print_tableau(tableau):

    size = len(tableau)
    squirt = int(math.sqrt(size))

    y = 0
    for r in tableau:

        if y % squirt == 0:
            e = ''
            for x in range(size):
                e += '%s---' % ('+' if x % squirt == 0 else '-')
            e += '+'
        else:
            a = [' '] * 4 * size
            for i in range(4 * size):
                if i % (squirt * 4) == 0:
                    a[i] = '|'
            e = ''.join(a)
            e += '|'
        print e

        e = ''
        x = 0
        for i in r:
            e += '%s %d ' % ('|' if x % squirt == 0 else ' ', i)
            x += 1
        e += '|'
        print e

        y += 1

    e = ''
    for x in range(size):
        e += '%s---' % ('+' if x % squirt == 0 else '-')
    e += '+'
    print e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "arg count:  |%s|" % (''.join(sys.argv))
        sys.exit(1)

    size, initial_rows = tableau_from_file(sys.argv[1])

    initial_tableau = rows_to_tableau(initial_rows, size)
    for row in initial_tableau:
        print row

    print 'seed:', initial_rows

    datafile = 'sudoku%d_data.txt' % size

    matrix = dl.matrix_from_file(datafile)

    dlx = dl.DLXAlgorithm(matrix, seeds=initial_rows)

    dlx.dlx1()

    for s in dlx.solutions:
        solution_tableau = rows_to_tableau(s, size)
        print '=' * 44
        print s
        print_tableau(solution_tableau)
    
