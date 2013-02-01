#!/usr/bin/env python

import unittest
import sudoku
import pdb

class TestSudoku(unittest.TestCase):

    def test_gen_number_row(self):

        v = sudoku.gen_number_row(1, 0, 1, 4)
        self.assertEquals('0100000000000000', v)

        v = sudoku.gen_number_row(1, 1, 3, 4)
        self.assertEquals('0000000100000000', v)

    def test_gen_row_row(self):

        v = sudoku.gen_row_row(4, 0, 3, 4)
        self.assertEquals('0000000000000001', v)

        v = sudoku.gen_row_row(2, 2, 2, 4)
        self.assertEquals('0000000001000000', v)

    def test_gen_column_row(self):

        v = sudoku.gen_column_row(2, 1, 0, 4)
        self.assertEquals('0000010000000000', v)

        v = sudoku.gen_column_row(4, 0, 3, 4)
        self.assertEquals('0001000000000000', v)

    def test_gen_region_row(self):

        v = sudoku.gen_region_row(4, 1, 1, 4)
        self.assertEquals('0001000000000000', v)

        v = sudoku.gen_region_row(4, 1, 2, 4)
        self.assertEquals('0000000000010000', v)

    def test_gen_row(self):

        size = 9

        for i in range(1, size + 1):
            for x in range(size):
                for y in range(size):

                    row = list(sudoku.gen_row(i, x, y, size))

                    ni, nx, ny = sudoku.values_from_row(row)

                    self.assertEquals(i, ni)
                    self.assertEquals(x, nx)
                    self.assertEquals(y, ny)

    def test_rownum_tuple(self):

        size = 9
        nrows = size ** 3

        for r in range(nrows):

            t = sudoku.tuple_from_rownum(r)
            r2 = sudoku.rownum_from_tuple(t)

            t2 = sudoku.tuple_from_rownum(r2)

            self.assertEquals(t, t2)
            self.assertEquals(r, r2)

    def test_rows_to_tableau(self):

        filename = 'sudoku4_1.txt'

        size, initial = sudoku.tableau_from_file(filename)
        print size, initial

        tableau = sudoku.rows_to_tableau(initial, size)

        for row in tableau:
            print row

if __name__ == '__main__':
    unittest.main()

