#!/usr/bin/env python

import unittest
import dl

class TestDL(unittest.TestCase):

    def test_initial_solution_set(self):

        '''
        test behavior when algorithm is seeded with a set of rows
        that are expected to be part of the solution
        '''

        # solution for test.txt is [0,3,4]
        # so if we seed with row 1 we should get no solution

#        matrix = dl.matrix_from_file('test.txt')
        matrix = dl.matrix_from_file('two_solutions.txt')

        matrix.display_by_columns()

        matrix.display_sloppy()

        seeds = None
        seeds = [3]

        dlx = dl.DLXAlgorithm(matrix, seeds=seeds)
        dlx.dlx1()

        for s in dlx.solutions:
            matrix.display_by_rows(list(s))

    def test_cover_and_reduction(self):

        matrix = dl.matrix_from_file('test.txt')

        updates = 0

        matrix.display_by_columns()

        # reduce by the first row with a 1 in the leftmost column

        cheader = matrix.root.r
        row = cheader.d

        print 'covering column %s' % cheader
        matrix.cover_column(cheader)

        print 'reducing by row %d' % row.row_header.n

        updates = matrix.reduce_by_row(row)
        matrix.display_by_columns()

        updates = matrix.unreduce_by_row(row)
        matrix.uncover_column(cheader)

        matrix.display_by_columns()

    def test_row_reduction(self):
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

