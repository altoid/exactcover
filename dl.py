#!/usr/bin/python

import sys

class ColumnHeader:

    def __init__(self, name, col_number=0):

        self._name = name
        self._n = col_number
        self.l = self.r = self.u = self.d = self
        self.count = 0 # no. of bits in column

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
            s = '%s (%d) ' % (ch.name, ch.count)
            result = result + s
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
                ch.count += 1

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
                bit.c.count -= 1
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
                bit.c.count += 1
            cbit = cbit.u

        if c != self._covered_columns[-1]:
            raise ValueError("######################### %s != %s" % (c.name, self._covered_columns[-1].name))

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

class DLXAlgorithm:

    def __init__(self, matrix):

        self._matrix = matrix
        self._solutions = set()
        self._partial_solution = []
        self.nodes = 0
        self.leaves = 0
        self.backtracks = 0

    def dlx1(self, level=0):

#        log_msg(level, self._matrix.column_headers)

        self.nodes += 1
        if self._matrix.empty:
            l = [p.row_header.n for p in self._partial_solution]
            self._solutions.add(tuple(sorted(l)))
            self.leaves += 1
            return True
    
        # check for an empty column.  if we find one,
        # game over.
        ch = self._matrix.root.r
        while ch != self._matrix.root:
            if ch.empty:
                self.backtracks += 1
                return False
            ch = ch.r
    
        # start with the leftmost column, keep trying
            
        ch = self._matrix.root.r
        while ch != self._matrix.root:
    
            self._matrix.cover_column(ch)
    
            # go through each row and reduce
            r = ch.d
            while r != ch:
    
                self._matrix.reduce_by_row(r)
                self._partial_solution.append(r)
    
                answer = self.dlx1(level + 1)
    
                self._partial_solution.pop()
                self._matrix.unreduce_by_row(r)
                r = r.d

            self._matrix.uncover_column(ch)
            ch = ch.r
    
        self.backtracks += 1
        return False

    @property 
    def solutions(self):
        return self._solutions

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

    dlx = DLXAlgorithm(matrix)
    dlx.dlx1()
    solutions = dlx.solutions

    if len(solutions) == 0:
        print 'no solution'
    else:
        for s in solutions:
            matrix.display(list(s))

    print 'nodes:  %d' % dlx.nodes
    print 'leaves: %d' % dlx.leaves
    print 'backtracks: %d' % dlx.backtracks

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "arg count:  |%s|" % (''.join(sys.argv))
        sys.exit(1)

    main(sys.argv[1])


