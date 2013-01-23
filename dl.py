#!/usr/bin/python

import sys

class ColumnHeader:

    def __init__(self, name, col_number=0):

        self._name = name
        self._n = col_number
        self.l = self.r = self.u = self.d = self

    @property
    def name(self):
        return self._name

    @property
    def n(self):
        return self._n

    @property
    def empty(self):
        return self.d == self

    def __str__(self):
        return self._name

class RowHeader:

    def __init__(self, row_number):

        self._n = row_number
        self.l = self.r = self.u = self.d = self

    @property
    def n(self):
        return self._n

class DataObject:

    def __init__(self, row_header, column_header):

        self.l = self.r = self.u = self.d = self
        self.c = None
        self._row_header = row_header
        self._column_header = column_header

    @property
    def row_header(self):
        return self._row_header

    @property
    def column_header(self):
        return self._column_header

class Matrix:

    def __init__(self):
        self.root = ColumnHeader('root')
        self.ncolumns = 0
        self._covered_columns = []
        self._row_headers = []

    @property
    def empty(self):
        return self.root.l == self.root

    @property
    def column_headers(self):
        result = ''

        ch = self.root.r
        while ch != self.root:
            result = result + ch.name + ' '
            ch = ch.r

        return result

    def add_column_headers(self, column_names):

        for i, n in enumerate(column_names):
            column_header = ColumnHeader(n, i)
            self.root.l.r = column_header
            column_header.r = self.root
            column_header.l = self.root.l
            self.root.l = column_header
        self.ncolumns = len(column_names)

    def add_row(self, bits):

        # the row headers are just to aid in traversal.  nothing in
        # the array points to them.

        row_number = len(self._row_headers)
        row_header = RowHeader(row_number)
        self._row_headers.append(row_header)

        last_item_inserted = None
        ch = self.root

        for b in bits:
            ch = ch.r
            if b == '1':
                bit_obj = DataObject(row_header, ch)
                bit_obj.c = ch
                ch.u.d = bit_obj
                bit_obj.d = ch
                bit_obj.u = ch.u
                ch.u = bit_obj
                if last_item_inserted is not None:
                    bit_obj.l = last_item_inserted
                    bit_obj.r = last_item_inserted.r
                    last_item_inserted.r.l = bit_obj
                    last_item_inserted.r = bit_obj
                last_item_inserted = bit_obj

        if last_item_inserted is not None:
            row_header.r = last_item_inserted
            row_header.l = last_item_inserted.r

    def _display_row(self, rheader):

        last_column = 0
        if rheader.r != rheader: # i.e. list is not empty
            h = rheader.l
            while True:
                for i in range(last_column, h.column_header.n):
                    print '0',
                print '1',
                last_column = h.column_header.n + 1
                if h == rheader.r:
                    break
                h = h.r
            for i in range(last_column, self.ncolumns):
                print '0',

        print

    def display(self, solution=None):
        # solution is a list of ints giving array indices
        print '%s %s' % ('*' * 44, str(solution) if solution else '')

        # traverse by rows
        print self.column_headers

        if solution is None:
            headers = self._row_headers
        else:
            headers = [self._row_headers[x] for x in solution]

        for h in headers:
            self._display_row(h)

#    def display_by_columns(self):
#
#        print '=' * 33
#
#        # traverse the whole matrix, by columns
#        c = self.root.r
#        while c != self.root:
#            print c.name
#            bit = c.d
#            while bit != c:
#                print "(%s, %d, %d)" % (bit.c.name, bit.row, bit.column),
#                bit = bit.d
#            print
#            c = c.r

    def cover_column(self, c):
        '''
        the operation of covering column c removes c from the header
        list and removes all rows in c's own list from the other
        column lists they are in.
        '''

        c.l.r = c.r
        c.r.l = c.l

        cbit = c.d
        while cbit != c:
            bit = cbit.r
            while bit != cbit:
                bit.u.d = bit.d
                bit.d.u = bit.u
                bit = bit.r
            cbit = cbit.d

        self._covered_columns.append(c)

    def uncover_column(self, c):

        c.l.r = c
        c.r.l = c

        cbit = c.u
        while cbit != c:
            bit = cbit.r
            while bit != cbit:
                bit.d.u = bit
                bit.u.d = bit
                bit = bit.r
            cbit = cbit.u

        if c != self._covered_columns[-1]:
            print "######################### %s != %s" % (c.name, self._covered_columns[-1].name)
        else:
            self._covered_columns.pop()

    def reduce_by_row(self, d):
        # d is just a data object in the matrix
        x = d.r
        while x != d:
            self.cover_column(x.c)
            x = x.r

    def unreduce_by_row(self, d):
        # d is just a data object in the matrix
        x = d.l
        while x != d:
            self.uncover_column(x.c)
            x = x.l

def log_msg(level, msg):

    print "%s%s" % ('    ' * level, msg)

solutions = []

def dlx1(matrix, partial_solution, level=0):

    global solutions

    if matrix.empty:
        l = [p.row_header.n for p in partial_solution]
        solutions.append(tuple(sorted(l)))
        return True

    # check for an empty column.  if we find one,
    # game over.
    ch = matrix.root.r
    while ch != matrix.root:
        if ch.empty:
            return False
        ch = ch.r

    # start with the leftmost column, keep trying
        
    ch = matrix.root.r
    while ch != matrix.root:

        matrix.cover_column(ch)

        # go through each row and reduce
        r = ch.d
        while r != ch:

            matrix.reduce_by_row(r)
            partial_solution.append(r)

            answer = dlx1(matrix, partial_solution, level + 1)

            partial_solution.pop()
            matrix.unreduce_by_row(r)
            r = r.d

        matrix.uncover_column(ch)
        ch = ch.r

    return False
        
def main(filename):

    matrix = Matrix()

    f = open(filename)
    h = f.readline()
    column_names = h.split()

    matrix.add_column_headers(column_names)

    # row headers are just for traversal/printing.
    # nothing in the matrix points to them.

    for line in f:
        bits = line.split()
        matrix.add_row(bits)

    matrix.display()

    partial_solution = []
    result = dlx1(matrix, partial_solution)

    sset = set(solutions)

    if len(sset) == 0:
        print 'no solution'
    else:
        for s in sset:
            matrix.display(list(s))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "arg count:  |%s|" % (''.join(sys.argv))
        sys.exit(1)

    main(sys.argv[1])


