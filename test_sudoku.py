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

        # i, x, y
        for i in range(1, 5):
            for x in range(4):
                for y in range(4):
#                    pdb.set_trace()
#                    print i,x,y
                    v = sudoku.gen_row(i, x, y, 4)
                    l = list(v)
                    s = [' ' if b == '0' else b for b in l]
                    print ''.join(s)

if __name__ == '__main__':
    unittest.main()

