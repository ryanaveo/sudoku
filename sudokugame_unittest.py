# sudokugame_unittest.py

import sudokugame
import board
import unittest

class BoardTestCase(unittest.TestCase):
	'Tests for "sudokugame.py"'

	def setUp(self):
		test_board = board.Board()
		board_state = test_board.get_board()
		game = sudokugame.Game()
		
		win_board = [[5,3,4,6,7,8,9,1,2],
		[6,7,2,1,9,5,3,4,8],
		[1,9,8,3,4,2,5,6,7],
		[8,5,9,7,6,1,4,2,3],
		[4,2,6,8,5,3,7,9,1],
		[7,1,3,9,2,4,8,5,6],
		[9,6,1,5,3,7,2,8,4],
		[2,8,7,4,1,9,6,3,5],
		[3,4,5,2,8,6,1,7,9]]

	def test_valid_move(self):
		self.assertTrue(game.valid_move(0,0,1))
		self.assertFalse(game.valid_move(9,9,1))

		test_board.add(0,0,2)

		self.assertFalse(game.valid_move(0,0,1))

		self.assertFalse(game.valid_move(0,3,2))
		self.assertFalse(game.valid_move(5,0,2))
		self.assertFalse(game.valid_move(2,2,2))

	def test_open_cells(self):
		self.assertEqual(len(game.open_cells), 81)

		test_board.set_board([
			[1,2,3,4,5,6,7,8,9],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0]])

		self.assertEqual(len(game.open_cells), 72)
		self.assertEqual(game.open_cells, 
			[(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
			(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),
			(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),
			(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
			(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),
			(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
			(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),
			(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8)])

	def test_make_move(self):
		test_board.add(1,1,3)

		self.assertRaises(OccupiedCellException, game.make_move(), 1, 1, 1)
		self.assertRaises(CellOutOfBoundsException, game.make_move(), 9, 9, 1)
		self.assertRaises(SameRowException, game.make_move(), 1, 2, 3)
		self.assertRaises(SameColumnException, game.make_move(), 5, 1, 3)
		self.assertRaises(SameBoxException, game.make_move(), 0, 0, 3)

	def remove(self):
		

	def check_victory(self):
		self.assertFalse(game.check_victory())

		test_board.set_board(win_board)

		self.assertTrue(game.check_victory())

