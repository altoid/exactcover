#!/usr/bin/env python

import sets

class Board:

    def __init__(self, side=8):

        self._side = side

        self._array = []

        for i in range(self._side):
            self._array.append([0] * self._side)

    def _print_edge(self):

        e = ''

        for i in range(self._side):
            e += '+---'
        e += '+'
        print e

    def _print_row(self, row):

        e = ''
        for v in row:
            e += '| %s ' % ('*' if v == 1 else ' ')
        e += '|'
        print e
        
    def print_(self):
        for a in self._array[::-1]:
            self._print_edge()
            self._print_row(a)

        self._print_edge()

    def place_piece(self, piece, x, y):

        piece = piece.moveto(x, y)
        print piece

        for p in piece:

            self.set_space(p[0], p[1])

    def set_space(self, x, y):

        self._array[y][x] = 1

    def clear(self):

        self._array = []

        for i in range(self._side):
            self._array.append([0] * self._side)

class Piece(sets.ImmutableSet):

    # standard XY coordinate system

    def __set_bounding_box(self):

        minx = miny = maxx = maxy = None
        for p in self:

            minx = p[0] if minx is None else minx
            miny = p[1] if miny is None else miny

            minx = p[0] if p[0] < minx else minx
            miny = p[1] if p[1] < miny else miny

            maxx = p[0] if maxx is None else maxx
            maxy = p[1] if maxy is None else maxy

            maxx = p[0] if p[0] > maxx else maxx
            maxy = p[1] if p[1] > maxy else maxy

        self._minx = minx
        self._miny = miny
        self._maxx = maxx
        self._maxy = maxy

    def __init__(self, points):

        super(Piece, self).__init__(points)
        self.__set_bounding_box()

    def flip_y(self):

        l = [(-x[0], x[1]) for x in self]
        return Piece(l)

    def flip_x(self):
        '''
        returns a new Piece object
        '''
        l = [(x[0], -x[1]) for x in self]
        return Piece(l)

    def clockwise_90(self):

        l = [(x[1], -x[0]) for x in self]
        return Piece(l)

    def counterclockwise_90(self):

        l = [(-x[1], x[0]) for x in self]
        return Piece(l)

    def moveto(self, x, y):
        '''
        translate so that (minx, miny) of the bounding box of the piece
        is at x, y.
        '''

        dx = x - self._minx
        dy = y - self._miny

        l = set([(x[0] + dx, x[1] + dy) for x in self])
        return Piece(l)

    def __str__(self):

        result = '';

        arr = []

        w = self._maxx - self._minx + 1
        h = self._maxy - self._miny + 1
        for i in range(h):
            arr.append([' '] * w)

        t = self.moveto(0, 0)
        for p in t:
            print p,
        print
        for p in t:
            arr[p[1]][p[0]] = '*'

        for i in range(h):
            result += ''.join(arr[i])
            result += '\n'

        return result[:-1]

def orientations(piece):

    sofar = set()

    piece = piece.moveto(0,0)
    sofar.add(piece)
    yield piece

    piece = piece.clockwise_90().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

    piece = piece.clockwise_90().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

    piece = piece.clockwise_90().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

    piece = piece.flip_y().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

    piece = piece.clockwise_90().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

    piece = piece.clockwise_90().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

    piece = piece.clockwise_90().moveto(0,0)
    if piece not in sofar:
        sofar.add(piece)
        yield piece

def make_piece(filename):

    f = open('pentominoes/' + filename)

    points = set()
    y = 0
    for line in f:
        bits = line.split()
        x = 0
        for b in bits:
            if b == '1':
                points.add((x, y))
            x += 1

        y += 1

    return Piece(points)

center = set([(3,3),(3,4),(4,3),(4,4)])

def count_piece_placements(piece):

    global center

    count = 0
    x = y = 0
    piece = piece.moveto(x, y)

    while piece._maxy < 8:
        while piece._maxx < 8:
            i = center.intersection(piece)
            if len(i) == 0:
                count += 1
            x += 1
            piece = piece.moveto(x, y)
        x = 0
        y += 1
        piece = piece.moveto(x, y)

    return count

def piece_rows(piece, w, h):

    global center

    x = y = 0
    piece = piece.moveto(x, y)
    while piece._maxy < h:
        while piece._maxx < w:
            i = piece.intersection(center)
            if len(i) == 0:
                row = ['0'] * (w * h)
                for pt in piece:
                    row[pt[1] * w + pt[0]] = '1'
                yield row
            x += 1
            piece = piece.moveto(x, y)
        x = 0
        y += 1
        piece = piece.moveto(x, y)

def print_all_arrangements(w, h):

    all_pieces = list('nluxwpftvyzi')
    column_headers = all_pieces + ['b'] * (w * h)
    print ' '.join(column_headers)
    for n in all_pieces:
        p = make_piece(n)
        prelude = ['0'] * len(all_pieces)
        prelude[all_pieces.index(n)] = '1'
        for i in orientations(p):
            for row in piece_rows(i, w, h):
                k = prelude + row
                print ' '.join(k)

if __name__ == '__main__':

    print_all_arrangements(8, 8)

#    p = make_piece('y')
#    print_piece_rows(p)
