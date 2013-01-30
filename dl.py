#!/usr/bin/python

import sys
import operator

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
#            s = '%s (%d) ' % (ch.name, ch.count)
            s = '%s ' % (ch.name)
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

    def display_by_columns(self):

        print '=' * 44
        cheader = self.root.r
        rendition = []
        while cheader != self.root:
            s = cheader.name
            last_row = 0
            b = cheader.d
            while b != cheader:

                for i in range(last_row, b.row_header.n):
                    s += '0'
                s += '1'
                last_row = b.row_header.n + 1

                b = b.d
            for i in range(last_row, len(self._row_headers)):
                s += '0'

            cheader = cheader.r
            rendition.append(s)

        nrows = len(rendition[1:])

        s = ''
        for c in rendition:
            s += c[0]
        print ' '.join(s)

        rcount = 0
        for j in range(nrows):
            s = ''
            for c in rendition:
                s += c[j + 1]

            if s != '0' * len(rendition):
                s = ' '.join(s) + ' (%d)' % self._row_headers[rcount].n
                print s
            rcount += 1

    def cover_column(self, c):
        '''
        the operation of covering column c removes c from the header
        list and removes all rows in c's own list from the other
        column lists they are in.

        returns the number of objects removed from the column; i.e. the number
        of dance steps.
        '''

        c.l.r = c.r
        c.r.l = c.l
        steps = 0

        cbit = c.d
        while cbit != c:
            bit = cbit.r
            while bit != cbit:
                bit.u.d = bit.d
                bit.d.u = bit.u
                bit = bit.r
                bit.c.count -= 1
                steps += 1
            cbit = cbit.d

        self._covered_columns.append(c)
        return steps

    def reduce_by_row(self, d):
        # d is just a data object in the matrix
        x = d.r
        updates = 0
        while x != d:
            updates += self.cover_column(x.c)
            x = x.r

        return updates

    def uncover_column(self, c):

        '''
        undoes cover_column.  note that it applies its steps in reverse order.
        
        returns the number of objects returned to the column; i.e. the number
        of dance steps.
        '''
        
        c.l.r = c
        c.r.l = c
        steps = 0

        cbit = c.u
        while cbit != c:
            bit = cbit.r
            while bit != cbit:
                bit.d.u = bit
                bit.u.d = bit
                bit = bit.r
                bit.c.count += 1
                steps += 1
            cbit = cbit.u

        if c != self._covered_columns[-1]:
            raise ValueError("######################### %s != %s" % (c.name, self._covered_columns[-1].name))

        self._covered_columns.pop()
        return steps

    def unreduce_by_row(self, d):
        # d is just a data object in the matrix
        x = d.l
        updates = 0
        while x != d:
            updates += self.uncover_column(x.c)
            x = x.l

        return updates

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
        self.updates = 0

    def leftmost_all(self):
        # generator.  naively picks the leftmost available column in the array.
        ch = self._matrix.root.r
        while ch != self._matrix.root:
            yield ch
            ch = ch.r

    def leftmost(self):
        # generator.  naively picks the leftmost available column in the array.
        ch = self._matrix.root.r
        if ch != self._matrix.root:
            yield ch

    def shortest(self):
        # generator.  returns the shortest column encountered in traversing the colums left to right.
        # knuth's S heuristic.

        ch = self._matrix.root.r
        s = ch.count
        shortest = ch
        while ch != self._matrix.root:
            if ch.count < s:
                s = ch.count
                shortest = ch
            ch = ch.r

        yield shortest

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
    
#        for ch in self.leftmost():    
        updates = 0
        for ch in self.shortest():
            updates += self._matrix.cover_column(ch)
    
            # go through each row and reduce
            r = ch.d
            while r != ch:
    
                updates += self._matrix.reduce_by_row(r)
                self._partial_solution.append(r)
    
                answer = self.dlx1(level + 1)
    
                self._partial_solution.pop()
                updates += self._matrix.unreduce_by_row(r)

                r = r.d

            updates += self._matrix.uncover_column(ch)

#        log_msg(level, 'updates this level (%d):  %d' % (level, updates))
        self.updates += updates
                
        self.backtracks += 1
        return False

    @property 
    def solutions(self):
        return self._solutions

def matrix_from_file(filename):

    matrix = Matrix()

    f = open(filename)
    column_names = None

    for line in f:
        text = line.split('#', 1)[0]
        elements = text.split()
        if not elements:
            continue

        if column_names is None:
            column_names = elements
            matrix.add_column_headers(column_names)
        else:
            matrix.add_row(elements)

    return matrix

def main(filename):

    matrix = matrix_from_file(filename)

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
    print 'updates: %d' % dlx.updates

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "arg count:  |%s|" % (''.join(sys.argv))
        sys.exit(1)

    main(sys.argv[1])


