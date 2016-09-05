#!/usr/bin/python3

# sudokugame.py

import board
from collections import namedtuple

Move = namedtuple('Move', 'move_type row col num')

class Game():
	'''Handles all the game logic and interfaces with the board to execute moves.'''

	def __init__(self):
		'Starts a new game'
		self._board = board.Board()
		self._undo_list = []
		self._redo_list = []
			
	def new_game(self):
		'Creates a new board to start a new game'
		pass

	def get_board(self):
		'Returns a representation of the game board.'
		pass

	def open_cells(self):
		'Returns a list of the cells that are empty.'
		pass

	def add_number(self, row: int, col: int, number: int):
		"Executes a move if it's valid. Adds move to undo list and clears redo list"
		self._validate_move(row, col, number)
		self._board.add(row, col, number)

		move = self._store_move('add', row, col, number)
		self._undo_list.append(move)
		self._redo_list = []


	def undo_move(self):
		'Undoes the last move if there are any. Otherwise raises exception.'
		if len(self._undo_list) == 0:
			raise UndoError

		else:
			last_move = self._undo_list.pop()
			if last_move.move_type == 'add':
				self._board.clear(last_move.row, last_move.col)
			elif last_move.move_type == 'remove':
				self._board.add(last_move.row, last_move.col, last_move.number)
			
			self._redo_list.append(last_move)


	def redo_move(self):
		'Redoes the last undo if there are any. Otherwise raises exception.'
		if len(self._redo_list) == 0:
			raise RedoError

		else:
			last_undo = self._redo_list.pop()
			if last_undo.move_type == 'add':
				self._board.add(last_undo.row, last_undo.col, last_undo.number)
			elif last_undo.move_type == 'remove':
				self._board.clear(last_undo.row, last_undo.col)
			
			self._undo_list.append(last_undo)


	def remove_number(self, row: int, col: int):
		"Remove a number from the given cell"
		number = self._board.clear(row, col)
		move = self._store_move('remove', row, col, number)
		
		self._undo_list.append(move)
		self._redo_list = []

	def save_state(self, state_name: str='save'):
		'''
		Saves the current state. Uses state_name to name the csv file in
		the board's to_csv call. 
		'''
		pass

	def load_state(self, state_name: str='save'):
		'Loads a board state'
		pass

	def check_victory(self) -> bool:
		'Checks the victory conditions have been met.'
		pass

	def print_board(self):
		"Prints the board using the board's print_board method"
		pass

	def _store_move(self, move_type: str, row: int, col: int, number: int):
		'Creates a Move namedtuple that stores information about the move for undo and redo. Type will be "add" or "remove" depending on what was done'
		move = Move(move_type, row, col, number)
		
		return move

	def _validate_move(self, row: int, col: int, number: int):
		'''
		Raises an exception if the given move is valid on the board.
		Needs to check:
			(1) Cell is within the board's bounds
			(2) Cell is not occupied
			(3) The move doesn't have any of the same entry in the same column, row, or box.
			(4) The number is valid (1-9)
		'''
		if self._cell_is_occupied(self, row: int, col: int):
			raise OccupiedCellError

		if not self._cell_in_bounds(self, row: int, col: int):
			raise CellOutOfBoundsError

		if self._same_num_in_row(self, row: int, number: int):
			raise SameRowError

		if self._same_num_in_col(self, col: int, number: int):
			raise SameColumnError
		
		if self._same_num_in_box(self, row: int, col: int, number: int):
			raise SameBoxError

		if not self._valid_number(self, number: int):
			raise InvalidNumberError

	def _cell_is_occupied(self, row: int, col: int):
		'Returns a bool that indicates if a cell is occupied'
		return self._board._state[row][col] != 0

	def _cell_in_bounds(self, row: int, col: int):
		'Returns a bool that indicates if the given row and column are in the dimension of the board'

		return (0 <= row <= 8) and (0 <= col <= 8)

	def _same_num_in_row(self, row: int, number: int):
		'Returns a bool that indicates if the given number is already in the given row'

		return number in self._board.get_row(row)

	def _same_num_in_col(self, col: int, number: int):
		'Returns a bool that indicates if the given number is already in the given column'

		return number in self._board.get_column(col)

	def _same_num_in_box(self, row: int, col: int, number: int):
		'Returns a bool that indicates if the given number is already in the respective box of the given cell'

		return number in self._board.get_box(row, col)

	def _valid_number(self, number: int):
		'Returns a bool that indicates if the given number is valid'

		return 1 <= number <= 9

class OccupiedCellError(Exception):
	'Exception for trying to make a move on an occupied cell.'
	pass

class CellOutOfBoundsError(Exception):
	'Exception for giving coordinates that are outside of the board.'
	pass

class SameRowError(Exception):
	'Exception for moves whose numbers have already been seen in the same row.'
	pass

class SameColumnError(Exception):
	'Exception for moves whose numbers have already been seen in the same column.'
	pass

class SameBoxError(Exception):
	'Exception for moves whose numbers have already been seen in the same box.'
	pass

class InvalidNumberError(Exception):
	'Exception for attempts to place an invalid number (any number not 1-9) in a cell'
	pass

class UndoError(Exception):
	'Exception for attempts to undo when there are no moves to undo'
	pass

class RedoError(Exception):
	'Exception for attempts to redo when there are no moves to redo'
	pass