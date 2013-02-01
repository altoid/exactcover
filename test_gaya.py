#!/usr/bin/env python

import unittest
import gaya
import pentominoes

class TestGaya(unittest.TestCase):

    def test_translate_to_plane(self):

        ypiece = pentominoes.make_piece('y')

        with self.assertRaises(ValueError):
            gaya.translate_to_plane(ypiece, xplane=0, yplane=0)

        for p in ypiece:
            print p
        print ypiece

        print gaya.translate_to_plane(ypiece, zplane=0)

        print gaya.translate_to_plane(ypiece, xplane=3)

        yp = gaya.translate_to_plane(ypiece, yplane=4)

        for p in yp:
            print p,gaya.xyz_to_cell(p)

        knob = gaya.find_outlier(yp)
        print knob,gaya.xyz_to_cell(knob)

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

