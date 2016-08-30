# board_unittest.py

import board
import unittest

class BoardTestCase(unittest.TestCase):
	'Tests for "board.py"'

	def setUp(self):
		self._test_board = board.Board()
		self._board_state = self._test_board.get_board()

	def test_add(self):

		self._test_board.add(0,0,1)
		self._test_board.add(8,8,9)
		self._test_board.add(5,5,4)

		self.assertEqual(self._test_board._board[0][0], 1)
		self.assertEqual(self._test_board._board[8][8], 9)
		self.assertEqual(self._test_board._board[5][5], 4)

	def test_get_board(self):
		
		self.assertEqual(len(self._board_state), 9)

		for row in range(len(self._board_state)):
			self.assertEqual(len(self._board_state[row]), 9)

		for row in range(len(self._board_state)):
			for col in range(len(self._board_state[row])):
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

##	def test_get_box(self):
##
##		self.assertEqual(self._test_board.get_box(1,1), [0,0,0,0,0,0,0,0,0])
##
##		self._test_board.add(0,0,1)
##		self._test_board.add(1,1,2)
##		self._test_board.add(2,2,3)
##
##		self.assertEqual(self._test_board.get_box(1,1), [1,0,0,0,2,0,0,0,3])
##
##	def test_clear(self):
##
##		self._test_board.add(0,0,1)
##		self._test_board.add(8,8,9)
##		self._test_board.add(5,5,4)
##
##		self.assertEqual(self._test_board.clear(0,0), 1)
##		self.assertEqual(self._test_board.clear(8,8), 9)
##		self.assertEqual(self._test_board.clear(5,5), 4)
##
##		self.assertEqual(self._test_board.get_cell(0,0), 0)
##		self.assertEqual(self._test_board.get_cell(8,8), 0)
##		self.assertEqual(self._test_board.get_cell(5,5), 0)
##
##	def test_box_indices(self):
##
##		self.assertEqual(self._test_board._box_indices(0,0),
##			[(0,0),(0,1),(0,2),
##			(1,0),(1,1),(1,2),
##			(2,0),(2,1),(2,2)])
##
##		self.assertEqual(self._test_board._box_indices(1,1),
##			[(0,0),(0,1),(0,2),
##			(1,0),(1,1),(1,2),
##			(2,0),(2,1),(2,2)])
##
##		self.assertEqual(self._test_board._box_indices(2,2),
##			[(0,0),(0,1),(0,2),
##			(1,0),(1,1),(1,2),
##			(2,0),(2,1),(2,2)])
##
##


if __name__ == '__main__':
	unittest.main()

