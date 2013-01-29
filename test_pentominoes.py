#!/usr/bin/env python

import unittest
import pentominoes

class TestPentominoes(unittest.TestCase):

    def test_print(self):

        p = pentominoes.make_piece('f')
        p = p.moveto(0, 0)
        print p

    def test_equal(self):

        p = pentominoes.make_piece('f')

        q = p.moveto(10, 10)

        self.assertTrue(p == p)
        self.assertFalse(p == q)

    def test_generate(self):

        b = pentominoes.Board()

        p = pentominoes.make_piece('i')

        for i in pentominoes.orientations(p):
            print '=' * 33
            print i

    def test_transformations(self):

        points = ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1))
        p = pentominoes.Piece(points)

        p2 = p.moveto(20, 20)

        print p
        print p2

        p3 = p.moveto(10, 10).flip_x().moveto(0, 0)
        print p3

        p4 = p.clockwise_90().moveto(0, 0)
        print p4

        p5 = p.counterclockwise_90().moveto(0, 0)
        print p5

    def test_translation(self):

        p = pentominoes.make_piece('f')
        
        x = y = 0
        p = p.moveto(x, y)

        while p._maxy < 8:
            while p._maxx < 8:
                print '[minx = %d, miny = %d, maxx = %d, maxy = %d]' % (p._minx, p._miny, p._maxx, p._maxy)
                x += 1
                p = p.moveto(x, y)
            x = 0
            y += 1
            p = p.moveto(x, y)

    def test_board(self):

        b = pentominoes.Board()

        p = pentominoes.make_piece('f')

        b.place_piece(p, 0, 0)

        b.print_()

if __name__ == '__main__':
    unittest.main()
