#!/usr/bin/env python

import unittest
import dl

class TestDL(unittest.TestCase):

    def test_knuthexample(self):
        matrix = dl.matrix_from_file('test.txt')

        updates = 0

        matrix.display_by_columns()

        # reduce by the first row with a 1 in the leftmost column

        cheader = matrix.root.r
        row = cheader.d

        print 'reducing by row %d' % row.row_header.n

        updates = matrix.reduce_by_row(row)
        matrix.display_by_columns()

        updates = matrix.unreduce_by_row(row)
        matrix.display_by_columns()

if __name__ == '__main__':
    unittest.main()

