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

if __name__ == '__main__':
    unittest.main()

