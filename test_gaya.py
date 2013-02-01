#!/usr/bin/env python

import unittest
import gaya

class TestGaya(unittest.TestCase):

    def test_xyz_to_cell(self):
    
        self.assertEquals(0, gaya.xyz_to_cell((0,0,0)))
        self.assertEquals(4, gaya.xyz_to_cell((4,0,0)))
        self.assertEquals(20, gaya.xyz_to_cell((0,4,0)))
        self.assertEquals(24, gaya.xyz_to_cell((4,4,0)))

        self.assertEquals(70, gaya.xyz_to_cell((0,4,2)))

        self.assertEquals(124, gaya.xyz_to_cell((4,4,4)))

    def test_cell_to_xyz(self):

        self.assertEquals( (0,0,0), gaya.cell_to_xyz(0))

        self.assertEquals( (0, 4, 4), gaya.cell_to_xyz(120))

if __name__ == '__main__':
    unittest.main()

