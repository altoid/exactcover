#!/usr/bin/env python

import sets
import copy

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

        for p in self:
            x = p[0] - self._minx
            y = p[1] - self._miny
            arr[y][x] = '*'

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

def piece_rows(piece, w, h, nothere=()):

    '''
    nothere is a list of coordinates which may
    not have a piece placed on them.
    '''

    x = y = 0
    piece = piece.moveto(x, y)
    while piece._maxy < h:
        while piece._maxx < w:
            i = piece.intersection(nothere)
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

def piece_placements(piece, w, h, nothere=()):

    '''
    nothere is a list of coordinates which may
    not have a piece placed on them.
    '''

    x = y = 0
    p = piece.moveto(x, y)
    while p._maxy < h:
        while p._maxx < w:
            i = p.intersection(nothere)
            if len(i) == 0:
                yield p
            x += 1
            p = p.moveto(x, y)
        x = 0
        y += 1
        p = p.moveto(x, y)

def all_arrangements(piece, w, h, nothere=()):

    for i in orientations(piece):
        for row in piece_rows(i, w, h, nothere):
            yield ''.join(row)

if __name__ == '__main__':

    center = set([(3,3),(3,4),(4,3),(4,4)])

    all_pieces = list('nluxwpftvyzi')
    w = h = 8
    column_headers = all_pieces + ['b'] * (w * h)
    print ''.join(column_headers)
    for name in all_pieces:
        prelude = ['0'] * len(all_pieces)
        prelude[all_pieces.index(name)] = '1'
        prelude = ''.join(prelude)

        piece = make_piece(name)
        for a in all_arrangements(piece, w, h, center):
            print prelude + a
