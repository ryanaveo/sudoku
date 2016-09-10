# sudokugame_unittest.py

import sudokugame
import board
import unittest

class GameTestCase(unittest.TestCase):
    'Tests for "sudokugame.py"'

    def setUp(self):
        self._game = sudokugame.Game()
        
        self._win_board = [[5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]]

    def test_open_cells(self):
        self.assertEqual(len(self._game.open_cells()), 81)

        self._game._board.set_board([
            [1,2,3,4,5,6,7,8,9],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]])

        self.assertEqual(len(self._game.open_cells()), 72)
        self.assertEqual(self._game.open_cells(), 
            [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
            (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),
            (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),
            (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
            (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),
            (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
            (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),
            (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8)])

    def test_add_number(self):
        self._game.add_number(1,1,3)

        self.assertEqual(self._game._board.get_cell(1,1), 3)

        self.assertEqual(self._game._undo_list, [(sudokugame.Move(move_type = 'add', row = 1, col = 1, num = 3))])
        self.assertEqual(len(self._game._redo_list), 0)

    def test_undo_move(self):
    	self.assertRaises(sudokugame.UndoError, self._game.undo_move)

    	self._game.add_number(1,1,3)
    	self._game.undo_move()

    	self.assertEqual(self._game._board._state[1][1], 0)
    	self.assertEqual(self._game._redo_list, [sudokugame.Move(move_type = 'add', row = 1, col = 1, num = 3)])

    	self._game.add_number(5,5,4)
    	self._game.remove_number(5,5)
    	self._game.undo_move()

    	self.assertEqual(self._game._board._state[5][5], 4)
    	self.assertEqual(self._game._redo_list, [sudokugame.Move(move_type = 'remove', row = 5, col = 5, num = 4)])

    def test_redo_move(self):
    	self.assertRaises(sudokugame.RedoError, self._game.redo_move)

    	self._game.add_number(2,2,3)
    	self._game.undo_move()
    	self._game.redo_move()

    	self.assertEqual(self._game._board._state[2][2], 3)
    	self.assertEqual(self._game._undo_list, [sudokugame.Move(move_type = 'add', row = 2, col = 2, num = 3)])

    	self._game.add_number(8,8,5)
    	self._game.remove_number(8,8)
    	self._game.undo_move()
    	self._game.redo_move()

    	self.assertEqual(self._game._board._state[8][8], 0)
    	self.assertEqual(self._game._undo_list, [sudokugame.Move(move_type='add', row=2, col=2, num=3), sudokugame.Move(move_type='add', row=8, col=8, num=5), sudokugame.Move(move_type='remove', row=8, col=8, num=5)])

    def test_remove_number(self):
        self._game.add_number(1,1,9)
        self._game.remove_number(1,1)
        
        self.assertFalse(self._game._board.get_cell(1,1) == 9)
        self.assertEqual(self._game._board.get_cell(1,1), 0)

        self.assertEqual(self._game._undo_list, [sudokugame.Move(move_type = 'add', row = 1, col = 1, num = 9), sudokugame.Move(move_type = 'remove', row = 1, col = 1, num = 9)])

        self.assertEqual(len(self._game._redo_list), 0)

    def test_check_victory(self):
        self.assertFalse(self._game.check_victory())

        self._game._board.set_board(self._win_board)

        self.assertTrue(self._game.check_victory())

    def test_validate_move(self):
        self._game._board.add(0,1,2)

        self.assertRaises(sudokugame.OccupiedCellError, self._game._validate_move, 0, 1, 3)
        self.assertRaises((sudokugame.CellOutOfBoundsError, IndexError), self._game._validate_move, 9, 9, 1)
        self.assertRaises(sudokugame.SameRowError, self._game._validate_move, 0, 2, 2)
        self.assertRaises(sudokugame.SameColumnError, self._game._validate_move, 5, 1, 2)
        self.assertRaises(sudokugame.SameBoxError, self._game._validate_move, 2, 2, 2)

        self.assertRaises(sudokugame.InvalidNumberError, self._game._validate_move, 4, 4, -5)
        self.assertRaises(sudokugame.InvalidNumberError, self._game._validate_move, 4, 4, 0)
        self.assertRaises(sudokugame.InvalidNumberError, self._game._validate_move, 4, 4, 10)
if __name__ == '__main__':
    unittest.main()
