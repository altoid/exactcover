#!/usr/bin/env python

import unittest
import dl

class TestDL(unittest.TestCase):

    def test_knuthexample(self):
        matrix = dl.matrix_from_file('test.txt')

        matrix.display_by_columns()

        # reduce by the first row with a 1 in the leftmost column

        cheader = matrix.root.r
        row = cheader.d

        updates = matrix.reduce_by_row(row)

        matrix.display_by_columns()
        print 'updates = %d' % updates

if __name__ == '__main__':
    unittest.main()

