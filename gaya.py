#!/usr/bin/env python

import pentominoes
import dl

def xyz_to_cell(t, size=5):

    x, y, z = t
    return z * size * size + y * size + x

def cell_to_xyz(n, size=5):

    z = n / (size * size)
    r = n % (size * size)
    y = r / size
    x = r % size

    return x, y, z

def translate_to_plane(piece, xplane=None, yplane=None, zplane=None, size=5):

    v = [0] * 3
    v[0] = 0 if xplane is None else 1
    v[1] = 0 if yplane is None else 1
    v[2] = 0 if zplane is None else 1

    if sum(v) != 1:
        raise ValueError("translate_to_plane called stupidly")

    result = []

    if zplane is not None:
        result = [(pt[0], pt[1], zplane) for pt in piece]

    if yplane is not None:
        result = [(pt[0], yplane, pt[1]) for pt in piece]

    if xplane is not None:
        result = [(xplane, pt[0], pt[1]) for pt in piece]

    return result

def find_outlier(pts):
    '''
    pts is the coordinates of a y-piece in 3 space.  find
    the coordinates of the 'knob'.
    '''
    all_x = {}
    all_y = {}
    all_z = {}

    # find the axis where there are exactly 4 of the same value
    for p in pts:
        x, y, z = p
        if not x in all_x:
            all_x[x] = 0
        all_x[x] += 1

        if not y in all_y:
            all_y[y] = 0
        all_y[y] += 1

        if not z in all_z:
            all_z[z] = 0
        all_z[z] += 1

#    print all_x
#    print all_y
#    print all_z

    c = []
    if len(all_x.keys()) == 2:
        c = [i for i in all_x.items() if i[1] == 1]
        item = c[0]
        knob = [k for k in pts if k[0] == item[0]]
    elif len(all_y.keys()) == 2:
        c = [i for i in all_y.items() if i[1] == 1]
        item = c[0]
        knob = [k for k in pts if k[1] == item[0]]
    elif len(all_z.keys()) == 2:
        c = [i for i in all_z.items() if i[1] == 1]
        item = c[0]
        knob = [k for k in pts if k[2] == item[0]]
    else:
        raise ValueError('oh shit')

    return knob[0]

def make_row(pts, size=5):

    cells = [xyz_to_cell(x) for x in pts]
    row = ['0'] * (size ** 3)
    for c in cells:
        row[c] = '1'
    return ''.join(row)

def spin(size=5):

    '''
    generate 3-space coordes for every orientation of a piece
    '''
    ypiece = pentominoes.make_piece('y')

    for o in pentominoes.orientations(ypiece):
        for p in pentominoes.piece_placements(o, size, size):

            for plane in range(size):
                three_d = translate_to_plane(p, zplane=plane)
                yield three_d

            for plane in range(size):
                three_d = translate_to_plane(p, xplane=plane)
                yield three_d

            for plane in range(size):
                three_d = translate_to_plane(p, yplane=plane)
                yield three_d

def print_matrix():

    size = 5

    column_headers = 'x' * (size ** 3)

    for point_vector in spin(size):

        print make_row(point_vector, size)

def solve():

    matrix = dl.matrix_from_file('gaya.txt')

#    matrix.add_column_headers([str(x) for x in range(size ** 3)])
#
#    all_rows = []
#    for point_vector in spin(5):
#        
#        r = list(make_row(point_vector, size))
#        all_rows.append(r)
#        matrix.add_row(r)
#
##        knob = find_outlier(point_vector)
##        cell = xyz_to_cell(knob, size)
##        print r
#
#
    initial_rows = [100]
    dlx = dl.DLXAlgorithm(matrix, seeds=initial_rows)

    dlx.dlx1()

    scount = 0
    for s in dlx.solutions:
        print s
        scount += 0

    print '%d solutions' % scount

if __name__ == '__main__':
    solve()

