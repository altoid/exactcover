#!/usr/bin/env python

import sets
import copy

class Board:

    '''
        x ---->

    y
    |
    |
    V

    '''
    def clear(self):

        self._array = []

        for i in range(self._height):
            e = ['-'] * (4 * self._width)
            for i in range(0, len(e), 4):
                e[i] = '+'
            e.append('+')
            self._array.append(e)

            e = [' '] * (4 * self._width)
            for i in range(0, len(e), 4):
                e[i] = '|'

            e.append('|')
            self._array.append(e)

        e = ['-'] * (4 * self._width)
        for i in range(0, len(e), 4):
            e[i] = '+'
        e.append('+')
        self._array.append(e)

    def __init__(self, width, height):

        self._height = height
        self._width = width

        self.clear()

    def mark(self, pt):
        x = 2 + 4 * pt[0]
        y = 1 + 2 * pt[1]
        self._array[y][x] = '*'

    def connect(self, pt0, pt1):

        self.mark(pt0)
        self.mark(pt1)

        x0 = min(2 + 4 * pt0[0], 2 + 4 * pt1[0])
        x1 = max(2 + 4 * pt0[0], 2 + 4 * pt1[0])

        y0 = min(1 + 2 * pt0[1], 1 + 2 * pt1[1])
        y1 = max(1 + 2 * pt0[1], 1 + 2 * pt1[1])

        if x0 == x1:
            for i in range(y0, y1, 2):
                self._array[i][x0] = '*'
                self._array[i + 1][x0] = '*'
                self._array[i + 1][x0 - 1] = ' '
                self._array[i + 1][x0 + 1] = ' '
        else:
            for i in range(x0, x1):
                self._array[y0][i] = '*'

    def print_(self):
        for a in self._array:
            print ''.join(a)

    def place_piece(self, piece, x, y):

        piece = piece.moveto(x, y)
        clist = list(piece)
        print clist

        l = len(clist)
        for i in range(l - 1):
            for j in range(i, l):
                if (clist[i][0] == clist[j][0]) or (clist[i][1] == clist[j][1]):
                    self.connect(clist[i], clist[j])

    def set_space(self, x, y):

        self._array[y][x] = 1

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
