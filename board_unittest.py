# board_unittest.py

import board
import unittest

class BoardTestCase(unittest.TestCase):
	'Tests for "board.py"'

	def setUp(self):

		test_board = board.Board()
		board_state = test_board.get_board()

	def test_get_board(self):
		
		self.assertEqual(len(board_state), 9)

		for row in board_state:
			self.assertEqual(len(board_state[row]), 9)

		for row in board_state:
			for col in test_board[row]:
				self.assertEqual(test_board.get_cell(row, col), 0, msg = 'board[{}][{}] should be 0.'.format(row, col))

		test_board.add(0,0,9)

		self.assertEqual([[9,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0]],
			test_board.get_board())

	def test_get_cell(self):

		self.assertEqual(test_board.get_cell(0,0), 0)
		self.assertEqual(test_board.get_cell(8,8), 0)
		self.assertEqual(test_board.get_cell(3,3), 0)

		test_board.add(0,0,1)
		test_board.add(8,8,4)
		test_board.add(3,3,5)

		self.assertEqual(test_board.get_cell(0,0), 1)
		self.assertEqual(test_board.get_cell(8,8), 4)
		self.assertEqual(test_board.get_cell(3,3), 5)

	def test_get_row(self):

		self.assertEqual(test_board.get_row(0), [0,0,0,0,0,0,0,0,0])

		test_board.add(8,0,9)
		test_board.add(8,3,4)
		test_board.add(8,8,1)

		self.assertEqual(test_board.get_row(1), [9,0,0,4,0,0,0,0,1])

	def test_get_column(self):

		self.assertEqual(test_board.get_column(0), [0,0,0,0,0,0,0,0,0])

		test_board.add(0,0,5)
		test_board.add(4,0,1)
		test_board.add(8,0,9)

		self.assertEqual(test_board.get_row(), [5,0,0,0,1,0,0,0,9])

	def test_get_box(self):

		self.assertEqual(test_board.get_box(1,1), [0,0,0,0,0,0,0,0,0])

		test_board.add(0,0,1)
		test_board.add(1,1,2)
		test_board.add(2,2,3)

		self.assertEqual(test_board.get_box(1,1), [1,0,0,0,2,0,0,0,3])

	def test_add(self):

		test_board.add(0,0,1)
		test_board.add(8,8,9)
		test_board.add(5,5,4)

		self.assertEqual(test_board.get_cell(0,0), 1)
		self.assertEqual(test_board.get_cell(8,8), 9)
		self.assertEqual(test_board.get_cell(5,5), 4)
		
	def test_clear(self):

		test_board.add(0,0,1)
		test_board.add(8,8,9)
		test_board.add(5,5,4)

		self.assertEqual(test_board.clear(0,0), 1)
		self.assertEqual(test_board.clear(8,8), 9)
		self.assertEqual(test_board.clear(5,5), 4)

		self.assertEqual(test_board.get_cell(0,0), 0)
		self.assertEqual(test_board.get_cell(8,8), 0)
		self.assertEqual(test_board.get_cell(5,5), 0)

	def test_box_indices(self):

		self.assertEqual(test_board._box_indices(0,0),
			[(0,0),(0,1),(0,2),
			(1,0),(1,1),(1,2),
			(2,0),(2,1),(2,2)])

		self.assertEqual(test_board._box_indices(1,1),
			[(0,0),(0,1),(0,2),
			(1,0),(1,1),(1,2),
			(2,0),(2,1),(2,2)])

		self.assertEqual(test_board._box_indices(2,2),
			[(0,0),(0,1),(0,2),
			(1,0),(1,1),(1,2),
			(2,0),(2,1),(2,2)])




if __name__ == '__main__':
	unittest.main()

