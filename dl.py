#!/usr/bin/python

import sys

class ColumnObject:

    def __init__(self, name):

        self._name = name
        self.l = self.r = self.u = self.d = self

    @property
    def name(self):
        return self._name

    @property
    def empty(self):
        return self.d == self

class RowHeader:

    def __init__(self, row):

        self._row = row
        self.l = self.r = self.u = self.d = self

    @property
    def row(self):
        return self._row

class DataObject:

    def __init__(self, row, column):

        self.l = self.r = self.u = self.d = self
        self.c = None
        self._row = row
        self._column = column

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

class Matrix:

    def __init__(self):
        self.root = ColumnObject('root')
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

        for n in column_names:
            column_header = ColumnObject(n)
            self.root.l.r = column_header
            column_header.r = self.root
            column_header.l = self.root.l
            self.root.l = column_header
        self.ncolumns = len(column_names)

    def add_row(self, bits, row_number):

        # the row headers are just to aid in traversal.  nothing in
        # the array points to them.

        row_header = RowHeader(row_number)
        self._row_headers.append(row_header)

        last_item_inserted = None
        ch = self.root
        col_counter = 0
        for b in bits:
            ch = ch.r
            if b == '1':
                bit_obj = DataObject(row_number, col_counter)
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
            col_counter += 1

        if last_item_inserted is not None:
            row_header.r = last_item_inserted
            row_header.l = last_item_inserted.r

    def _display_row(self, rheader):

        last_column = 0
        if rheader.r != rheader: # i.e. list is not empty
            h = rheader.l
            while True:
                for i in range(last_column, h.column):
                    print '0',
                print '1',
                last_column = h.column + 1
                if h == rheader.r:
                    break
                h = h.r
            for i in range(last_column, self.ncolumns):
                print '0',

        print

    def display(self, partial_solution=None):

        print '*' * 44

        # traverse by rows
        print self.column_headers

        for rheader in self._row_headers:

            if partial_solution is None:
                self._display_row(rheader)
            elif rheader.row in partial_solution:
                self._display_row(rheader)

    def display_by_columns(self):

        print '=' * 33

        # traverse the whole matrix, by columns
        c = self.root.r
        while c != self.root:
            print c.name
            bit = c.d
            while bit != c:
                print "(%s, %d, %d)" % (bit.c.name, bit.row, bit.column),
                bit = bit.d
            print
            c = c.r

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
            print "#########################"
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

def dlx1(matrix, partial_solution, level=0):

    if matrix.empty:
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

            answer = dlx1(matrix, partial_solution, level + 1)

            if answer == True:
                partial_solution.append(r.row)
                return True

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

    row_counter = 0
    for line in f:
        bits = line.split()
        matrix.add_row(bits, row_counter)

        row_counter += 1

    matrix.display()

    partial_solution = []
    result = dlx1(matrix, partial_solution)

    while len(matrix._covered_columns) > 0:
        matrix.uncover_column(matrix._covered_columns[-1])

    if result:
        print partial_solution
        matrix.display(partial_solution)
    else:
        print 'no solution'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "arg count:  |%s|" % (''.join(sys.argv))
        sys.exit(1)

    main(sys.argv[1])


