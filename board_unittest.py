# board_unittest.py

import board
import csv
import os
import unittest

class BoardTestCase(unittest.TestCase):
    'Tests for "board.py"'

    def setUp(self):
        self._empty_board = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

        self._full_board = [[5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]]

        self._test_board = board.Board()
        self._test_board._state

        self._test_board2 = board.Board()
        self._test_board2.set_board(self._full_board)

    def test_add(self):

        self._test_board.add(0,0,1)
        self._test_board.add(8,8,9)
        self._test_board.add(5,5,4)

        self.assertEqual(self._test_board._board[0][0], 1)
        self.assertEqual(self._test_board._board[8][8], 9)
        self.assertEqual(self._test_board._board[5][5], 4)

    def test_get_board(self):
        
        self.assertEqual(len(self._test_board._state), 9)

        for row in range(len(self._test_board._state)):
            self.assertEqual(len(self._test_board._state[row]), 9)

        for row in range(len(self._test_board._state)):
            for col in range(len(self._test_board._state[row])):
                self.assertEqual(self._test_board.get_cell(row, col), 0, msg = 'board[{}][{}] should be 0.'.format(row, col))

        self._test_board.add(0,0,9)

        self.assertEqual([[9,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]],
            self._test_board.get_board())

    def test_get_cell(self):

        self.assertEqual(self._test_board.get_cell(0,0), 0)
        self.assertEqual(self._test_board.get_cell(8,8), 0)
        self.assertEqual(self._test_board.get_cell(3,3), 0)

        self._test_board.add(0,0,1)
        self._test_board.add(8,8,4)
        self._test_board.add(3,3,5)

        self.assertEqual(self._test_board.get_cell(0,0), 1)
        self.assertEqual(self._test_board.get_cell(8,8), 4)
        self.assertEqual(self._test_board.get_cell(3,3), 5)

    def test_get_row(self):

        self.assertEqual(self._test_board.get_row(0), [0,0,0,0,0,0,0,0,0])

        self._test_board.add(8,0,9)
        self._test_board.add(8,3,4)
        self._test_board.add(8,8,1)

        self.assertEqual(self._test_board.get_row(8), [9,0,0,4,0,0,0,0,1])

    def test_get_column(self):

        self.assertEqual(self._test_board.get_column(0), [0,0,0,0,0,0,0,0,0])

        self._test_board.add(0,0,5)
        self._test_board.add(4,0,1)
        self._test_board.add(8,0,9)

        self.assertEqual(self._test_board.get_column(0), [5,0,0,0,1,0,0,0,9])

    def test_get_box(self):

        self.assertEqual(self._test_board.get_box(1,1), [0,0,0,0,0,0,0,0,0])

        self._test_board.add(0,0,1)
        self._test_board.add(1,1,2)
        self._test_board.add(2,2,3)

        self.assertEqual(self._test_board.get_box(1,1), [1,0,0,0,2,0,0,0,3])

    def test_clear(self):
      
        self._test_board.add(0,0,1)
        self._test_board.add(8,8,9)
        self._test_board.add(5,5,4)

        self.assertEqual(self._test_board.clear(0,0), 1)
        self.assertEqual(self._test_board.clear(8,8), 9)
        self.assertEqual(self._test_board.clear(5,5), 4)

        self.assertEqual(self._test_board.get_cell(0,0), 0)
        self.assertEqual(self._test_board.get_cell(8,8), 0)
        self.assertEqual(self._test_board.get_cell(5,5), 0)

    def test_box_indices(self):

        self.assertEqual(self._test_board._box_indices(0,0),
            [(0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2)])

        self.assertEqual(self._test_board._box_indices(1,1),
            [(0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2)])

        self.assertEqual(self._test_board._box_indices(2,2),
            [(0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2)])

    def test_box_bounds(self):
        self.assertEqual(self._test_board._box_bounds(0,0),[(0,2),(0,2)])

        self.assertEqual(self._test_board._box_bounds(4,4),[(3,5),(3,5)])

        self.assertEqual(self._test_board._box_bounds(8,8),[(6,8),(6,8)])

    def test_to_csv(self):
        self._test_board.to_csv('sudoku_test.csv')
        with open('sudoku_test.csv', newline='') as csvfile:
            board = []
            cells = csv.reader(csvfile)
            for row in cells:
                row_values = []
                for index in range(9):
                    row_values.append(int(row[index]))
                board.append(row_values)

            self.assertEqual(board, self._empty_board)

        self._test_board2.to_csv('sudoku_test2.csv')
        with open('sudoku_test2.csv', newline='') as csvfile:
            board = []
            cells = csv.reader(csvfile)
            for row in cells:
                row_values = []
                for index in range(9):
                    row_values.append(int(row[index]))
                board.append(row_values)

            self.assertEqual(board, self._full_board)

        os.remove('sudoku_test.csv')
        os.remove('sudoku_test2.csv')

        

    def test_read_csv(self):
        self._test_board.to_csv('sudoku_test.csv')
        self._test_board2.to_csv('sudoku_test2.csv')

        new_test_board = board.Board()
        new_test_board2 = board.Board()

        new_test_board.read_csv('sudoku_test.csv')
        new_test_board2.read_csv('sudoku_test2.csv')

        self.assertEqual(new_test_board.get_board(), self._empty_board)

        self.assertEqual(new_test_board2.get_board(), self._full_board)

        os.remove('sudoku_test.csv')
        os.remove('sudoku_test2.csv')
        


if __name__ == '__main__':
    unittest.main()

